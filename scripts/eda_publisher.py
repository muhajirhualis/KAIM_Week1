# scripts/eda_publisher.py
import pandas as pd
import matplotlib.pyplot as plt
import re

def extract_domains(df):
    """
    Extract email domains from publisher names (e.g., 'john@reuters.com' → 'reuters.com').
    If not an email, keep original (e.g., 'Benzinga Insights' → 'benzinga insights').
    """
    def get_domain(pub):
        if not isinstance(pub, str):
            return "unknown"
        pub = pub.strip().lower()
        # Simple email pattern: contains @ and . after @
        match = re.search(r"@([a-z0-9.-]+\.[a-z]{2,})", pub)
        if match:
            return match.group(1)
        # Fallback: normalize known patterns (e.g., "Benzinga Insights" → "benzinga")
        if "benzinga" in pub:
            return "benzinga.com"
        if "reuters" in pub:
            return "reuters.com"
        if "bloomberg" in pub:
            return "bloomberg.com"
        if "cnbc" in pub:
            return "cnbc.com"
        return pub  # keep as-is if unclear
    
    df = df.copy()
    df["publisher_domain"] = df["publisher"].apply(get_domain)
    return df


def top_publishers_analysis(df, top_n=10):
    """
    Show top publishers by article count and domain-level aggregation.
    """
    # Raw publishers
    pub_counts = df["publisher"].value_counts()
    print(f"📰 Top {top_n} Raw Publishers:")
    for i, (pub, cnt) in enumerate(pub_counts.head(top_n).items(), 1):
        print(f"{i:2}. {pub[:40]:<40} → {cnt:>6} articles")

    # Domains
    domain_counts = df["publisher_domain"].value_counts()
    print(f"\n🏢 Top {top_n} Publisher Domains:")
    for i, (dom, cnt) in enumerate(domain_counts.head(top_n).items(), 1):
        pct = cnt / len(df) * 100
        print(f"{i:2}. {dom:<30} → {cnt:>6} ({pct:4.1f}%)")

    # Plot domains
    plt.figure(figsize=(10, 5))
    domain_counts.head(10).plot(kind="barh", color="lightcoral")
    plt.gca().invert_yaxis()
    plt.title("Top 10 Publisher Domains")
    plt.xlabel("Number of Articles")
    plt.tight_layout()
    plt.show()
    
    return pub_counts, domain_counts


def publisher_content_analysis(df, top_domains=None):
    """
    Compare content differences across top publishers:
    - Avg headline length
    - % mentioning 'price target', 'upgrade', 'fda'
    """
    if top_domains is None:
        top_domains = df["publisher_domain"].value_counts().head(5).index.tolist()
    
    results = []
    for domain in top_domains:
        subset = df[df["publisher_domain"] == domain]
        if len(subset) == 0:
            continue
        avg_len = subset["headline_len"].mean()
        pct_price = subset["headline"].str.contains("price target", case=False, na=False).mean() * 100
        pct_upgrade = subset["headline"].str.contains("upgrade|raised", case=False, na=False).mean() * 100
        pct_fda = subset["headline"].str.contains("fda", case=False, na=False).mean() * 100
        
        results.append({
            "domain": domain,
            "articles": len(subset),
            "avg_headline_len": round(avg_len, 1),
            "price_target_%": round(pct_price, 1),
            "upgrade_%": round(pct_upgrade, 1),
            "fda_%": round(pct_fda, 1),
        })
    
    result_df = pd.DataFrame(results).sort_values("articles", ascending=False)
    print("\n📊 Publisher Content Comparison (Top Domains):")
    print(result_df.to_string(index=False, float_format="{:.1f}".format))
    
    return result_df
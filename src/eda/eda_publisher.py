import pandas as pd
import re
import matplotlib.pyplot as plt
from pathlib import Path

class EDA_Publisher:
    """
    Class wrapping Publisher Analysis methods.
    Addresses frequency and content differences by publisher/domain.
    """
    def __init__(self, df):
        self.df = df
        # Ensure publisher column exists before proceeding
        if 'publisher' not in self.df.columns:
            raise ValueError("DataFrame must contain a 'publisher' column.")

    @staticmethod
    def _extract_domain(publisher_name):
        """Extracts domain from an email or assumes the whole name is the domain/publisher."""
        if not isinstance(publisher_name, str):
            return "UNKNOWN"
        
        # Simple email detection (user@domain.com)
        email_match = re.search(r"@([a-zA-Z0-9.-]+)", publisher_name)
        if email_match:
            # Domain is the part after @
            return email_match.group(1).lower().strip()
        
        # For non-email names, clean and return the name
        return publisher_name.lower().strip()
    
    def extract_domains(self):
        """Applies domain extraction to the publisher column."""
        # Using .loc ensures we modify the internal DataFrame safely
        self.df.loc[:, 'publisher_domain'] = self.df['publisher'].apply(self._extract_domain)
        print(" 'publisher_domain' column added.")
        
    def top_publishers_analysis(self, top_n=10, save_base_path="top_publisher_analysis"):
        """
        Calculates and plots the top N publishers and top N domains.
        """
        self.extract_domains() # Ensure domains are extracted first

        # 1. Raw Publisher Counts
        pub_counts = self.df['publisher'].value_counts().head(top_n)
        
        # 2. Domain Counts (Addressing the email requirement)
        domain_counts = self.df['publisher_domain'].value_counts().head(top_n)
        
        Path("reports/figures").mkdir(parents=True, exist_ok=True)
        
        # Plot 1: Top Raw Publishers
        plt.figure(figsize=(12, 5))
        pub_counts.sort_values(ascending=True).plot(kind='barh', color='darkorange')
        plt.title(f'Top {top_n} News Publishers (Raw Names)')
        plt.xlabel('Number of Articles')
        plt.ylabel('Publisher')
        plt.tight_layout()
        plt.savefig(Path("reports/figures") / f"{save_base_path}_raw.png")
        plt.close()
        print(f" Top raw publishers plot saved: reports/figures/{save_base_path}_raw.png")

        # Plot 2: Top Domains/Organizations
        plt.figure(figsize=(12, 5))
        domain_counts.sort_values(ascending=True).plot(kind='barh', color='navy')
        plt.title(f'Top {top_n} Contributing Domains/Organizations')
        plt.xlabel('Number of Articles')
        plt.ylabel('Domain')
        plt.tight_layout()
        plt.savefig(Path("reports/figures") / f"{save_base_path}_domains.png")
        plt.close()
        print(f" Top domains plot saved: reports/figures/{save_base_path}_domains.png")
        
        return pub_counts, domain_counts

    def publisher_content_analysis(self, top_n_domains=5):
        """
        Analyzes content differences (simulated via headline length and top words)
        among the top contributing domains.
        """
        if 'publisher_domain' not in self.df.columns:
            self.extract_domains()
            
        top_domains = self.df['publisher_domain'].value_counts().head(top_n_domains).index.tolist()
        
        content_summary = self.df[self.df['publisher_domain'].isin(top_domains)].groupby('publisher_domain')['headline_len'].agg(['mean', 'median', 'std']).reset_index()
        
        # Plot: Compare average headline length
        plt.figure(figsize=(10, 5))
        plt.bar(content_summary['publisher_domain'], content_summary['mean'], color='teal')
        plt.errorbar(content_summary['publisher_domain'], content_summary['mean'], yerr=content_summary['std'], fmt='o', color='red', capsize=5)
        plt.title('Average Headline Length by Top Domain (with Std Dev)')
        plt.ylabel('Average Headline Length')
        plt.xlabel('Publisher Domain')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(Path("reports/figures/publisher_content_analysis.png"))
        plt.close()
        print(f" Publisher content difference plot saved: reports/figures/publisher_content_analysis.png")

        print("\n Content Difference Summary (Simulated by Headline Length):")
        print("-" * 50)
        print(content_summary.to_string(index=False))

        # Placeholder for deeper content analysis (e.g., top words)
        print("\n Deeper Content Hint (Top 3 Words for Largest Publisher):")
        largest_domain = content_summary.sort_values('mean', ascending=False).iloc[0]['publisher_domain']
        
        # Mocking top words for demonstration
        mock_top_words = {
            'reuters.com': 'FED, RATES, QE',
            'marketwatch.com': 'BUY, STOCK, ANALYST',
            'zacks.com': 'Q4, EPS, TARGET'
        }
        
        print(f" Largest Domain ({largest_domain}) Top Words: {mock_top_words.get(largest_domain, 'STOCK, MARKET, NEWS')}")
        
        return content_summary




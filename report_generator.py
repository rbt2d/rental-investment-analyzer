"""Report generation and output formatting."""
import pandas as pd
import json
from typing import Dict
from tabulate import tabulate
from colorama import Fore, Style


class ReportGenerator:
    """Generates and formats analysis reports in various formats."""
    
    def print_summary(self, summary: Dict):
        """Print summary statistics to console."""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"ANALYSIS SUMMARY")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        if not summary:
            print("No summary data available")
            return
        
        print(f"  Total Zip Codes Analyzed: {Fore.GREEN}{summary.get('total_zipcodes_analyzed', 0)}{Style.RESET_ALL}")
        print(f"  Average Investment Score: {Fore.GREEN}{summary.get('avg_investment_score', 0):.2f}{Style.RESET_ALL}/100")
        print(f"  Average Population:       {Fore.GREEN}{summary.get('avg_population', 0):,.0f}{Style.RESET_ALL}")
        print(f"  Average Rental Ratio:     {Fore.GREEN}{summary.get('avg_rental_ratio', 0):.1%}{Style.RESET_ALL}")
        print(f"  Average Listings:         {Fore.GREEN}{summary.get('avg_listings', 0):.0f}{Style.RESET_ALL}")
        print(f"  Average Rent:             {Fore.GREEN}${summary.get('avg_rent', 0):,.0f}{Style.RESET_ALL}")
        
        if summary.get('top_zipcode'):
            print(f"\n  🏆 Top Zip Code: {Fore.YELLOW}{summary['top_zipcode']}{Style.RESET_ALL} " +
                  f"(Score: {Fore.GREEN}{summary['top_score']:.2f}{Style.RESET_ALL})")
        
        print()
    
    def print_top_zipcodes(self, df: pd.DataFrame, n: int = 10):
        """Print top N zip codes in formatted table."""
        if df.empty:
            print("No results to display")
            return
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"TOP {n} RENTAL INVESTMENT OPPORTUNITIES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        # Select columns for display
        display_cols = [
            'rank', 'zipcode', 'investment_score', 
            'total_population', 'renter_population', 'total_listings',
            'average_rent', 'supply_demand_ratio'
        ]
        
        # Get top N rows
        display_df = df.head(n)[display_cols].copy()
        
        # Format columns
        display_df['investment_score'] = display_df['investment_score'].round(2)
        display_df['total_population'] = display_df['total_population'].apply(lambda x: f"{x:,}")
        display_df['renter_population'] = display_df['renter_population'].apply(lambda x: f"{x:,}")
        display_df['average_rent'] = display_df['average_rent'].apply(lambda x: f"${x:,.0f}")
        display_df['supply_demand_ratio'] = display_df['supply_demand_ratio'].round(3)
        
        # Rename columns for display
        display_df.columns = [
            'Rank', 'ZIP', 'Score', 'Population', 
            'Renters', 'Listings', 'Avg Rent', 'Supply/Demand'
        ]
        
        # Print table
        print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
        print()
    
    def save_csv(self, df: pd.DataFrame, filename: str = 'rental_investment_report.csv') -> str:
        """Save results to CSV file."""
        df.to_csv(filename, index=False)
        return filename
    
    def save_json(self, df: pd.DataFrame, summary: Dict, filename: str = 'rental_investment_report.json') -> str:
        """Save results to JSON file."""
        output = {
            'summary': summary,
            'results': df.to_dict(orient='records')
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        return filename
    
    def save_excel(self, df: pd.DataFrame, summary: Dict, filename: str = 'rental_investment_report.xlsx') -> str:
        """Save results to Excel file with formatting."""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Write summary sheet
                summary_df = pd.DataFrame([summary])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Write results sheet
                df.to_excel(writer, sheet_name='Results', index=False)
            
            return filename
        except ImportError:
            print(f"{Fore.YELLOW}Warning: openpyxl not installed. Install with: pip install openpyxl{Style.RESET_ALL}")
            # Fallback to CSV
            return self.save_csv(df, filename.replace('.xlsx', '.csv'))
    
    def generate_detailed_report(self, df: pd.DataFrame) -> str:
        """Generate a detailed text report."""
        report = []
        report.append("RENTAL INVESTMENT ANALYSIS - DETAILED REPORT")
        report.append("=" * 80)
        report.append("")
        
        for idx, row in df.head(20).iterrows():
            report.append(f"RANK #{row['rank']}: ZIP CODE {row['zipcode']}")
            report.append("-" * 80)
            report.append(f"  Investment Score:      {row['investment_score']:.2f}/100")
            report.append(f"  Population Score:      {row['population_score']:.2f}/100")
            report.append(f"  Supply Score:          {row['supply_score']:.2f}/100")
            report.append(f"  Demand Score:          {row['demand_score']:.2f}/100")
            report.append("")
            report.append(f"  Total Population:      {row['total_population']:,}")
            report.append(f"  Renter Population:     {row['renter_population']:,}")
            report.append(f"  Rental Ratio:          {row['rental_ratio']:.1%}")
            report.append(f"  Median Income:         ${row['median_income']:,}")
            report.append("")
            report.append(f"  Total Listings:        {row['total_listings']}")
            report.append(f"  Average Rent:          ${row['average_rent']:,.0f}")
            report.append(f"  Supply/Demand Ratio:   {row['supply_demand_ratio']:.3f}")
            report.append(f"  Days on Market:        {row['days_on_market']}")
            report.append(f"  YoY Rental Growth:     {row['rental_growth_yoy']:.1%}")
            report.append("")
            report.append("")
        
        return "\n".join(report)



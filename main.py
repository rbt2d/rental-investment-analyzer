#!/usr/bin/env python3
"""
Rental Investment Analyzer - Main Application

A tool to identify high-potential rental investment zip codes by analyzing:
- Population density and demographics (Census data)
- Rental supply and demand metrics
- Market trends and growth indicators
"""

import argparse
import sys
import os
from typing import List
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from data_collectors.census_collector import CensusDataCollector
from data_collectors.rental_collector import RentalDataCollector
from analyzer import RentalInvestmentAnalyzer
from zipcode_generator import ZipCodeGenerator
from report_generator import ReportGenerator


def print_header():
    """Print application header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}   RENTAL INVESTMENT ANALYZER")
    print(f"{Fore.CYAN}   Find the Best Zip Codes for Rental Property Investment")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def validate_setup():
    """Validate that necessary APIs are configured."""
    print(f"{Fore.YELLOW}Validating configuration...{Style.RESET_ALL}")
    warnings = Config.validate()
    
    if warnings:
        print(f"\n{Fore.YELLOW}⚠ Configuration Warnings:{Style.RESET_ALL}")
        for warning in warnings:
            print(f"  • {warning}")
        print()
    else:
        print(f"{Fore.GREEN}✓ Configuration valid{Style.RESET_ALL}\n")
    
    return True


def get_zipcodes(args) -> List[str]:
    """Get list of zip codes to analyze based on arguments."""
    if args.zipcode_file:
        print(f"Loading zip codes from file: {args.zipcode_file}")
        if args.zipcode_file.endswith('.csv'):
            zipcodes = ZipCodeGenerator.load_zipcodes_from_csv(args.zipcode_file)
        else:
            zipcodes = ZipCodeGenerator.load_zipcodes_from_file(args.zipcode_file)
    elif args.metro:
        print(f"Loading zip codes for metro: {args.metro}")
        zipcodes = ZipCodeGenerator.get_metro_zipcodes(args.metro)
        if not zipcodes:
            print(f"{Fore.RED}Metro '{args.metro}' not found.{Style.RESET_ALL}")
            print(f"Available metros: {', '.join(ZipCodeGenerator.get_all_major_metros())}")
            sys.exit(1)
    elif args.zipcodes:
        zipcodes = [z.strip() for z in args.zipcodes.split(',')]
    else:
        print(f"Using sample zip codes from major metros")
        zipcodes = ZipCodeGenerator.get_sample_zipcodes(args.limit or 50)
    
    print(f"{Fore.GREEN}✓ Loaded {len(zipcodes)} zip codes for analysis{Style.RESET_ALL}\n")
    return zipcodes


def collect_data(zipcodes: List[str]) -> tuple:
    """Collect census and rental data for all zip codes."""
    print(f"{Fore.CYAN}Step 1: Collecting Census Data{Style.RESET_ALL}")
    census_collector = CensusDataCollector()
    
    census_data = {}
    for zipcode in tqdm(zipcodes, desc="Census data", ncols=70):
        data = census_collector._fetch_zipcode_data(zipcode)
        if data:
            census_data[zipcode] = data
    
    print(f"{Fore.GREEN}✓ Collected census data for {len(census_data)} zip codes{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Step 2: Collecting Rental Market Data{Style.RESET_ALL}")
    rental_collector = RentalDataCollector()
    
    rental_data = {}
    for zipcode in tqdm(zipcodes, desc="Rental data", ncols=70):
        data = rental_collector.get_rental_listings_count(zipcode)
        demand = rental_collector.get_rental_demand_metrics(zipcode)
        rental_data[zipcode] = {**data, **demand}
    
    print(f"{Fore.GREEN}✓ Collected rental data for {len(rental_data)} zip codes{Style.RESET_ALL}\n")
    
    return census_data, rental_data


def analyze_data(zipcodes: List[str], census_data: dict, rental_data: dict, args) -> tuple:
    """Analyze all zip codes and generate rankings."""
    print(f"{Fore.CYAN}Step 3: Analyzing Investment Opportunities{Style.RESET_ALL}")
    
    analyzer = RentalInvestmentAnalyzer()
    results = []
    
    for zipcode in tqdm(zipcodes, desc="Analyzing", ncols=70):
        if zipcode in census_data and zipcode in rental_data:
            analysis = analyzer.analyze_zipcode(
                zipcode, 
                census_data[zipcode], 
                rental_data[zipcode]
            )
            if analysis:
                results.append(analysis)
    
    print(f"{Fore.GREEN}✓ Analyzed {len(results)} zip codes{Style.RESET_ALL}\n")
    
    # Rank and filter results
    df = analyzer.rank_zipcodes(results, top_n=args.top or 50)
    
    # Apply filters if specified
    if args.min_population or args.max_listings or args.min_score:
        print(f"{Fore.CYAN}Applying filters...{Style.RESET_ALL}")
        df = analyzer.filter_by_criteria(
            df,
            min_population=args.min_population,
            max_listings=args.max_listings,
            min_score=args.min_score
        )
        print(f"{Fore.GREEN}✓ {len(df)} zip codes meet criteria{Style.RESET_ALL}\n")
    
    summary = analyzer.generate_summary_stats(df)
    
    return df, summary


def generate_output(df, summary, args):
    """Generate and save analysis report."""
    print(f"{Fore.CYAN}Step 4: Generating Report{Style.RESET_ALL}")
    
    report_gen = ReportGenerator()
    
    # Display summary in console
    report_gen.print_summary(summary)
    report_gen.print_top_zipcodes(df, n=min(10, len(df)))
    
    # Save to file
    output_file = args.output or "rental_investment_report"
    
    if args.format == 'csv':
        filepath = report_gen.save_csv(df, f"{output_file}.csv")
        print(f"\n{Fore.GREEN}✓ Report saved to: {filepath}{Style.RESET_ALL}")
    elif args.format == 'json':
        filepath = report_gen.save_json(df, summary, f"{output_file}.json")
        print(f"\n{Fore.GREEN}✓ Report saved to: {filepath}{Style.RESET_ALL}")
    elif args.format == 'excel':
        filepath = report_gen.save_excel(df, summary, f"{output_file}.xlsx")
        print(f"\n{Fore.GREEN}✓ Report saved to: {filepath}{Style.RESET_ALL}")
    else:
        # Save all formats
        csv_file = report_gen.save_csv(df, f"{output_file}.csv")
        json_file = report_gen.save_json(df, summary, f"{output_file}.json")
        print(f"\n{Fore.GREEN}✓ Reports saved:{Style.RESET_ALL}")
        print(f"  • {csv_file}")
        print(f"  • {json_file}")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze zip codes for rental investment opportunities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze specific zip codes
  python main.py --zipcodes "10001,10002,10003"
  
  # Analyze a metro area
  python main.py --metro NYC --top 20
  
  # Load zip codes from file
  python main.py --zipcode-file zipcodes.txt --format csv
  
  # Apply filters
  python main.py --metro Dallas --min-population 20000 --max-listings 300
  
Available metros: NYC, LA, Chicago, Houston, Phoenix, Dallas, Miami, Seattle, Boston, Austin
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--zipcodes', type=str,
                           help='Comma-separated list of zip codes')
    input_group.add_argument('--metro', type=str,
                           help='Metro area name (e.g., NYC, LA, Chicago)')
    input_group.add_argument('--zipcode-file', type=str,
                           help='Path to file with zip codes (txt or csv)')
    
    # Filter options
    parser.add_argument('--min-population', type=int,
                       help='Minimum population filter')
    parser.add_argument('--max-listings', type=int,
                       help='Maximum rental listings filter')
    parser.add_argument('--min-score', type=float,
                       help='Minimum investment score filter')
    
    # Output options
    parser.add_argument('--top', type=int, default=50,
                       help='Number of top results to return (default: 50)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of zip codes to analyze')
    parser.add_argument('--output', type=str,
                       help='Output filename (without extension)')
    parser.add_argument('--format', type=str, choices=['csv', 'json', 'excel', 'all'],
                       default='csv', help='Output format (default: csv)')
    
    # Other options
    parser.add_argument('--list-metros', action='store_true',
                       help='List available metro areas and exit')
    
    args = parser.parse_args()
    
    # Handle list metros
    if args.list_metros:
        print("\nAvailable Metro Areas:")
        for metro in ZipCodeGenerator.get_all_major_metros():
            count = len(ZipCodeGenerator.get_metro_zipcodes(metro))
            print(f"  • {metro:15} ({count} zip codes)")
        print()
        sys.exit(0)
    
    # Print header
    print_header()
    
    # Validate setup
    validate_setup()
    
    # Get zip codes to analyze
    zipcodes = get_zipcodes(args)
    
    if args.limit:
        zipcodes = zipcodes[:args.limit]
        print(f"Limited to {len(zipcodes)} zip codes\n")
    
    if not zipcodes:
        print(f"{Fore.RED}Error: No zip codes to analyze{Style.RESET_ALL}")
        sys.exit(1)
    
    # Collect data
    census_data, rental_data = collect_data(zipcodes)
    
    if not census_data or not rental_data:
        print(f"{Fore.RED}Error: Failed to collect sufficient data{Style.RESET_ALL}")
        sys.exit(1)
    
    # Analyze data
    df, summary = analyze_data(zipcodes, census_data, rental_data, args)
    
    if df.empty:
        print(f"{Fore.RED}Error: No results after analysis{Style.RESET_ALL}")
        sys.exit(1)
    
    # Generate output
    generate_output(df, summary, args)
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}Analysis Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Analysis interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



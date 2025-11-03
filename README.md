# Rental Investment Analyzer 🏠📊

A comprehensive tool to identify the best zip codes for rental property investment by analyzing population data, rental supply/demand, and market trends using legitimate data sources.

## 🎯 Features

- **Census Integration**: Uses official US Census API for demographic data
- **Rental Market Analysis**: Framework for integrating legitimate rental data APIs
- **Investment Scoring**: Sophisticated algorithm weighing multiple factors:
  - Population density and renter demographics
  - Rental supply shortage indicators
  - Market demand and growth trends
  - Economic factors (income, employment)
- **Flexible Analysis**: Analyze specific zip codes, metro areas, or custom lists
- **Multiple Output Formats**: CSV, JSON, and Excel reports
- **Command-Line Interface**: Easy-to-use CLI with filtering options

## 🚨 Important Legal Notice

**This tool DOES NOT scrape websites.** Scraping sites like Zillow, Redfin, and Realtor.com violates their Terms of Service and may be illegal.

Instead, this tool:
- ✅ Uses official Census Bureau API (free, legitimate)
- ✅ Provides framework for legitimate rental data APIs (RentCast, etc.)
- ✅ Includes demo data mode for testing
- ✅ Respects all API rate limits and terms of service

## 📋 Prerequisites

- Python 3.8 or higher
- US Census API key (free)
- Optional: RentCast or other rental data API keys (paid)

## 🚀 Installation

1. **Clone or download this repository**

```bash
cd rental_investment_analyzer
```

2. **Create a virtual environment (recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up API keys**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

### Getting a Census API Key (Required, Free)

1. Visit: https://api.census.gov/data/key_signup.html
2. Fill out the form with your name and email
3. You'll receive your API key via email instantly
4. Add it to `.env`: `CENSUS_API_KEY=your_key_here`

### Getting Rental Data API Keys (Optional, Paid)

For production use with real rental data, sign up for one or more:

- **RentCast** (Recommended): https://developers.rentcast.io/
  - Provides rental listings, market stats, vacancy rates
  - Plans start at $29/month
  
- **RealtyMole**: https://www.realtymole.com/api
  - Rental property data and estimates
  
- **Mashvisor**: https://www.mashvisor.com/api
  - Investment property analysis data

**Note**: Without rental API keys, the tool will use demo data for testing purposes.

## 💻 Usage

### Basic Examples

**Analyze specific zip codes:**
```bash
python main.py --zipcodes "10001,10002,10003,90210,94102"
```

**Analyze a metro area:**
```bash
python main.py --metro NYC --top 20
```

**Load zip codes from a file:**
```bash
python main.py --zipcode-file my_zipcodes.txt
```

**Apply filters:**
```bash
python main.py --metro Dallas --min-population 20000 --max-listings 300 --min-score 70
```

### Available Metro Areas

List all available metros:
```bash
python main.py --list-metros
```

Available metros: NYC, LA, Chicago, Houston, Phoenix, Dallas, Miami, Seattle, Boston, Austin

### Command-Line Options

**Input Options:**
- `--zipcodes`: Comma-separated list of zip codes
- `--metro`: Metro area name (NYC, LA, etc.)
- `--zipcode-file`: Path to file with zip codes (one per line or CSV)

**Filter Options:**
- `--min-population`: Minimum population threshold
- `--max-listings`: Maximum number of rental listings
- `--min-score`: Minimum investment score (0-100)

**Output Options:**
- `--top`: Number of top results (default: 50)
- `--limit`: Limit total zip codes analyzed
- `--output`: Output filename (without extension)
- `--format`: Output format (csv, json, excel, or all)

### Advanced Examples

**Analyze top 100 zip codes in Texas metros with filters:**
```bash
python main.py --metro Houston --limit 100 --min-population 15000 --max-listings 250 --format all
```

**Custom zip code list with Excel output:**
```bash
python main.py --zipcode-file targets.csv --output my_analysis --format excel
```

## 📊 Understanding the Results

### Investment Score (0-100)

The investment score weighs three key factors:

1. **Population Score (30%)**: Higher population = more potential renters
2. **Supply Score (35%)**: Fewer listings relative to renters = tighter market
3. **Demand Score (35%)**: Market trends, growth, and demand indicators

**Score Interpretation:**
- 80-100: Excellent investment opportunity
- 60-80: Good opportunity, worth investigating
- 40-60: Moderate opportunity
- Below 40: Limited opportunity

### Key Metrics Explained

- **Rental Ratio**: Percentage of renter vs. owner households
- **Supply/Demand Ratio**: Available listings per renter household (lower is better)
- **Days on Market**: Average time rentals stay listed (lower = higher demand)
- **YoY Rental Growth**: Year-over-year rent increase (positive is good)

## 📁 Output Files

### CSV Format
Simple spreadsheet with all metrics for further analysis in Excel or Google Sheets.

### JSON Format
Structured data including summary statistics and detailed results, ideal for:
- Integration with other tools
- Building dashboards
- Further programmatic analysis

### Excel Format
Formatted workbook with:
- Summary sheet: Key statistics
- Results sheet: Detailed zip code data

## 🔧 Customization

### Adding Custom Zip Codes

Create a text file with one zip code per line:
```
10001
10002
10003
```

Or use a CSV file with a 'zipcode' column.

### Adjusting Scoring Weights

Edit `config.py` to change scoring weights:

```python
POPULATION_WEIGHT = 0.30
RENTAL_DEMAND_WEIGHT = 0.35
SUPPLY_SHORTAGE_WEIGHT = 0.35
```

### Adding New Data Sources

The architecture supports adding new data collectors:

1. Create a new collector in `data_collectors/`
2. Implement data fetching methods
3. Add API key to `config.py`
4. Update `main.py` to use new collector

## 🏗️ Project Structure

```
rental_investment_analyzer/
├── main.py                    # Main application
├── config.py                  # Configuration and API keys
├── analyzer.py                # Investment scoring algorithm
├── zipcode_generator.py       # Zip code list management
├── report_generator.py        # Output formatting and reports
├── requirements.txt           # Python dependencies
├── .env                       # API keys (create from .env.example)
├── .env.example              # Environment template
└── data_collectors/
    ├── census_collector.py   # Census API integration
    └── rental_collector.py   # Rental data API framework
```

## 🎓 Methodology

This tool identifies investment opportunities by finding markets with:

1. **High Population Density**: More potential renters
2. **Strong Renter Demographics**: High percentage of renters vs. owners
3. **Limited Supply**: Fewer available listings relative to demand
4. **High Demand Indicators**: 
   - Low days on market
   - Positive rental growth
   - High search volume
5. **Economic Viability**: Median income supporting rent levels

## ⚠️ Limitations & Disclaimers

- **Demo Data Mode**: Without API keys, the tool uses simulated data for demonstration
- **Data Freshness**: Census data updates annually; rental market data frequency depends on API
- **Not Financial Advice**: This tool provides analytical data only, not investment advice
- **Market Changes**: Real estate markets change rapidly; always verify current conditions
- **Local Factors**: Many local factors (regulations, schools, crime) aren't captured

## 🤝 Contributing

To add new features or data sources:

1. Ensure all data sources use legitimate APIs (no scraping)
2. Follow existing code structure
3. Add appropriate error handling
4. Update documentation

## 📝 License

This project is for educational and analytical purposes. Users are responsible for:
- Obtaining their own API keys
- Following all API terms of service
- Making their own investment decisions

## 🆘 Support & Troubleshooting

### Common Issues

**"Census API key not found"**
- Make sure you've created `.env` file from `.env.example`
- Verify your Census API key is correct
- Check that `.env` is in the same directory as `main.py`

**"No rental data API keys configured"**
- This is a warning, not an error
- Tool will use demo data without rental API keys
- Sign up for RentCast or similar service for real data

**Import errors**
- Ensure you've activated your virtual environment
- Run `pip install -r requirements.txt` again

**Slow performance**
- Census API has rate limits
- Use `--limit` to analyze fewer zip codes initially
- Consider analyzing one metro at a time

## 🔮 Future Enhancements

Potential additions:
- Property price data integration
- School district ratings
- Crime statistics
- Walk score / transit data
- ROI calculator
- Historical trend analysis
- Predictive modeling

## 📧 Questions?

For questions about:
- **Census API**: https://www.census.gov/data/developers/guidance.html
- **RentCast API**: https://developers.rentcast.io/docs
- **This Tool**: Check the code comments and docstrings

---

**Happy Investing! 🏠💰**

Remember: Always conduct thorough due diligence before making any investment decisions.



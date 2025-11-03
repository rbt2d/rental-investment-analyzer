# Quick Start Guide 🚀

Get up and running with Rental Investment Analyzer in 5 minutes!

## Step 1: Install (2 minutes)

```bash
cd rental_investment_analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Get Census API Key (2 minutes)

1. Go to: https://api.census.gov/data/key_signup.html
2. Enter your name and email
3. Check your email for the API key
4. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
5. Edit `.env` and paste your key:
   ```
   CENSUS_API_KEY=your_actual_key_here
   ```

## Step 3: Run Your First Analysis (1 minute)

### Option A: Analyze a Metro Area
```bash
python main.py --metro NYC --top 10
```

### Option B: Analyze Specific Zip Codes
```bash
python main.py --zipcodes "10001,90210,60601,77001,33101"
```

### Option C: Quick Test Run
```bash
python main.py --metro Austin --limit 10 --top 5
```

## That's It! 🎉

You'll see:
1. Progress bars as data is collected
2. Analysis summary statistics
3. Top investment opportunities table
4. A CSV file with detailed results

## What's Next?

### Get Better Data (Optional but Recommended)

For real rental market data instead of demo data:

1. **Sign up for RentCast** (recommended): https://developers.rentcast.io/
   - Get your API key
   - Add to `.env`: `RENTCAST_API_KEY=your_key`
   - Plans start at $29/month

### Run Advanced Analysis

```bash
# Filter for high-population, low-supply markets
python main.py --metro LA --min-population 30000 --max-listings 200 --min-score 70

# Export to Excel for detailed analysis
python main.py --metro Chicago --format excel --output chicago_analysis

# Analyze multiple metros (save each separately)
python main.py --metro NYC --output nyc_report
python main.py --metro Miami --output miami_report
python main.py --metro Austin --output austin_report
```

### Use Your Own Zip Code List

Create `my_zipcodes.txt`:
```
10001
10002
10003
```

Then run:
```bash
python main.py --zipcode-file my_zipcodes.txt
```

## Understanding Your Results

**Investment Score**: 0-100 score (higher is better)
- 80+: Excellent opportunity ⭐⭐⭐
- 60-80: Good opportunity ⭐⭐
- 40-60: Moderate opportunity ⭐
- <40: Limited opportunity

**Key Metrics to Look For**:
- High population with high renter percentage
- Low supply/demand ratio (fewer listings per renter)
- Low days on market (fast-moving rentals)
- Positive rental growth year-over-year

## Troubleshooting

**"Census API key not found"**
- Did you create `.env` file?
- Is your API key in quotes?

**"No zip codes to analyze"**
- Check your metro name (use `--list-metros` to see options)
- Verify your zip code file exists and has valid zip codes

**Running slow?**
- Use `--limit 20` to test with fewer zip codes
- Census API has rate limits (it's free after all!)

## Tips for Best Results

1. **Start Small**: Test with `--limit 10` first
2. **Use Filters**: Focus on markets that meet your criteria
3. **Compare Metros**: Run separate analyses for different cities
4. **Verify Data**: Always cross-check high-scoring markets with local research
5. **Update Regularly**: Real estate markets change—rerun analysis quarterly

## Need Help?

- Run `python main.py --help` for all options
- Check `README.md` for detailed documentation
- Review sample outputs to understand the data

---

**Ready to find your next rental investment? Let's go! 🏠💰**



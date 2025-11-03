# API Setup Guide for Real Data 🔑

This guide helps you set up legitimate data sources for production use of the Rental Investment Analyzer.

## Overview

Without API keys, the tool works with demo data. To get real market data, you need:
1. **Census API** (Required, Free) - Population and demographic data
2. **Rental Data API** (Optional, Paid) - Real rental listings and market data

## 1. Census API Setup (FREE) ⭐

### Why You Need It
- Real population data by zip code
- Demographics (renters vs owners)
- Median income statistics
- Updated annually

### How to Get Your Free API Key

**Step 1:** Visit the Census API signup page
```
https://api.census.gov/data/key_signup.html
```

**Step 2:** Fill out the form
- Organization name: Your name or company
- Email: Your email address
- Click "Submit"

**Step 3:** Check your email
- You'll receive your API key instantly
- It looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`

**Step 4:** Add to your .env file
```bash
CENSUS_API_KEY=your_actual_key_here
```

### Testing Your Census API Key

Run this curl command to test:
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01003_001E&for=zip%20code%20tabulation%20area:10001&key=YOUR_KEY_HERE"
```

You should see population data for zip 10001.

## 2. Rental Data APIs (PAID) 💰

### Option A: RentCast (RECOMMENDED)

**Best For:** Comprehensive rental market data

**Features:**
- Rental listings count
- Average/median rent
- Vacancy rates
- Market trends
- Days on market

**Pricing:**
- Starter: $29/month (500 calls/month)
- Professional: $79/month (2,000 calls/month)
- Business: $199/month (10,000 calls/month)

**Setup:**
1. Visit: https://developers.rentcast.io/
2. Sign up for an account
3. Subscribe to a plan
4. Get your API key from dashboard
5. Add to `.env`:
   ```bash
   RENTCAST_API_KEY=your_rentcast_key_here
   ```

**Documentation:**
- API Docs: https://developers.rentcast.io/reference/getting-started
- Endpoints used:
  - `/v1/markets` - Market statistics by zip code
  - `/v1/listings` - Rental listings

---

### Option B: RealtyMole Property Data API

**Best For:** Property valuations and rental estimates

**Features:**
- Rental estimates
- Property values
- Market comparables

**Pricing:**
- Basic: $50/month (500 requests)
- Premium: $150/month (2,000 requests)

**Setup:**
1. Visit: https://www.realtymole.com/api
2. Create account and subscribe
3. Get API key
4. Add to `.env`:
   ```bash
   REALTOR_API_KEY=your_realtymole_key_here
   ```

---

### Option C: Mashvisor API

**Best For:** Investment analysis data

**Features:**
- Rental income estimates
- Occupancy rates
- Cash flow projections
- Neighborhood data

**Pricing:**
- Basic: $49/month
- Pro: $99/month
- Custom plans available

**Setup:**
1. Visit: https://www.mashvisor.com/api
2. Sign up for account
3. Subscribe to plan
4. Get API credentials
5. Add to `.env` (Note: Mashvisor may require OAuth)

---

### Option D: Zillow Research Data (FREE, Limited)

**Note:** Zillow's public API is discontinued, but they offer free research data downloads.

**Features:**
- Historical rent data
- Zip code level aggregates
- Monthly updates

**Setup:**
1. Visit: https://www.zillow.com/research/data/
2. Download rental data CSV files
3. No API key needed - use downloaded files

**Integration:**
- You'll need to modify the code to read CSV files instead of API calls
- Good for historical analysis but not real-time data

---

## 3. Additional Data Sources

### HUD (U.S. Department of Housing) - FREE

**What it offers:**
- Fair Market Rents by zip code
- Housing affordability data
- Section 8 data

**Setup:**
```bash
# No API key needed for basic data
# Access: https://www.huduser.gov/portal/datasets/fmr.html
```

### BLS (Bureau of Labor Statistics) - FREE

**What it offers:**
- Employment data by metro area
- Wage statistics
- Economic indicators

**Setup:**
1. Register: https://data.bls.gov/registrationEngine/
2. Get API key
3. Add to `.env`:
   ```bash
   BLS_API_KEY=your_bls_key_here
   ```

---

## Complete .env File Example

Here's what your `.env` should look like with all keys:

```bash
# Required: Census API (FREE)
CENSUS_API_KEY=abc123def456ghi789jkl012mno345pqr678stu

# Optional: Rental Data APIs (choose one or more)
RENTCAST_API_KEY=rentcast_123456789abcdef
REALTOR_API_KEY=realtor_abcdef123456789
REDFIN_API_KEY=redfin_xyz789abc123

# Optional: Additional Data
BLS_API_KEY=bls_economic_data_key_123

# Configuration
MIN_POPULATION=10000
MAX_RENTAL_LISTINGS=500
OUTPUT_FORMAT=csv
```

## Usage After Setup

Once you have your API keys configured:

### Test with real data:
```bash
python main.py --zipcodes "10001,10002" --limit 2
```

### Run full analysis:
```bash
python main.py --metro NYC --top 20 --format excel
```

### The output will show:
- `data_quality: high` (instead of "demo")
- Real census numbers
- Actual rental listings count
- Current market rents
- Accurate vacancy rates

## Rate Limits & Best Practices

### Census API
- **Rate Limit:** 500 calls per IP per day
- **Tip:** Cache results, run analysis in batches

### RentCast API
- **Rate Limit:** Depends on plan
- **Tip:** Use their bulk endpoints when available

### General Tips
1. **Start small:** Test with `--limit 10` first
2. **Cache results:** Save intermediate data
3. **Run off-peak:** API calls are faster during off-peak hours
4. **Monitor usage:** Track your API usage to avoid overages
5. **Batch processing:** Analyze one metro at a time

## Costs Breakdown

### Minimal Setup (FREE)
- Census API: $0
- Demo rental data: $0
- **Total: $0/month**
- Good for: Learning, testing, basic analysis

### Recommended Setup ($29/month)
- Census API: $0
- RentCast Starter: $29/month
- **Total: $29/month**
- Good for: Analyzing 1-2 metros per week

### Professional Setup ($79-150/month)
- Census API: $0
- RentCast Professional: $79/month
- Optional: BLS API $0
- **Total: $79/month**
- Good for: Regular analysis, multiple metros, research

### Enterprise Setup ($200+/month)
- Census API: $0
- RentCast Business: $199/month
- RealtyMole Premium: $150/month
- **Total: $349/month**
- Good for: Daily analysis, nationwide coverage, business use

## Troubleshooting

### "Census API key not found"
- Make sure `.env` file exists
- Check the key name is exactly: `CENSUS_API_KEY`
- No quotes needed around the key
- File must be in same directory as `main.py`

### "API rate limit exceeded"
- Wait a few minutes and try again
- Reduce the number of zip codes analyzed
- Use `--limit` flag to process fewer at a time

### "Invalid API key"
- Double-check you copied the entire key
- Make sure there are no spaces or quotes
- Verify the key is active (check provider dashboard)

### "No rental data"
- This is normal without rental API keys
- Tool will use demo data
- To get real data, sign up for RentCast or similar

## Need Help?

- **Census API Issues:** https://www.census.gov/data/developers/guidance.html
- **RentCast Support:** support@rentcast.io
- **Tool Issues:** Check README.md and QUICKSTART.md

---

## Security Best Practices

1. **Never commit .env file to git** (it's in .gitignore)
2. **Never share your API keys publicly**
3. **Rotate keys periodically**
4. **Use read-only keys when available**
5. **Monitor your usage for suspicious activity**

---

**Ready to get started?**

1. Get your free Census API key (5 minutes)
2. Test the tool with demo data
3. If you like the results, sign up for RentCast
4. Run your first real analysis!

Happy investing! 🏠💰



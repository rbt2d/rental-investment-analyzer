# Investment Scoring Methodology 📊

This document explains how the Rental Investment Analyzer evaluates and scores zip codes for rental property investment potential.

## Overview

The analyzer uses a **multi-factor scoring system** that combines:
1. Population demographics
2. Rental supply metrics
3. Market demand indicators

Each factor is scored 0-100, then combined into a weighted composite score.

## Composite Investment Score Formula

```
Investment Score = (Population Score × 30%) + 
                  (Supply Score × 35%) + 
                  (Demand Score × 35%)
```

**Why these weights?**
- **Supply (35%)**: Scarcity drives value; limited supply is crucial
- **Demand (35%)**: Active demand ensures consistent occupancy
- **Population (30%)**: Large renter base provides market depth

You can adjust these in `config.py`.

---

## 1. Population Score (Weight: 30%)

**What it measures:** The size and composition of the potential renter pool

### Components

#### A. Total Population (Primary Factor)

Optimal range scoring:
- **Below 5,000**: Proportional score (0-30 points)
  - `Score = (Population / 5,000) × 30`
- **5,000 - 50,000**: Growth phase (30-80 points)
  - `Score = 30 + ((Pop - 5,000) / 45,000) × 50`
- **Above 50,000**: Mature market (80-100 points)
  - `Score = 80 + min((Pop - 50,000) / 100,000 × 20, 20)`

**Rationale:**
- Very small markets (< 5k) are risky
- Sweet spot: 10k-100k population
- Large markets (> 100k) are stable but competitive

#### B. Renter Percentage (Bonus)

Adds up to 20 bonus points based on renter ratio:
```
Renter Ratio = Renter-Occupied / Total Occupied Households
Bonus = Renter Ratio × 20 points
```

**Example:**
- 60% renters → +12 points
- 80% renters → +16 points

**Why it matters:** Higher renter percentage = larger target market

### Scoring Examples

| Population | Renters | Owner | Ratio | Base Score | Bonus | Final |
|-----------|---------|-------|-------|------------|-------|-------|
| 10,000    | 6,000   | 4,000 | 60%   | 35         | 12    | 47    |
| 50,000    | 40,000  | 10,000| 80%   | 80         | 16    | 96    |
| 100,000   | 30,000  | 70,000| 30%   | 90         | 6     | 96    |

---

## 2. Supply Score (Weight: 35%)

**What it measures:** How tight the rental market is (lower supply = higher score)

### Calculation Method

Uses **Listings per 100 Renters** as key metric:
```
Listings per 100 = (Total Listings / Renter Households) × 100
```

### Scoring Tiers

| Listings per 100 | Interpretation | Score Formula | Score Range |
|------------------|----------------|---------------|-------------|
| < 1              | Severe shortage| 100           | 100         |
| 1-3              | Tight market   | 90 - (ratio-1)×20 | 70-90   |
| 3-5              | Balanced       | 70 - (ratio-3)×15 | 40-70   |
| 5-10             | Loose market   | 40 - (ratio-5)×5  | 15-40   |
| > 10             | Oversupply     | max(10-ratio,0)| 0-15    |

**Rationale:**
- **< 1%**: Extreme shortage, very favorable
- **1-3%**: Healthy tight market
- **3-5%**: Balanced market
- **> 5%**: Too much supply, unfavorable

### Real-World Examples

**Tight Market (High Score):**
- 20,000 renters
- 250 listings
- Ratio: 1.25 per 100
- Score: 88 ✅

**Balanced Market (Medium Score):**
- 20,000 renters
- 800 listings
- Ratio: 4 per 100
- Score: 55 ⚠️

**Oversupplied Market (Low Score):**
- 20,000 renters
- 3,000 listings
- Ratio: 15 per 100
- Score: 5 ❌

---

## 3. Demand Score (Weight: 35%)

**What it measures:** Active market demand and growth trends

### Four Demand Indicators (Averaged)

#### A. Days on Market Score (Weight: 25%)

Lower is better - indicates high demand:

| Days on Market | Market Condition | Score |
|---------------|------------------|-------|
| < 10 days     | Very hot         | 100   |
| 10-20 days    | Hot              | 60-90 |
| 20-40 days    | Normal           | 20-60 |
| > 40 days     | Slow             | 0-20  |

**Formula:**
```python
if days < 10:
    score = 100
elif days < 20:
    score = 90 - (days - 10) × 3
elif days < 40:
    score = 60 - (days - 20) × 2
else:
    score = max(20 - (days - 40), 0)
```

#### B. Rental Growth Score (Weight: 25%)

Year-over-year rent growth:

| YoY Growth | Interpretation | Score |
|-----------|----------------|-------|
| 0-15%     | Healthy growth | 50-100|
| > 15%     | Hot market     | 100   |
| < 0%      | Declining      | 0-50  |

**Formula:**
```python
if -5% <= growth <= 15%:
    score = 50 + (growth × 333)  # Linear scaling
elif growth > 15%:
    score = 100
else:
    score = max(50 + (growth × 500), 0)
```

**Why cap at 15%?**
- Extremely high growth (>20%) may indicate bubble
- Sustainable growth is better long-term

#### C. Search Volume Index (Weight: 25%)

Relative search interest (0-100 scale):
```
Score = min(search_volume_index, 100)
```

This would ideally come from:
- Google Trends data for rental searches
- Zillow/Redfin view counts
- Rental site traffic data

#### D. Direct Demand Score (Weight: 25%)

If available from data provider:
```
Score = demand_score × 100
```

This may include:
- Application rates
- Inquiry volume
- Showing requests
- Rental price trends

### Demand Score Calculation

```python
demand_score = (days_on_market_score + 
                growth_score + 
                search_score + 
                direct_demand_score) / 4
```

### Example Scenarios

**High Demand Market:**
- Days on market: 12 days → Score: 84
- YoY growth: 8% → Score: 77
- Search volume: 85 → Score: 85
- Direct demand: 0.9 → Score: 90
- **Average: 84** ⭐⭐⭐

**Moderate Demand Market:**
- Days on market: 25 days → Score: 50
- YoY growth: 3% → Score: 60
- Search volume: 55 → Score: 55
- Direct demand: 0.6 → Score: 60
- **Average: 56** ⭐⭐

**Low Demand Market:**
- Days on market: 50 days → Score: 10
- YoY growth: -2% → Score: 40
- Search volume: 30 → Score: 30
- Direct demand: 0.3 → Score: 30
- **Average: 27** ⭐

---

## Final Investment Score Interpretation

### Score Ranges

| Score | Rating | Interpretation | Action |
|-------|--------|----------------|--------|
| 80-100| ⭐⭐⭐⭐⭐ | Excellent | Strong buy signal, investigate immediately |
| 70-80 | ⭐⭐⭐⭐ | Very Good | Good opportunity, worth detailed analysis |
| 60-70 | ⭐⭐⭐ | Good | Moderate opportunity, proceed with caution |
| 50-60 | ⭐⭐ | Fair | Marginal opportunity, high due diligence |
| 40-50 | ⭐ | Poor | Limited opportunity, likely pass |
| < 40  | ❌ | Very Poor | Avoid |

### What Makes a Top-Scoring Zip Code?

**Perfect 90+ Score Example:**
```
ZIP: 12345
├─ Population Score: 95/100
│  ├─ 75,000 total population
│  └─ 75% renters (high ratio)
├─ Supply Score: 92/100
│  ├─ 600 listings
│  └─ 1.1 per 100 renters (tight market)
└─ Demand Score: 85/100
   ├─ 8 days on market (very fast)
   ├─ 10% YoY rent growth (strong)
   ├─ High search volume
   └─ Growing economy

Investment Score: (95×0.3) + (92×0.35) + (85×0.35) = 90.45
```

**Why it scores high:**
- Large renter population
- Very limited supply
- Strong demand indicators
- Sustainable growth

---

## Additional Metrics (Not in Score)

### Supporting Data Points

While these don't directly affect the score, they provide context:

#### Median Income
- Higher income = ability to pay higher rents
- Look for income 3x the average rent

#### Rental Ratio
- Percentage of renters vs owners
- Higher = better rental culture

#### Supply/Demand Ratio
- Direct measure of market tightness
- Lower = better for landlords

#### Rental Growth YoY
- Positive = growing market
- 5-10% is ideal sustainable growth

---

## Limitations & Considerations

### What This Model DOESN'T Capture

1. **Property Prices:** High scores may have high entry costs
2. **Local Regulations:** Rent control, tenant laws vary
3. **Property Taxes:** Significant impact on ROI
4. **Insurance Costs:** Vary by location
5. **Natural Disasters:** Hurricane, flood, earthquake zones
6. **School Districts:** Major factor for families
7. **Crime Rates:** Safety impacts demand
8. **Employment:** Job growth drives rental demand
9. **Development Pipeline:** New construction affects supply
10. **Neighborhood Trends:** Gentrification, decline

### How to Use These Scores

✅ **DO:**
- Use as initial screening tool
- Identify markets for deeper research
- Compare similar markets
- Track changes over time
- Combine with local knowledge

❌ **DON'T:**
- Make investment decisions solely on score
- Ignore property-specific factors
- Skip boots-on-the-ground research
- Forget about exit strategy
- Overlook financing implications

---

## Customizing the Methodology

### Adjust Scoring Weights

Edit `config.py`:
```python
# Default weights
POPULATION_WEIGHT = 0.30
RENTAL_DEMAND_WEIGHT = 0.35
SUPPLY_SHORTAGE_WEIGHT = 0.35

# Example: Emphasize supply over population
POPULATION_WEIGHT = 0.20
SUPPLY_SHORTAGE_WEIGHT = 0.45
RENTAL_DEMAND_WEIGHT = 0.35
```

### Modify Scoring Functions

Edit `analyzer.py` methods:
- `_calculate_population_score()`
- `_calculate_supply_score()`
- `_calculate_demand_score()`

You can adjust:
- Optimal population ranges
- Supply ratio thresholds
- Growth rate preferences
- Days on market targets

---

## Validation & Backtesting

To validate the scoring methodology:

1. **Historical Analysis:** Score past markets and compare to actual performance
2. **Expert Review:** Have local real estate experts review top-scoring areas
3. **Portfolio Correlation:** Compare scores to your portfolio performance
4. **Market Feedback:** Track if high-scoring areas actually perform well

---

## References & Further Reading

- U.S. Census Bureau: https://www.census.gov/
- HUD Fair Market Rents: https://www.huduser.gov/
- NAR Research: https://www.nar.realtor/research-and-statistics
- NMHC Rent Tracker: https://www.nmhc.org/
- CoStar Market Research: https://www.costar.com/

---

**Remember:** This tool provides data-driven insights, but successful real estate investing requires:
- Local market knowledge
- Property-specific analysis
- Financial due diligence
- Risk assessment
- Long-term strategy

Use these scores as a starting point, not an ending point! 🎯



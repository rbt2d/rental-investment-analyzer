"""Rental investment analysis and scoring engine."""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from config import Config


class RentalInvestmentAnalyzer:
    """
    Analyzes zip codes for rental investment opportunities.
    
    Scoring methodology:
    1. High population (more potential renters)
    2. Low rental supply (fewer listings = higher demand)
    3. High rental demand indicators (search volume, growth)
    4. Economic factors (income levels, employment)
    """
    
    def __init__(self):
        """Initialize analyzer with scoring weights from config."""
        self.pop_weight = Config.POPULATION_WEIGHT
        self.demand_weight = Config.RENTAL_DEMAND_WEIGHT
        self.supply_weight = Config.SUPPLY_SHORTAGE_WEIGHT
    
    def analyze_zipcode(self, zipcode: str, census_data: Dict, rental_data: Dict) -> Dict:
        """
        Analyze a single zip code for investment potential.
        
        Args:
            zipcode: ZIP code string
            census_data: Population and demographic data
            rental_data: Rental listing and demand data
            
        Returns:
            Dictionary with investment scores and metrics
        """
        if not census_data or not rental_data:
            return None
        
        # Calculate individual scores
        population_score = self._calculate_population_score(census_data)
        supply_score = self._calculate_supply_score(rental_data, census_data)
        demand_score = self._calculate_demand_score(rental_data)
        
        # Calculate composite investment score (0-100)
        investment_score = (
            population_score * self.pop_weight +
            supply_score * self.supply_weight +
            demand_score * self.demand_weight
        )
        
        # Calculate additional metrics
        rental_ratio = self._calculate_rental_ratio(census_data)
        supply_demand_ratio = self._calculate_supply_demand_ratio(rental_data, census_data)
        
        return {
            'zipcode': zipcode,
            'investment_score': round(investment_score, 2),
            'population_score': round(population_score, 2),
            'supply_score': round(supply_score, 2),
            'demand_score': round(demand_score, 2),
            'total_population': census_data.get('total_population', 0),
            'renter_population': census_data.get('renter_occupied', 0),
            'rental_ratio': round(rental_ratio, 3),
            'total_listings': rental_data.get('total_listings', 0),
            'average_rent': rental_data.get('average_rent', 0),
            'median_income': census_data.get('median_income', 0),
            'supply_demand_ratio': round(supply_demand_ratio, 3),
            'rental_growth_yoy': rental_data.get('rental_growth_yoy', 0),
            'days_on_market': rental_data.get('avg_days_on_market', 0),
            'data_quality': self._assess_data_quality(census_data, rental_data)
        }
    
    def _calculate_population_score(self, census_data: Dict) -> float:
        """
        Calculate score based on population metrics.
        Higher population = more potential renters = higher score.
        """
        total_pop = census_data.get('total_population', 0)
        renter_pop = census_data.get('renter_occupied', 0)
        
        # Normalize population (higher is better, up to a point)
        # Optimal range: 10,000 - 100,000
        if total_pop < 5000:
            pop_score = total_pop / 5000 * 30
        elif total_pop < 50000:
            pop_score = 30 + ((total_pop - 5000) / 45000 * 50)
        else:
            pop_score = 80 + min((total_pop - 50000) / 100000 * 20, 20)
        
        # Bonus for high renter percentage
        if total_pop > 0:
            renter_ratio = renter_pop / (renter_pop + census_data.get('owner_occupied', 1))
            renter_bonus = renter_ratio * 20
            pop_score = min(pop_score + renter_bonus, 100)
        
        return pop_score
    
    def _calculate_supply_score(self, rental_data: Dict, census_data: Dict) -> float:
        """
        Calculate score based on rental supply shortage.
        Lower supply relative to demand = higher score.
        """
        total_listings = rental_data.get('total_listings', 0)
        renter_pop = census_data.get('renter_occupied', 1)  # Avoid division by zero
        
        if renter_pop == 0:
            return 0
        
        # Calculate listings per 100 renters
        listings_per_100 = (total_listings / renter_pop) * 100
        
        # Optimal ratio: 1-3 listings per 100 renters (tight market)
        if listings_per_100 < 1:
            supply_score = 100
        elif listings_per_100 < 3:
            supply_score = 90 - ((listings_per_100 - 1) * 20)
        elif listings_per_100 < 5:
            supply_score = 70 - ((listings_per_100 - 3) * 15)
        elif listings_per_100 < 10:
            supply_score = 40 - ((listings_per_100 - 5) * 5)
        else:
            supply_score = max(10 - (listings_per_100 - 10), 0)
        
        return supply_score
    
    def _calculate_demand_score(self, rental_data: Dict) -> float:
        """
        Calculate score based on rental demand indicators.
        High demand signals = higher score.
        """
        demand_indicators = []
        
        # 1. Days on market (lower is better)
        days_on_market = rental_data.get('avg_days_on_market', 30)
        if days_on_market < 10:
            dom_score = 100
        elif days_on_market < 20:
            dom_score = 90 - ((days_on_market - 10) * 3)
        elif days_on_market < 40:
            dom_score = 60 - ((days_on_market - 20) * 2)
        else:
            dom_score = max(20 - (days_on_market - 40), 0)
        demand_indicators.append(dom_score)
        
        # 2. Rental growth (higher is better, but not too extreme)
        growth_yoy = rental_data.get('rental_growth_yoy', 0)
        if -0.05 <= growth_yoy <= 0.15:  # 0% to 15% is healthy
            growth_score = 50 + (growth_yoy * 333)
        elif growth_yoy > 0.15:
            growth_score = 100
        else:
            growth_score = max(50 + (growth_yoy * 500), 0)
        demand_indicators.append(growth_score)
        
        # 3. Search volume index
        search_volume = rental_data.get('search_volume_index', 50)
        search_score = min(search_volume, 100)
        demand_indicators.append(search_score)
        
        # 4. Direct demand score from data source
        if 'demand_score' in rental_data:
            demand_indicators.append(rental_data['demand_score'] * 100)
        
        return np.mean(demand_indicators)
    
    def _calculate_rental_ratio(self, census_data: Dict) -> float:
        """Calculate percentage of renter-occupied households."""
        renter = census_data.get('renter_occupied', 0)
        owner = census_data.get('owner_occupied', 0)
        
        if renter + owner == 0:
            return 0
        
        return renter / (renter + owner)
    
    def _calculate_supply_demand_ratio(self, rental_data: Dict, census_data: Dict) -> float:
        """Calculate ratio of available listings to renter households."""
        listings = rental_data.get('total_listings', 0)
        renters = census_data.get('renter_occupied', 1)
        
        return listings / renters
    
    def _assess_data_quality(self, census_data: Dict, rental_data: Dict) -> str:
        """Assess the quality and source of data."""
        data_source = rental_data.get('data_source', 'unknown')
        
        if data_source == 'demo_data':
            return 'demo'
        elif data_source in ['rentcast', 'zillow', 'realtor']:
            return 'high'
        else:
            return 'medium'
    
    def rank_zipcodes(self, analysis_results: List[Dict], top_n: int = 50) -> pd.DataFrame:
        """
        Rank zip codes by investment score.
        
        Args:
            analysis_results: List of analysis dictionaries
            top_n: Number of top results to return
            
        Returns:
            DataFrame sorted by investment score
        """
        df = pd.DataFrame(analysis_results)
        
        if df.empty:
            return df
        
        # Sort by investment score
        df = df.sort_values('investment_score', ascending=False)
        
        # Add rank column
        df.insert(0, 'rank', range(1, len(df) + 1))
        
        # Filter to top N
        df = df.head(top_n)
        
        return df
    
    def filter_by_criteria(self, df: pd.DataFrame, 
                          min_population: int = None,
                          max_listings: int = None,
                          min_score: float = None) -> pd.DataFrame:
        """
        Filter results based on investment criteria.
        
        Args:
            df: DataFrame with analysis results
            min_population: Minimum total population
            max_listings: Maximum number of listings
            min_score: Minimum investment score
            
        Returns:
            Filtered DataFrame
        """
        filtered = df.copy()
        
        if min_population:
            filtered = filtered[filtered['total_population'] >= min_population]
        
        if max_listings:
            filtered = filtered[filtered['total_listings'] <= max_listings]
        
        if min_score:
            filtered = filtered[filtered['investment_score'] >= min_score]
        
        # Reset rank
        if not filtered.empty:
            filtered['rank'] = range(1, len(filtered) + 1)
        
        return filtered
    
    def generate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics for the analysis."""
        if df.empty:
            return {}
        
        return {
            'total_zipcodes_analyzed': len(df),
            'avg_investment_score': df['investment_score'].mean(),
            'avg_population': df['total_population'].mean(),
            'avg_rental_ratio': df['rental_ratio'].mean(),
            'avg_listings': df['total_listings'].mean(),
            'avg_rent': df['average_rent'].mean(),
            'top_zipcode': df.iloc[0]['zipcode'] if len(df) > 0 else None,
            'top_score': df.iloc[0]['investment_score'] if len(df) > 0 else None,
        }



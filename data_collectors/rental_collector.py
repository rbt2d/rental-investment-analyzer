"""Rental data collector with support for multiple legitimate APIs."""
import requests
import time
from typing import Dict, List, Optional
from config import Config


class RentalDataCollector:
    """
    Collects rental listing data using legitimate APIs.
    
    Note: This class provides a framework for API integration.
    Users need to:
    1. Sign up for API access with providers (RentCast, Zillow, etc.)
    2. Add their API keys to .env file
    3. Follow each provider's terms of service
    """
    
    def __init__(self):
        """Initialize with configured API keys."""
        self.rentcast_key = Config.RENTCAST_API_KEY
        self.session = requests.Session()
    
    def get_rental_listings_count(self, zipcode: str) -> Dict:
        """
        Get rental listing counts and metrics for a zip code.
        
        Args:
            zipcode: ZIP code to analyze
            
        Returns:
            Dictionary with rental metrics
        """
        data = {
            'zipcode': zipcode,
            'total_listings': 0,
            'average_rent': 0,
            'vacancy_rate': 0,
            'data_source': 'none'
        }
        
        # Try RentCast API first (if configured)
        if self.rentcast_key:
            rentcast_data = self._get_rentcast_data(zipcode)
            if rentcast_data:
                return rentcast_data
        
        # If no API keys configured, use demo data
        data.update(self._generate_demo_data(zipcode))
        
        return data
    
    def _get_rentcast_data(self, zipcode: str) -> Optional[Dict]:
        """
        Fetch data from RentCast API.
        RentCast API: https://developers.rentcast.io/
        """
        if not self.rentcast_key:
            return None
        
        try:
            headers = {
                'X-Api-Key': self.rentcast_key,
                'accept': 'application/json'
            }
            
            # Get market statistics
            url = f"https://api.rentcast.io/v1/markets"
            params = {'zipCode': zipcode}
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'zipcode': zipcode,
                    'total_listings': data.get('totalListings', 0),
                    'average_rent': data.get('averageRent', 0),
                    'vacancy_rate': data.get('vacancyRate', 0),
                    'median_rent': data.get('medianRent', 0),
                    'price_per_sqft': data.get('pricePerSquareFoot', 0),
                    'data_source': 'rentcast'
                }
            else:
                print(f"RentCast API error: {response.status_code}")
        
        except Exception as e:
            print(f"Error fetching RentCast data: {e}")
        
        return None
    
    def _generate_demo_data(self, zipcode: str) -> Dict:
        """
        Generate realistic demo data for demonstration purposes.
        In production, this should be replaced with real API calls.
        """
        # Use zipcode as seed for reproducible "random" data
        seed = sum(ord(c) for c in zipcode)
        
        return {
            'total_listings': (seed % 300) + 50,
            'average_rent': 1000 + (seed % 2000),
            'vacancy_rate': (seed % 10) / 100,
            'median_rent': 950 + (seed % 1800),
            'price_per_sqft': 1.0 + (seed % 3),
            'data_source': 'demo_data'
        }
    
    def get_rental_demand_metrics(self, zipcode: str) -> Dict:
        """
        Get rental demand indicators for a zip code.
        
        This would ideally come from:
        - Search volume data
        - Days on market
        - Application rates
        - Rental growth trends
        """
        seed = sum(ord(c) for c in zipcode)
        
        return {
            'zipcode': zipcode,
            'search_volume_index': (seed % 100),
            'avg_days_on_market': 15 + (seed % 45),
            'rental_growth_yoy': ((seed % 20) - 5) / 100,  # -5% to +15%
            'demand_score': (seed % 100) / 100,
        }
    
    def get_bulk_rental_data(self, zipcodes: List[str]) -> Dict[str, Dict]:
        """
        Get rental data for multiple zip codes.
        
        Args:
            zipcodes: List of zip codes
            
        Returns:
            Dictionary mapping zip codes to their rental data
        """
        results = {}
        
        for zipcode in zipcodes:
            try:
                listing_data = self.get_rental_listings_count(zipcode)
                demand_data = self.get_rental_demand_metrics(zipcode)
                
                results[zipcode] = {
                    **listing_data,
                    **demand_data
                }
                
                time.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                print(f"Error collecting data for {zipcode}: {e}")
                continue
        
        return results


class ZillowAPICollector:
    """
    Zillow API collector (requires Zillow API access).
    Note: Zillow's public API has been discontinued. 
    Alternative: Use Zillow's ZTRAX data or partner APIs.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ZILLOW_API_KEY
    
    def get_listings(self, zipcode: str) -> Dict:
        """Placeholder for Zillow API integration."""
        return {
            'status': 'not_implemented',
            'message': 'Zillow public API discontinued. Use alternative data sources.'
        }



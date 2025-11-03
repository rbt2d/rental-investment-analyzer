"""Census data collector using official Census API."""
import requests
import time
from typing import Dict, List, Optional
from config import Config


class CensusDataCollector:
    """Collects population and demographic data from US Census API."""
    
    BASE_URL = "https://api.census.gov/data"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key."""
        self.api_key = api_key or Config.CENSUS_API_KEY
        self.session = requests.Session()
    
    def get_population_by_zipcode(self, zipcodes: List[str]) -> Dict[str, Dict]:
        """
        Get population data for multiple zip codes.
        
        Args:
            zipcodes: List of zip codes to query
            
        Returns:
            Dictionary mapping zip codes to their demographic data
        """
        results = {}
        
        for zipcode in zipcodes:
            try:
                data = self._fetch_zipcode_data(zipcode)
                if data:
                    results[zipcode] = data
                time.sleep(0.2)  # Rate limiting
            except Exception as e:
                print(f"Error fetching data for {zipcode}: {e}")
                continue
        
        return results
    
    def _fetch_zipcode_data(self, zipcode: str) -> Optional[Dict]:
        """Fetch data for a single zip code from Census API."""
        # Using ACS 5-Year estimates (most comprehensive)
        year = 2022
        
        params = {
            'get': 'NAME,B01003_001E,B25003_002E,B25003_003E,B19013_001E',
            'for': f'zip code tabulation area:{zipcode}',
            'key': self.api_key
        }
        
        try:
            url = f"{self.BASE_URL}/{year}/acs/acs5"
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    headers = data[0]
                    values = data[1]
                    
                    return {
                        'zipcode': zipcode,
                        'name': values[0],
                        'total_population': int(values[1]) if values[1] not in ['-', None] else 0,
                        'owner_occupied': int(values[2]) if values[2] not in ['-', None] else 0,
                        'renter_occupied': int(values[3]) if values[3] not in ['-', None] else 0,
                        'median_income': int(values[4]) if values[4] not in ['-', None] else 0,
                    }
        except Exception as e:
            print(f"Error fetching Census data for {zipcode}: {e}")
        
        return None
    
    def get_all_zipcodes_for_state(self, state_code: str) -> List[str]:
        """
        Get all zip codes for a given state.
        
        Args:
            state_code: Two-letter state code (e.g., 'CA', 'TX')
            
        Returns:
            List of zip codes
        """
        # This would require a comprehensive zip code database
        # For now, return empty list - users should provide target zip codes
        return []
    
    def get_metro_zipcodes(self, metro_name: str) -> List[str]:
        """Get zip codes for a metropolitan area."""
        # This would require metro area mapping
        # Implementation would need additional data source
        return []



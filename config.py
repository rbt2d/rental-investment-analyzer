"""Configuration management for Rental Investment Analyzer."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for API keys and settings."""
    
    # API Keys
    CENSUS_API_KEY = os.getenv('CENSUS_API_KEY', '')
    ZILLOW_API_KEY = os.getenv('ZILLOW_API_KEY', '')
    REALTOR_API_KEY = os.getenv('REALTOR_API_KEY', '')
    REDFIN_API_KEY = os.getenv('REDFIN_API_KEY', '')
    RENTCAST_API_KEY = os.getenv('RENTCAST_API_KEY', '')
    
    # Analysis Parameters
    MIN_POPULATION = int(os.getenv('MIN_POPULATION', 10000))
    MAX_RENTAL_LISTINGS = int(os.getenv('MAX_RENTAL_LISTINGS', 500))
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'csv')
    
    # Scoring Weights
    POPULATION_WEIGHT = 0.30
    RENTAL_DEMAND_WEIGHT = 0.35
    SUPPLY_SHORTAGE_WEIGHT = 0.35
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are present."""
        warnings = []
        if not cls.CENSUS_API_KEY:
            warnings.append("Census API key not found. Get one free at: https://api.census.gov/data/key_signup.html")
        
        if not any([cls.ZILLOW_API_KEY, cls.REALTOR_API_KEY, cls.RENTCAST_API_KEY]):
            warnings.append("No rental data API keys configured. Analysis will use demo data.")
        
        return warnings



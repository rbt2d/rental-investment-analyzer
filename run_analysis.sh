#!/bin/bash
# Quick run script for Rental Investment Analyzer

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN}  Rental Investment Analyzer${NC}"
echo -e "${CYAN}======================================${NC}"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo "Error: Virtual environment not found!"
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${CYAN}Creating .env from template...${NC}"
    cp .env.example .env
    echo "Please edit .env and add your Census API key"
    echo "Get one free at: https://api.census.gov/data/key_signup.html"
    echo ""
fi

# Run the application with passed arguments
if [ $# -eq 0 ]; then
    echo "Usage: ./run_analysis.sh [options]"
    echo ""
    echo "Examples:"
    echo "  ./run_analysis.sh --metro NYC --top 10"
    echo "  ./run_analysis.sh --zipcodes '10001,10002,10003'"
    echo "  ./run_analysis.sh --zipcode-file sample_zipcodes.txt"
    echo ""
    python main.py --help
else
    python main.py "$@"
fi



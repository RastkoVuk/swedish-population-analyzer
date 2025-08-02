# Swedish Population Analyzer

A Python tool for analyzing Swedish municipality population data.

## Features
- Population density analysis
- County-based statistics  
- Historical city age analysis
- Special focus on Göteborg

## Usage
```python
from swedish_analyzer import SwedishPopulationAnalyzer

analyzer = SwedishPopulationAnalyzer()
analyzer.run_complete_analysis()


Installation:

pip install -r requirements.txt
python swedish_analyzer.py


Data Source
Uses sample data with fallback to SCB API (when implemented).


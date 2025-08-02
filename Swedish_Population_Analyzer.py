# Swedish Population Analyzer
# API/fallback to sample data

import pandas as pd
import requests
from pathlib import Path

class SwedishPopulationAnalyzer:
    """
    Analyzes Swedish population data using pandas.
    Uses real SCB API data with fallback to sample data for offline use.
    """
    
    def __init__(self):
        self.df = None
        self.results = {}
        self.data_source = None  # Track whether we used API or sample data
    
    def _download_from_api(self):
        """
        Download data from Statistics Sweden (SCB) API.
        """
        # SCB API endpoint for population data
        api_url = "https://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0101/BE0101A/BefolkningNy"
        
        print("Attempting to download data from SCB API...")
        
        # Makes API request
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raises exception for bad status codes
        
        # Parse API response (this would need to be adapted to actual SCB format)
        api_data = response.json()
        
        # Convert to DataFrame (simplified - real implementation would parse SCB format)
        # This is a placeholder - actual SCB API parsing would be more complex
        raise NotImplementedError("SCB API parsing not yet implemented")
    
    def _load_sample_data(self):
        """
        Load sample data for offline use and development.
        """
        print("Using sample data for offline analysis...")
        
        sample_data = {
            'Municipality': ['Stockholm', 'Göteborg', 'Malmö', 'Uppsala', 'Västerås', 
                           'Örebro', 'Linköping', 'Helsingborg', 'Jönköping', 'Norrköping',
                           'Lund', 'Umeå', 'Gävle', 'Borås', 'Eskilstuna'],
            'Population': [975551, 579281, 347949, 230767, 154049, 
                          156381, 165618, 149280, 141081, 143171,
                          125542, 130224, 103318, 113641, 109382],
            'Area_km2': [188, 203, 158, 2189, 1139,
                        1380, 1436, 346, 1489, 1499,
                        430, 2331, 1617, 915, 1243],
            'County': ['Stockholm', 'Västra Götaland', 'Skåne', 'Uppsala', 'Västmanland',
                      'Örebro', 'Östergötland', 'Skåne', 'Jönköping', 'Östergötland',
                      'Skåne', 'Västerbotten', 'Gävleborg', 'Västra Götaland', 'Södermanland'],
            'Founded': [1252, 1621, 1275, 1286, 990,
                       1200, 1120, 1085, 1284, 1384,
                       990, 1622, 1446, 1621, 1659]
        }
        
        self.df = pd.DataFrame(sample_data)
        self.data_source = "sample"
        return True
    
    def load_data(self, force_sample=False):
        """
        Load data with automatic fallback from API to sample data.
        
        Args:
            force_sample (bool): If True, skip API and use sample data directly
        """
        if force_sample:
            print("Forced to use sample data...")
            return self._load_sample_data()
        
        try:
            # Try to get fresh data from API first
            self._download_from_api()
            self.data_source = "api"
            print(f"Loaded fresh data from SCB API")
            return True
            
        except Exception as e:
            print(f"API failed ({e})")
            print("Falling back to sample data...")
            return self._load_sample_data()
    
    def basic_analysis(self):
        """
        Perform basic data analysis.
        """
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print(f"BASIC DATA ANALYSIS ({self.data_source} data)")
        print("="*50)
        
        # Dataset overview
        print(f"Dataset shape: {self.df.shape}")
        print(f"Missing values: {self.df.isnull().sum().sum()}")
        
        # Basic statistics
        print(f"\nPopulation Statistics:")
        print(f"Total population: {self.df['Population'].sum():,}")
        print(f"Average population: {self.df['Population'].mean():,.0f}")
        print(f"Median population: {self.df['Population'].median():,.0f}")
        print(f"Largest city: {self.df.loc[self.df['Population'].idxmax(), 'Municipality']}")
        print(f"Smallest city: {self.df.loc[self.df['Population'].idxmin(), 'Municipality']}")
        
        # Store results
        self.results['basic_stats'] = {
            'total_population': self.df['Population'].sum(),
            'avg_population': self.df['Population'].mean(),
            'largest_city': self.df.loc[self.df['Population'].idxmax(), 'Municipality'],
            'data_source': self.data_source
        }
    
    def population_density_analysis(self):
        """
        Calculate and analyze population density.
        """
        if self.df is None:
            return
        
        print("\n" + "="*50)
        print("POPULATION DENSITY ANALYSIS")
        print("="*50)
        
        # Calculate population density
        self.df['Density_per_km2'] = self.df['Population'] / self.df['Area_km2']
        
        # Sort by density
        density_sorted = self.df.sort_values('Density_per_km2', ascending=False)
        
        print("Top 5 Most Dense Cities:")
        for i, row in density_sorted.head().iterrows():
            print(f"{row['Municipality']}: {row['Density_per_km2']:.0f} people/km²")
        
        print("\nTop 5 Least Dense Cities:")
        for i, row in density_sorted.tail().iterrows():
            print(f"{row['Municipality']}: {row['Density_per_km2']:.0f} people/km²")
    
    def goteborg_focus(self):
        """
        Special analysis focusing on Göteborg.
        """
        if self.df is None:
            return
        
        print("\n" + "="*50)
        print("GÖTEBORG FOCUS ANALYSIS")
        print("="*50)
        
        # Get Göteborg data
        goteborg = self.df[self.df['Municipality'] == 'Göteborg'].iloc[0]
        
        print(f"Göteborg Profile:")
        print(f"Population: {goteborg['Population']:,}")
        print(f"Area: {goteborg['Area_km2']:,} km²")
        print(f"Density: {goteborg['Density_per_km2']:.0f} people/km²")
        print(f"Founded: {goteborg['Founded']}")
        
        # Ranking
        pop_rank = (self.df['Population'] > goteborg['Population']).sum() + 1
        density_rank = (self.df['Density_per_km2'] > goteborg['Density_per_km2']).sum() + 1
        
        print(f"\nGöteborg Rankings:")
        print(f"Population rank: #{pop_rank} out of {len(self.df)}")
        print(f"Density rank: #{density_rank} out of {len(self.df)}")
    
    def run_complete_analysis(self, force_sample=False):
        """
        Run the complete analysis pipeline.
        
        Args:
            force_sample (bool): Use sample data instead of trying API
        """
        print("Starting Swedish Population Analysis")
        print("Focus: Göteborg and Swedish municipalities")
        
        # Load data with fallback
        if not self.load_data(force_sample=force_sample):
            print("Failed to load any data. Exiting.")
            return
        
        # Run analysis steps
        steps = [
            ("Basic Analysis", self.basic_analysis),
            ("Population Density", self.population_density_analysis),
            ("Göteborg Focus", self.goteborg_focus)
        ]
        
        for step_name, step_func in steps:
            try:
                step_func()
            except Exception as e:
                print(f"{step_name} failed: {e}")
        
        print("\n🎉 Analysis Complete!")
        
        # Show data source info
        if self.data_source == "sample":
            print(" Note: This analysis used sample data.")
            print("   For production use, implement real SCB API integration.")


def main():
    """
    Main function to run the analysis.
    """
    analyzer = SwedishPopulationAnalyzer()
    
    # Run with sample data (reliable for GitHub demos)
    analyzer.run_complete_analysis(force_sample=True)
    
    print("\n" + "="*50)
    print("PYTHON SKILLS DEMONSTRATION")
    print("="*50)
    
    # List comprehensions
    large_cities = [city for city, pop in zip(analyzer.df['Municipality'], analyzer.df['Population']) 
                   if pop > 150000]
    print(f"Large cities (>150k): {large_cities}")
    
    # Dictionary comprehension
    city_populations = {row['Municipality']: row['Population'] 
                       for _, row in analyzer.df.iterrows()}
    print(f"Stockholm population: {city_populations.get('Stockholm', 'Not found'):,}")


if __name__ == "__main__":
    main()
"""
Main script for the Bellabeat fitness data analysis.
This script orchestrates the entire analysis workflow.
"""

import os
from pathlib import Path
from data.prepare import DataPreparation
from data.validate import DataValidation
from analysis.activity import ActivityAnalysis
from visualization.plots import DataVisualization

# Set environment variable to avoid KMeans memory leak warning
os.environ['OMP_NUM_THREADS'] = '1'

def create_directories() -> None:
    """Create necessary directories if they don't exist."""
    dirs = ['data', 'reports', 'reports/figures']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def main():
    """Run the complete analysis workflow."""
    print("Starting Bellabeat Fitness Data Analysis...")
    
    # Create directories
    create_directories()
    
    # Initialize data preparation
    print("\n1. Preparing data...")
    data_prep = DataPreparation()
    merged_daily, heart_rate, weight, hourly = data_prep.prepare_all_data()
    
    # Validate data
    print("\n2. Validating data quality...")
    validator = DataValidation()
    validation_passed = validator.validate_all_data(
        merged_daily,
        data_prep.sleep_data,
        heart_rate,
        weight,
        hourly
    )
    
    if not validation_passed:
        print("\n⚠️ Data validation failed! Check validation_report.md for details.")
        print("Proceeding with analysis, but results may be affected.")
    else:
        print("\n✓ Data validation passed!")
    
    # Perform activity analysis
    print("\n3. Analyzing activity patterns...")
    activity_analysis = ActivityAnalysis(merged_daily, hourly)
    
    # Get user segments
    user_segments = activity_analysis.calculate_user_segments()
    daily_patterns = activity_analysis.analyze_daily_patterns()
    hourly_patterns = activity_analysis.analyze_hourly_patterns()
    correlations = activity_analysis.analyze_correlations()
    
    # Generate insights and recommendations
    print("\n4. Generating insights...")
    insights = activity_analysis.generate_insights()
    recommendations = activity_analysis.get_recommendations()
    
    # Create visualizations
    print("\n5. Creating visualizations...")
    viz = DataVisualization()
    
    data_dict = {
        'daily': merged_daily,
        'hourly': hourly,
        'segments': user_segments,
        'correlations': correlations,
        'sleep': merged_daily[merged_daily['SleepDurationHours'].notna()]
    }
    
    viz.create_dashboard(data_dict, 'reports/figures')
    
    # Generate report
    print("\n6. Generating final report...")
    generate_report(insights, recommendations, validation_passed)
    
    print("\nAnalysis complete! Check the 'reports' directory for results.")

def generate_report(insights: list, recommendations: list, validation_passed: bool) -> None:
    """Generate a markdown report with analysis results.
    
    Args:
        insights: List of key insights
        recommendations: List of recommendations
        validation_passed: Whether data validation passed
    """
    report = """# Bellabeat Fitness Data Analysis Report

## Overview
This report presents the analysis of FitBit Fitness Tracker Data to inform Bellabeat's marketing strategy.

## Data Quality
"""
    
    if validation_passed:
        report += "All data quality checks passed. The analysis is based on validated data.\n"
    else:
        report += """Some data quality checks failed. Please refer to the validation_report.md
for detailed information about data quality issues that may affect the analysis results.\n"""
    
    report += "\n## Key Insights\n"
    
    for i, insight in enumerate(insights, 1):
        report += f"{i}. {insight}\n"
    
    report += "\n## Recommendations\n"
    
    for i, rec in enumerate(recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += """
## Visualizations
The following visualizations can be found in the 'reports/figures' directory:

1. Daily Activity Patterns (daily_patterns.png)
2. Hourly Activity Patterns (hourly_patterns.html)
3. User Segments (user_segments.html)
4. Correlation Matrix (correlations.png)
5. Sleep Patterns (sleep_patterns.png)

## Methodology
The analysis followed these steps:
1. Data preparation and cleaning
2. Data quality validation
3. Activity pattern analysis
4. User segmentation
5. Correlation analysis
6. Insight generation

## Conclusion
The analysis reveals several opportunities for Bellabeat to enhance its product offerings
and marketing strategy based on user behavior patterns and preferences.

## Next Steps
1. Implement the recommended features in the Bellabeat app
2. Design targeted marketing campaigns for each user segment
3. Conduct follow-up analysis on feature adoption and impact
4. Consider collecting additional data points for deeper insights
"""
    
    # Create reports directory if it doesn't exist
    Path('reports').mkdir(exist_ok=True)
    
    with open('reports/analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    main() 
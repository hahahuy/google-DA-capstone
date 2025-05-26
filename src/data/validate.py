"""
Data validation module for the Bellabeat fitness data analysis.
This module ensures data quality and consistency.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path

class DataValidation:
    def __init__(self):
        """Initialize the data validation class."""
        self.validation_results = {}
    
    def validate_daily_activity(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate daily activity data.
        
        Args:
            df: DataFrame containing daily activity data
            
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Check for missing values
        results['no_missing_values'] = df.isnull().sum().sum() == 0
        
        # Check for valid date range
        date_range = df['ActivityDate'].max() - df['ActivityDate'].min()
        results['valid_date_range'] = date_range.days <= 31  # Data should be within a month
        
        # Check for valid numeric ranges
        results['valid_steps'] = (df['TotalSteps'] >= 0).all()
        results['valid_distance'] = (df['TotalDistance'] >= 0).all()
        results['valid_calories'] = (df['Calories'] > 0).all()
        results['valid_minutes'] = (
            (df['VeryActiveMinutes'] >= 0).all() and
            (df['FairlyActiveMinutes'] >= 0).all() and
            (df['LightlyActiveMinutes'] >= 0).all() and
            (df['SedentaryMinutes'] >= 0).all()
        )
        
        # Check for logical consistency
        total_minutes = (
            df['VeryActiveMinutes'] +
            df['FairlyActiveMinutes'] +
            df['LightlyActiveMinutes'] +
            df['SedentaryMinutes']
        )
        results['valid_total_minutes'] = (total_minutes <= 1440).all()  # 24 hours = 1440 minutes
        
        return results
    
    def validate_sleep_data(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate sleep data.
        
        Args:
            df: DataFrame containing sleep data
            
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Check for missing values
        results['no_missing_values'] = df.isnull().sum().sum() == 0
        
        # Check for valid sleep duration
        results['valid_sleep_duration'] = (
            (df['TotalMinutesAsleep'] >= 60).all() and  # At least 1 hour
            (df['TotalMinutesAsleep'] <= 1440).all()    # At most 24 hours
        )
        
        # Check for valid time in bed
        results['valid_time_in_bed'] = (
            (df['TotalTimeInBed'] >= df['TotalMinutesAsleep']).all()
        )
        
        return results
    
    def validate_heart_rate(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate heart rate data.
        
        Args:
            df: DataFrame containing heart rate data
            
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Check for missing values
        results['no_missing_values'] = df.isnull().sum().sum() == 0
        
        # Check for valid heart rate range (40-220 bpm)
        results['valid_heart_rate'] = (
            (df['Value'] >= 40).all() and
            (df['Value'] <= 220).all()
        )
        
        # Check for valid timestamps
        results['valid_timestamps'] = pd.to_datetime(df['Time']).notna().all()
        
        return results
    
    def validate_weight_data(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate weight data.
        
        Args:
            df: DataFrame containing weight data
            
        Returns:
            Dictionary of validation results
        """
        results = {}
        
        # Check for valid weight range (20-300 kg)
        results['valid_weight'] = (
            (df['WeightKg'] >= 20).all() and
            (df['WeightKg'] <= 300).all()
        )
        
        # Check for valid BMI range (15-50)
        results['valid_bmi'] = (
            (df['BMI'] >= 15).all() and
            (df['BMI'] <= 50).all()
        )
        
        # Check for missing values in required fields
        results['no_missing_required'] = (
            df[['Id', 'Date', 'WeightKg', 'BMI']].isnull().sum().sum() == 0
        )
        
        return results
    
    def validate_hourly_data(self, hourly_data: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, bool]]:
        """Validate hourly data.
        
        Args:
            hourly_data: Dictionary containing hourly activity data
            
        Returns:
            Dictionary of validation results for each dataset
        """
        results = {}
        
        for key, df in hourly_data.items():
            dataset_results = {}
            
            # Check for missing values
            dataset_results['no_missing_values'] = df.isnull().sum().sum() == 0
            
            # Check for valid hour values
            dataset_results['valid_hours'] = (
                (df['Hour'] >= 0).all() and
                (df['Hour'] <= 23).all()
            )
            
            # Check for valid metrics
            if key == 'steps':
                dataset_results['valid_values'] = (df['StepTotal'] >= 0).all()
            elif key == 'calories':
                dataset_results['valid_values'] = (df['Calories'] > 0).all()
            elif key == 'intensities':
                dataset_results['valid_values'] = (
                    (df['TotalIntensity'] >= 0).all() and
                    (df['AverageIntensity'] >= 0).all()
                )
            
            results[key] = dataset_results
        
        return results
    
    def generate_validation_report(self) -> str:
        """Generate a validation report.
        
        Returns:
            Validation report as a string
        """
        report = "# Data Validation Report\n\n"
        
        for dataset, results in self.validation_results.items():
            report += f"## {dataset}\n"
            for check, passed in results.items():
                status = "PASS" if passed else "FAIL"
                report += f"- {check}: {status}\n"
            report += "\n"
        
        return report
    
    def validate_all_data(
        self,
        daily_activity: pd.DataFrame,
        sleep_data: pd.DataFrame,
        heart_rate: pd.DataFrame,
        weight_data: pd.DataFrame,
        hourly_data: Dict[str, pd.DataFrame]
    ) -> bool:
        """Validate all datasets.
        
        Args:
            daily_activity: Daily activity DataFrame
            sleep_data: Sleep data DataFrame
            heart_rate: Heart rate DataFrame
            weight_data: Weight data DataFrame
            hourly_data: Dictionary of hourly DataFrames
            
        Returns:
            True if all validations pass, False otherwise
        """
        # Validate each dataset
        self.validation_results['daily_activity'] = self.validate_daily_activity(daily_activity)
        self.validation_results['sleep_data'] = self.validate_sleep_data(sleep_data)
        self.validation_results['heart_rate'] = self.validate_heart_rate(heart_rate)
        self.validation_results['weight_data'] = self.validate_weight_data(weight_data)
        self.validation_results['hourly_data'] = self.validate_hourly_data(hourly_data)
        
        # Check if all validations passed
        all_passed = all(
            all(results.values())
            for results in self.validation_results.values()
        )
        
        # Create reports directory if it doesn't exist
        Path('reports').mkdir(exist_ok=True)
        
        # Generate validation report
        report = self.generate_validation_report()
        with open('reports/validation_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        return all_passed 
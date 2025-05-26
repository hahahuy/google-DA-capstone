"""
Data preparation module for the Bellabeat fitness data analysis.
This module handles data loading, cleaning, and preprocessing.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class DataPreparation:
    def __init__(self, data_dir: str = "dataset"):
        """Initialize the data preparation class.
        
        Args:
            data_dir: Directory containing the raw data files
        """
        self.data_dir = Path(data_dir)
        self.daily_activity = None
        self.sleep_data = None
        self.heart_rate = None
        self.weight_data = None
        self.hourly_data = {}
    
    def load_data(self) -> None:
        """Load all relevant datasets."""
        # Load daily activity data
        self.daily_activity = pd.read_csv(
            self.data_dir / "dailyActivity_merged.csv",
            parse_dates=['ActivityDate'],
            date_format='%m/%d/%Y'
        )
        
        # Load sleep data
        self.sleep_data = pd.read_csv(
            self.data_dir / "sleepDay_merged.csv"
        )
        
        # Load heart rate data
        self.heart_rate = pd.read_csv(
            self.data_dir / "heartrate_seconds_merged.csv"
        )
        
        # Load weight data
        self.weight_data = pd.read_csv(
            self.data_dir / "weightLogInfo_merged.csv"
        )
        
        # Load hourly data
        hourly_files = {
            'calories': 'hourlyCalories_merged.csv',
            'steps': 'hourlySteps_merged.csv',
            'intensities': 'hourlyIntensities_merged.csv'
        }
        
        for key, filename in hourly_files.items():
            self.hourly_data[key] = pd.read_csv(self.data_dir / filename)
    
    def clean_daily_activity(self) -> pd.DataFrame:
        """Clean and preprocess daily activity data.
        
        Returns:
            Cleaned daily activity DataFrame
        """
        df = self.daily_activity.copy()
        
        # Convert date column
        df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
        
        # Add day of week
        df['DayOfWeek'] = df['ActivityDate'].dt.day_name()
        
        # Calculate total active minutes
        df['TotalActiveMinutes'] = (
            df['VeryActiveMinutes'] + 
            df['FairlyActiveMinutes'] + 
            df['LightlyActiveMinutes']
        )
        
        # Calculate activity ratios
        df['ActiveToSedentaryRatio'] = df['TotalActiveMinutes'] / df['SedentaryMinutes']
        
        # Remove any rows with impossible values
        df = df[
            (df['TotalSteps'] >= 0) &
            (df['Calories'] > 0) &
            (df['TotalDistance'] >= 0)
        ]
        
        return df
    
    def clean_sleep_data(self) -> pd.DataFrame:
        """Clean and preprocess sleep data.
        
        Returns:
            Cleaned sleep DataFrame
        """
        df = self.sleep_data.copy()
        
        # Convert date column
        df['SleepDay'] = pd.to_datetime(df['SleepDay'], format='%m/%d/%Y %I:%M:%S %p')
        
        # Calculate sleep efficiency
        df['SleepEfficiency'] = df['TotalMinutesAsleep'] / df['TotalTimeInBed']
        
        # Calculate sleep duration in hours
        df['SleepDurationHours'] = df['TotalMinutesAsleep'] / 60
        
        # Remove outliers (sleep duration > 24 hours or < 1 hour)
        df = df[
            (df['SleepDurationHours'] <= 24) &
            (df['SleepDurationHours'] >= 1) &
            (df['SleepEfficiency'] <= 1)  # Sleep time can't be more than time in bed
        ]
        
        return df
    
    def clean_heart_rate(self) -> pd.DataFrame:
        """Clean and preprocess heart rate data.
        
        Returns:
            Cleaned heart rate DataFrame
        """
        df = self.heart_rate.copy()
        
        # Convert time column
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
        
        # Add date column
        df['Date'] = df['Time'].dt.date
        
        # Remove outliers (heart rate > 220 or < 40)
        df = df[
            (df['Value'] <= 220) &
            (df['Value'] >= 40)
        ]
        
        return df
    
    def clean_weight_data(self) -> pd.DataFrame:
        """Clean and preprocess weight data.
        
        Returns:
            Cleaned weight DataFrame
        """
        df = self.weight_data.copy()
        
        # Convert date column
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
        
        # Fill missing fat values with median per user
        df['Fat'] = df.groupby('Id')['Fat'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # Calculate BMI if missing
        df['BMI'] = np.where(
            df['BMI'].isnull(),
            df['WeightKg'] / ((df['WeightKg'] / df['BMI']).mean()) ** 2,
            df['BMI']
        )
        
        return df
    
    def clean_hourly_data(self) -> Dict[str, pd.DataFrame]:
        """Clean and preprocess hourly data.
        
        Returns:
            Dictionary of cleaned hourly DataFrames
        """
        cleaned_data = {}
        
        for key, df in self.hourly_data.items():
            cleaned = df.copy()
            
            # Convert activity time
            cleaned['ActivityHour'] = pd.to_datetime(cleaned['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')
            
            # Add date and hour columns
            cleaned['Date'] = cleaned['ActivityHour'].dt.date
            cleaned['Hour'] = cleaned['ActivityHour'].dt.hour
            
            cleaned_data[key] = cleaned
        
        return cleaned_data
    
    def merge_daily_sleep(self) -> pd.DataFrame:
        """Merge daily activity and sleep data.
        
        Returns:
            Merged DataFrame with daily activity and sleep data
        """
        daily = self.clean_daily_activity()
        sleep = self.clean_sleep_data()
        
        # Merge with daily activity
        merged = pd.merge(
            daily,
            sleep,
            left_on=['Id', daily['ActivityDate'].dt.date],
            right_on=['Id', sleep['SleepDay'].dt.date],
            how='left'
        )
        
        return merged
    
    def prepare_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Prepare all datasets.
        
        Returns:
            Tuple containing:
            - Merged daily activity and sleep data
            - Cleaned heart rate data
            - Cleaned weight data
            - Dictionary of cleaned hourly data
        """
        self.load_data()
        
        merged_daily = self.merge_daily_sleep()
        heart_rate = self.clean_heart_rate()
        weight = self.clean_weight_data()
        hourly = self.clean_hourly_data()
        
        return merged_daily, heart_rate, weight, hourly 
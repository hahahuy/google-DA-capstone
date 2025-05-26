"""
Test script to verify data loading and processing.
"""

from data.prepare import DataPreparation
import pandas as pd

def test_data_loading():
    """Test if all data files can be loaded and processed."""
    print("Testing data loading and processing...")
    
    try:
        # Initialize data preparation
        data_prep = DataPreparation()
        
        # Try loading all data
        print("\n1. Loading data files...")
        data_prep.load_data()
        print("✓ All data files loaded successfully")
        
        # Check data shapes
        print("\n2. Checking data dimensions:")
        print(f"- Daily activity: {data_prep.daily_activity.shape}")
        print(f"- Sleep data: {data_prep.sleep_data.shape}")
        print(f"- Heart rate: {data_prep.heart_rate.shape}")
        print(f"- Weight data: {data_prep.weight_data.shape}")
        for key, df in data_prep.hourly_data.items():
            print(f"- Hourly {key}: {df.shape}")
        
        # Try processing all data
        print("\n3. Processing data...")
        merged_daily, heart_rate, weight, hourly = data_prep.prepare_all_data()
        print("✓ All data processed successfully")
        
        # Check processed data
        print("\n4. Checking processed data:")
        print(f"- Merged daily data: {merged_daily.shape}")
        print(f"- Processed heart rate: {heart_rate.shape}")
        print(f"- Processed weight: {weight.shape}")
        for key, df in hourly.items():
            print(f"- Processed hourly {key}: {df.shape}")
        
        print("\n✓ All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_data_loading() 
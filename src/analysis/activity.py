"""
Activity analysis module for the Bellabeat fitness data analysis.
This module analyzes activity patterns and provides insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.cluster import KMeans

class ActivityAnalysis:
    def __init__(self, daily_data: pd.DataFrame, hourly_data: Dict[str, pd.DataFrame]):
        """Initialize the activity analysis class.
        
        Args:
            daily_data: DataFrame containing daily activity data
            hourly_data: Dictionary of hourly activity DataFrames
        """
        self.daily_data = daily_data
        self.hourly_data = hourly_data
    
    def calculate_user_segments(self) -> pd.DataFrame:
        """Segment users based on their activity patterns.
        
        Returns:
            DataFrame with user segments and their characteristics
        """
        # Calculate average metrics per user
        user_metrics = self.daily_data.groupby('Id').agg({
            'TotalSteps': 'mean',
            'Calories': 'mean',
            'TotalActiveMinutes': 'mean',
            'SedentaryMinutes': 'mean'
        }).reset_index()
        
        # Normalize features for clustering
        features = ['TotalSteps', 'Calories', 'TotalActiveMinutes']
        X = user_metrics[features]
        X_scaled = (X - X.mean()) / X.std()
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        user_metrics['Segment'] = kmeans.fit_predict(X_scaled)
        
        # Label segments
        segment_labels = {
            0: 'Low Activity',
            1: 'Moderate Activity',
            2: 'High Activity'
        }
        user_metrics['SegmentLabel'] = user_metrics['Segment'].map(segment_labels)
        
        return user_metrics
    
    def analyze_daily_patterns(self) -> Dict[str, pd.DataFrame]:
        """Analyze daily activity patterns.
        
        Returns:
            Dictionary containing various daily pattern analyses
        """
        results = {}
        
        # Activity by day of week
        results['day_of_week'] = self.daily_data.groupby('DayOfWeek').agg({
            'TotalSteps': 'mean',
            'Calories': 'mean',
            'TotalActiveMinutes': 'mean',
            'SedentaryMinutes': 'mean'
        }).round(2)
        
        # Activity level distribution
        def get_activity_level(minutes):
            if minutes < 30:
                return 'Sedentary'
            elif minutes < 60:
                return 'Lightly Active'
            elif minutes < 120:
                return 'Moderately Active'
            else:
                return 'Very Active'
        
        self.daily_data['ActivityLevel'] = self.daily_data['TotalActiveMinutes'].apply(get_activity_level)
        results['activity_levels'] = self.daily_data['ActivityLevel'].value_counts().to_frame()
        
        # Steps achievement
        self.daily_data['StepsAchieved'] = self.daily_data['TotalSteps'] >= 10000
        results['steps_achievement'] = self.daily_data['StepsAchieved'].value_counts().to_frame()
        
        return results
    
    def analyze_hourly_patterns(self) -> Dict[str, pd.DataFrame]:
        """Analyze hourly activity patterns.
        
        Returns:
            Dictionary containing various hourly pattern analyses
        """
        results = {}
        
        # Steps by hour
        hourly_steps = self.hourly_data['steps'].groupby('Hour')['StepTotal'].mean().round(2)
        results['hourly_steps'] = hourly_steps.to_frame()
        
        # Calories by hour
        hourly_calories = self.hourly_data['calories'].groupby('Hour')['Calories'].mean().round(2)
        results['hourly_calories'] = hourly_calories.to_frame()
        
        # Peak activity hours
        peak_hours = hourly_steps.nlargest(3)
        results['peak_hours'] = peak_hours.to_frame()
        
        return results
    
    def analyze_correlations(self) -> pd.DataFrame:
        """Analyze correlations between different metrics.
        
        Returns:
            DataFrame containing correlation analysis
        """
        # Select relevant columns for correlation
        cols = [
            'TotalSteps', 'Calories', 'TotalActiveMinutes',
            'SedentaryMinutes', 'VeryActiveMinutes',
            'FairlyActiveMinutes', 'LightlyActiveMinutes'
        ]
        
        # Calculate correlation matrix
        corr_matrix = self.daily_data[cols].corr().round(3)
        
        return corr_matrix
    
    def generate_insights(self) -> List[str]:
        """Generate key insights from the analysis.
        
        Returns:
            List of key insights
        """
        insights = []
        
        # User segments
        segments = self.calculate_user_segments()
        segment_dist = segments['SegmentLabel'].value_counts()
        insights.append(
            f"User Segmentation: {segment_dist.to_dict()}"
        )
        
        # Daily patterns
        daily_patterns = self.analyze_daily_patterns()
        steps_achieved = daily_patterns['steps_achievement']
        insights.append(
            f"Steps Goal Achievement: {(steps_achieved.loc[True] / len(self.daily_data) * 100).round(1)}% of days"
        )
        
        # Hourly patterns
        hourly_patterns = self.analyze_hourly_patterns()
        peak_hours = hourly_patterns['peak_hours']
        insights.append(
            f"Peak Activity Hours: {', '.join(map(str, peak_hours.index))}"
        )
        
        # Correlations
        corr_matrix = self.analyze_correlations()
        steps_calories_corr = corr_matrix.loc['TotalSteps', 'Calories']
        insights.append(
            f"Steps-Calories Correlation: {steps_calories_corr:.3f}"
        )
        
        return insights
    
    def get_recommendations(self) -> List[str]:
        """Generate recommendations based on the analysis.
        
        Returns:
            List of recommendations
        """
        recommendations = [
            "Implement personalized activity goals based on user segments",
            "Send activity reminders during peak activity hours",
            "Gamify the 10,000 steps achievement with rewards",
            "Provide detailed sleep analysis for better health insights",
            "Add social features to encourage group activities",
            "Develop stress monitoring based on activity and heart rate patterns"
        ]
        
        return recommendations 
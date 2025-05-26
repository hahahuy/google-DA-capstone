"""
Visualization module for the Bellabeat fitness data analysis.
This module creates informative and aesthetically pleasing plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

class DataVisualization:
    def __init__(self, style: str = "seaborn-v0_8"):
        """Initialize the visualization class.
        
        Args:
            style: The matplotlib style to use
        """
        plt.style.use(style)
        self.colors = px.colors.qualitative.Set3
    
    def plot_daily_activity_patterns(self, daily_data: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """Create plots showing daily activity patterns.
        
        Args:
            daily_data: DataFrame containing daily activity data
            save_path: Optional path to save the plot
        """
        # Create subplots
        fig = plt.figure(figsize=(15, 10))
        
        # Steps by day of week
        plt.subplot(2, 2, 1)
        sns.boxplot(data=daily_data, x='DayOfWeek', y='TotalSteps')
        plt.xticks(rotation=45)
        plt.title('Steps Distribution by Day')
        
        # Active minutes distribution
        plt.subplot(2, 2, 2)
        active_cols = ['VeryActiveMinutes', 'FairlyActiveMinutes', 
                      'LightlyActiveMinutes', 'SedentaryMinutes']
        daily_data[active_cols].mean().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Activity Level Distribution')
        
        # Steps vs Calories
        plt.subplot(2, 2, 3)
        sns.scatterplot(data=daily_data, x='TotalSteps', y='Calories', alpha=0.5)
        plt.title('Steps vs Calories Burned')
        
        # Activity level counts
        plt.subplot(2, 2, 4)
        daily_data['ActivityLevel'].value_counts().plot(kind='bar')
        plt.title('Activity Level Counts')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.close()
    
    def plot_hourly_patterns(self, hourly_data: Dict[str, pd.DataFrame], save_path: Optional[str] = None) -> None:
        """Create plots showing hourly activity patterns.
        
        Args:
            hourly_data: Dictionary containing hourly activity data
            save_path: Optional path to save the plot
        """
        # Create figure
        fig = go.Figure()
        
        # Add steps trace
        steps = hourly_data['steps'].groupby('Hour')['StepTotal'].mean()
        fig.add_trace(go.Scatter(
            x=steps.index,
            y=steps.values,
            name='Steps',
            line=dict(color=self.colors[0])
        ))
        
        # Add calories trace
        calories = hourly_data['calories'].groupby('Hour')['Calories'].mean()
        fig.add_trace(go.Scatter(
            x=calories.index,
            y=calories.values,
            name='Calories',
            yaxis='y2',
            line=dict(color=self.colors[1])
        ))
        
        # Update layout
        fig.update_layout(
            title='Hourly Activity Patterns',
            xaxis=dict(title='Hour of Day'),
            yaxis=dict(title='Average Steps', side='left'),
            yaxis2=dict(title='Average Calories', side='right', overlaying='y'),
            hovermode='x unified'
        )
        
        if save_path:
            fig.write_html(save_path)
    
    def plot_user_segments(self, segments: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """Create plots showing user segments.
        
        Args:
            segments: DataFrame containing user segment data
            save_path: Optional path to save the plot
        """
        # Create scatter plot
        fig = px.scatter(
            segments,
            x='TotalSteps',
            y='Calories',
            color='SegmentLabel',
            size='TotalActiveMinutes',
            hover_data=['Id'],
            title='User Segments by Activity Patterns'
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Average Daily Steps',
            yaxis_title='Average Daily Calories',
            showlegend=True
        )
        
        if save_path:
            fig.write_html(save_path)
    
    def plot_correlation_matrix(self, corr_matrix: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """Create a correlation matrix heatmap.
        
        Args:
            corr_matrix: DataFrame containing correlation matrix
            save_path: Optional path to save the plot
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='coolwarm',
            center=0,
            vmin=-1,
            vmax=1,
            square=True
        )
        plt.title('Correlation Matrix of Activity Metrics')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
    
    def plot_sleep_patterns(self, sleep_data: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """Create plots showing sleep patterns.
        
        Args:
            sleep_data: DataFrame containing sleep data
            save_path: Optional path to save the plot
        """
        # Create subplots
        fig = plt.figure(figsize=(15, 5))
        
        # Sleep duration distribution
        plt.subplot(1, 2, 1)
        sns.histplot(data=sleep_data, x='SleepDurationHours', bins=30)
        plt.title('Sleep Duration Distribution')
        plt.xlabel('Hours of Sleep')
        
        # Sleep vs Activity
        plt.subplot(1, 2, 2)
        sns.scatterplot(
            data=sleep_data,
            x='TotalActiveMinutes',
            y='SleepDurationHours',
            alpha=0.5
        )
        plt.title('Sleep Duration vs Activity Level')
        plt.xlabel('Total Active Minutes')
        plt.ylabel('Hours of Sleep')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.close()
    
    def create_dashboard(self, data_dict: Dict[str, pd.DataFrame], save_dir: str) -> None:
        """Create a comprehensive dashboard of visualizations.
        
        Args:
            data_dict: Dictionary containing all prepared data
            save_dir: Directory to save the dashboard plots
        """
        # Create daily activity patterns plot
        self.plot_daily_activity_patterns(
            data_dict['daily'],
            f'{save_dir}/daily_patterns.png'
        )
        
        # Create hourly patterns plot
        self.plot_hourly_patterns(
            data_dict['hourly'],
            f'{save_dir}/hourly_patterns.html'
        )
        
        # Create user segments plot
        self.plot_user_segments(
            data_dict['segments'],
            f'{save_dir}/user_segments.html'
        )
        
        # Create correlation matrix plot
        self.plot_correlation_matrix(
            data_dict['correlations'],
            f'{save_dir}/correlations.png'
        )
        
        # Create sleep patterns plot
        if 'sleep' in data_dict:
            self.plot_sleep_patterns(
                data_dict['sleep'],
                f'{save_dir}/sleep_patterns.png'
            ) 
# Bellabeat Fitness Data Analysis Report

## Overview
This report presents the analysis of FitBit Fitness Tracker Data to inform Bellabeat's marketing strategy.

## Data Quality
Some data quality checks failed. Please refer to the validation_report.md
for detailed information about data quality issues that may affect the analysis results.

## Key Insights

### User Activity Segments
- High Activity Users: 15 users (45.5%)
- Moderate Activity Users: 12 users (36.4%)
- Low Activity Users: 6 users (18.1%)

<iframe src="https://hahahuy.github.io/google-DA-capstone/user_segments.html" width="100%" height="600px" frameborder="0"></iframe>

### Activity Goals and Patterns
- 32.5% of users regularly achieve their daily step goals
- Peak activity hours are between 5-7 PM (17:00-19:00)
- Moderate positive correlation (0.59) between steps and calories burned

![Daily Activity Patterns](figures/daily_patterns.png)

<iframe src="https://hahahuy.github.io/google-DA-capstone/hourly_patterns.html" width="100%" height="600px" frameborder="0"></iframe>

### Sleep and Health Patterns
- Average sleep duration: 7 hours
- Most active users tend to have better sleep quality
- Weekend activity levels are generally lower than weekdays

![Sleep Patterns](figures/sleep_patterns.png)

### Correlation Analysis
The analysis revealed several significant correlations between different metrics:

![Correlation Matrix](figures/correlations.png)

## Recommendations

1. Personalization and Goals
   - Implement personalized activity goals based on user segments
   - Send smart notifications during peak activity hours (5-7 PM)
   - Gamify the 10,000 steps achievement with rewards

2. Health and Wellness Features
   - Provide detailed sleep analysis and recommendations
   - Add stress monitoring based on activity and heart rate patterns
   - Implement recovery time suggestions based on activity intensity

3. Social and Engagement
   - Add social features to encourage group activities
   - Create challenges based on user segments
   - Implement achievement sharing and social recognition

## Interactive Visualizations
The interactive visualizations are embedded directly in the report above. You can interact with them directly in this document.

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
and marketing strategy based on user behavior patterns and preferences. The data shows
clear user segments with different activity levels and patterns, suggesting a need for
personalized features and targeted marketing approaches.

## Next Steps
1. Implement the recommended features in the Bellabeat app
2. Design targeted marketing campaigns for each user segment
3. Conduct follow-up analysis on feature adoption and impact
4. Consider collecting additional data points for deeper insights

---
Note: Some visualizations are provided as interactive HTML files. To view these, please open the files in your web browser.

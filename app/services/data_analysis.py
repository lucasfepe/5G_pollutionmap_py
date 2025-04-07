import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

class PollutionAnalyzer:
    @staticmethod
    def process_historical_data(data):
        
        # Convert to DataFrame
        df = pd.DataFrame(data['results'])
        if data and 'results' in data and len(data['results']) > 0:
            print("First result:\n" + json.dumps(data['results'][0], indent=2, ensure_ascii=False))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')

        # Group by pollutant and timestamp
        df_grouped = df.pivot_table(
            index='timestamp',
            columns='pollutant',
            values='value',
            aggfunc='mean'
        )
        
        # Resample each pollutant to hourly data and interpolate missing values
        df_resampled = df_grouped.resample('1H').mean()
        df_resampled = df_resampled.interpolate(method='linear')
        
        return df_resampled

    @staticmethod
    def generate_predictions(historical_data, days_to_predict=5):
        predictions = {}
        
        for pollutant in historical_data.columns:
            # Get the series for this pollutant
            series = historical_data[pollutant]
            
            # Calculate trend using linear regression
            x = np.arange(len(series)).reshape(-1, 1)
            y = series.values.reshape(-1, 1)
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(x, y)
            
            # Generate future dates
            last_date = historical_data.index[-1]
            future_dates = pd.date_range(
                start=last_date + timedelta(hours=1),
                periods=days_to_predict * 24,
                freq='H'
            )
            
            # Generate predictions
            future_x = np.arange(len(series), len(series) + len(future_dates)).reshape(-1, 1)
            future_y = model.predict(future_x)
            
            # Add some daily patterns based on historical patterns
            if len(series) >= 24:
                daily_pattern = series.groupby(series.index.hour).mean()
                pattern_indices = [hour for hour in future_dates.hour]
                pattern_values = [daily_pattern[hour] for hour in pattern_indices]
                future_y = future_y.flatten() * 0.7 + np.array(pattern_values) * 0.3
            
            predictions[pollutant] = pd.Series(future_y, index=future_dates)
        
        return predictions

    @staticmethod
    def analyze_trends(data):
        analysis = {}
        
        for pollutant in data.columns:
            series = data[pollutant]
            analysis[pollutant] = {
                'mean': series.mean(),
                'std': series.std(),
                'min': series.min(),
                'max': series.max(),
                'trend': 'increasing' if series.iloc[-1] > series.iloc[0] else 'decreasing',
                'percent_change': ((series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100)
                    if series.iloc[0] != 0 else 0
            }
        
        return analysis

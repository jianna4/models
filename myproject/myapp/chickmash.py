import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
import numpy as np
from datetime import datetime
import os

class ChickMashPredictor:
    def __init__(self):
        self.model_path = r'F:\Program Files\projects\book2\myproject\myapp\chick_mash_price_prophet_model.pkl'
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained Prophet model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print("✅ Chick Mash Prophet model loaded successfully")
            else:
                raise Exception(f"Model file not found: {self.model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise Exception(f"Failed to load model: {e}")
    
    def predict_year(self, year):
        """Predict prices for all months of a year"""
        try:
            predictions = []
            for month in range(1, 13):
                prediction = self._predict_month(year, month)
                predictions.append(prediction)
            return predictions
        except Exception as e:
            raise Exception(f"Year prediction failed: {e}")
    
    def _predict_month(self, year, month):
        """Predict price for a specific month"""
        try:
            target_date = datetime(year, month, 1)
            last_training_date = pd.to_datetime('2024-12-01')
            months_ahead = (target_date.year - last_training_date.year) * 12 + (target_date.month - last_training_date.month)
            
            if months_ahead <= 0:
                return {
                    'month': target_date.strftime('%B'),
                    'year': year,
                    'predicted_price': 0,
                    'note': 'Historical data'
                }
            
            future = self.model.make_future_dataframe(periods=months_ahead, freq='M')
            forecast = self.model.predict(future)
            
            target_prediction = forecast[forecast['ds'].dt.to_period('M') == pd.Period(target_date, freq='M')]
            
            if len(target_prediction) == 0:
                raise ValueError(f"No prediction found for {target_date.strftime('%B %Y')}")
            
            prediction_data = target_prediction.iloc[0]
            
            return {
                'month': target_date.strftime('%B'),
                'year': year,
                'predicted_price': round(float(prediction_data['yhat']), 2),
                'lower_bound': round(float(prediction_data['yhat_lower']), 2),
                'upper_bound': round(float(prediction_data['yhat_upper']), 2),
            }
        except Exception as e:
            raise Exception(f"Month prediction failed: {e}")
    
    def get_best_months(self, year):
        """Get best months to buy and sell"""
        try:
            predictions = self.predict_year(year)
            
            # Sort by price
            sorted_predictions = sorted(predictions, key=lambda x: x['predicted_price'])
            
            best_buy = sorted_predictions[:3]  # Cheapest months
            best_sell = sorted_predictions[-3:]  # Most expensive months
            
            # Calculate profit potential
            avg_buy = sum([m['predicted_price'] for m in best_buy]) / 3
            avg_sell = sum([m['predicted_price'] for m in best_sell]) / 3
            profit_margin = ((avg_sell - avg_buy) / avg_buy) * 100
            
            return {
                'year': year,
                'best_buy_months': [
                    {
                        'month': month['month'],
                        'price': month['predicted_price'],
                        'reason': self._get_buy_reason(month['month'])
                    } for month in best_buy
                ],
                'best_sell_months': [
                    {
                        'month': month['month'],
                        'price': month['predicted_price'],
                        'reason': self._get_sell_reason(month['month'])
                    } for month in best_sell
                ],
                'profit_analysis': {
                    'average_buy_price': round(avg_buy, 2),
                    'average_sell_price': round(avg_sell, 2),
                    'potential_profit_margin': round(profit_margin, 2),
                    'annual_low': best_buy[0]['predicted_price'],
                    'annual_high': best_sell[-1]['predicted_price']
                }
            }
        except Exception as e:
            raise Exception(f"Best months analysis failed: {e}")
    
    def get_multi_year_predictions(self, years=3):
        """Get predictions for multiple years"""
        try:
            current_year = datetime.now().year
            all_predictions = {}
            
            for year in range(current_year, current_year + years):
                predictions = self.predict_year(year)
                all_predictions[year] = predictions
            
            return all_predictions
        except Exception as e:
            raise Exception(f"Multi-year prediction failed: {e}")
    
    def generate_price_chart(self, years=3):
        """Generate price chart for multiple years"""
        try:
            predictions = self.get_multi_year_predictions(years)
            
            plt.figure(figsize=(14, 8))
            
            # Prepare data for chart
            all_months = []
            all_prices = []
            
            for year, months_data in predictions.items():
                for month_data in months_data:
                    label = f"{month_data['month'][:3]} {str(year)[-2:]}"
                    all_months.append(label)
                    all_prices.append(month_data['predicted_price'])
            
            # Create the chart
            plt.plot(all_months, all_prices, 'bo-', linewidth=2, markersize=4, label='Predicted Price')
            
            # Add labels and styling
            plt.title('Chicken Mash Price Predictions', fontsize=16, fontweight='bold', pad=20)
            plt.ylabel('Price (KSh/Kg)', fontsize=12)
            plt.xlabel('Time (Months)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            
            # Save chart
            chart_path = f'chickmash_predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            raise Exception(f"Chart generation failed: {e}")
    
    def _get_buy_reason(self, month):
        reasons = {
            'January': 'Post-holiday prices usually drop',
            'February': 'Short month, stable low prices',
            'March': 'Before peak season price rise',
            'April': 'Good pre-rainy season prices',
            'May': 'Planting season, lower demand',
            'June': 'Mid-year price stability',
            'July': 'Strategic buying opportunity',
            'August': 'Pre-harvest favorable prices',
            'September': 'Harvest begins, supply increases',
            'October': 'Typically the lowest prices',
            'November': 'Before holiday price surge',
            'December': 'Avoid - holiday premium prices'
        }
        return reasons.get(month, 'Good buying conditions')
    
    def _get_sell_reason(self, month):
        reasons = {
            'January': 'New year demand recovery',
            'February': 'Valentine season demand',
            'March': 'Peak season highest prices',
            'April': 'Easter holiday demand',
            'May': 'Pre-planting demand spike',
            'June': 'Mid-year budget spending',
            'July': 'Stable high demand period',
            'August': 'Back-to-school demand',
            'September': 'Post-harvest demand rise',
            'October': 'Pre-holiday stocking begins',
            'November': 'Holiday preparation peak',
            'December': 'Highest holiday season prices'
        }
        return reasons.get(month, 'High demand period')

# Global instance
chickmash_predictor = ChickMashPredictor()
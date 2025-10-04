from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from datetime import datetime
import os
from .chickmash import chickmash_predictor

def best_buy_months(request):
    """Get best months to buy chicken mash"""
    try:
        year = int(request.GET.get('year', datetime.now().year))
        
        if year < datetime.now().year:
            return JsonResponse({
                'success': False,
                'error': 'Cannot analyze past years'
            }, status=400)
        
        result = chickmash_predictor.get_best_months(year)
        
        return JsonResponse({
            'success': True,
            'data': {
                'best_buy_months': result['best_buy_months'],
                'profit_analysis': result['profit_analysis'],
                'year': year
            },
            'message': f'Best months to buy chicken mash in {year}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def best_sell_months(request):
    """Get best months to sell chicken mash"""
    try:
        year = int(request.GET.get('year', datetime.now().year))
        
        if year < datetime.now().year:
            return JsonResponse({
                'success': False,
                'error': 'Cannot analyze past years'
            }, status=400)
        
        result = chickmash_predictor.get_best_months(year)
        
        return JsonResponse({
            'success': True,
            'data': {
                'best_sell_months': result['best_sell_months'],
                'profit_analysis': result['profit_analysis'],
                'year': year
            },
            'message': f'Best months to sell chicken mash in {year}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def price_predictions(request):
    """Get price predictions for multiple years"""
    try:
        years = int(request.GET.get('years', 3))
        
        predictions = chickmash_predictor.get_multi_year_predictions(years)
        
        return JsonResponse({
            'success': True,
            'data': predictions,
            'message': f'Price predictions for next {years} years'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def generate_price_chart(request):
    """Generate and return price chart"""
    try:
        years = int(request.GET.get('years', 3))
        
        chart_path = chickmash_predictor.generate_price_chart(years)
        
        return JsonResponse({
            'success': True,
            'data': {
                'chart_path': chart_path,
                'chart_url': f'/media/{os.path.basename(chart_path)}'
            },
            'message': f'Price chart generated for {years} years'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def complete_analysis(request):
    """Get complete analysis: best buy/sell + predictions"""
    try:
        year = int(request.GET.get('year', datetime.now().year))
        chart_years = int(request.GET.get('chart_years', 3))
        
        # Get best months
        best_months = chickmash_predictor.get_best_months(year)
        
        # Get multi-year predictions
        predictions = chickmash_predictor.get_multi_year_predictions(chart_years)
        
        # Generate chart
        chart_path = chickmash_predictor.generate_price_chart(chart_years)
        
        return JsonResponse({
            'success': True,
            'data': {
                'year_analysis': best_months,
                'multi_year_predictions': predictions,
                'chart_info': {
                    'path': chart_path,
                    'url': f'/media/{os.path.basename(chart_path)}'
                }
            },
            'message': f'Complete chicken mash analysis for {year}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add parent directory to path to import from results
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

app = Flask(__name__)
CORS(app)

class OilDataAPI:
    """API for serving Brent oil price analysis data from your existing results"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.load_data()
    
    def load_data(self):
        """Load data from your existing Task 2 results"""
        print(f"Base path: {self.base_path}")
        
        # Load cleaned price data from Task 2 results
        price_path = self.base_path / "results" / "change_point_analysis" / "brent_oil_cleaned.csv"
        if price_path.exists():
            self.price_data = pd.read_csv(price_path)
            self.price_data['date'] = pd.to_datetime(self.price_data['date'])
            print(f"Loaded {len(self.price_data)} price records")
        else:
            # Fallback: Use raw data
            raw_path = self.base_path / "data" / "raw" / "BrentOilPrices.csv"
            self.price_data = pd.read_csv(raw_path)
            self.price_data.columns = ['date', 'price']
            self.price_data['date'] = pd.to_datetime(self.price_data['date'])
            print(f"Loaded {len(self.price_data)} raw price records")
        
        # Load events data (create if doesn't exist)
        self.load_or_create_events()
        
        # Calculate metrics
        self.calculate_metrics()
        
        # Try to load change point results
        self.load_change_points()
    
    def load_or_create_events(self):
        """Load or create events data"""
        events_path = self.base_path / "results" / "events.csv"
        
        if events_path.exists():
            self.events_data = pd.read_csv(events_path)
        else:
            # Create events data based on known historical events
            events = [
                {'id': 1, 'date': '1990-08-02', 'name': 'Iraq invades Kuwait', 'type': 'Geopolitical', 'region': 'Middle East', 'severity': 'High'},
                {'id': 2, 'date': '1997-11-30', 'name': 'Asian Financial Crisis', 'type': 'Financial', 'region': 'Asia', 'severity': 'Medium'},
                {'id': 3, 'date': '2001-09-11', 'name': '9/11 Attacks', 'type': 'Geopolitical', 'region': 'Global', 'severity': 'High'},
                {'id': 4, 'date': '2003-03-20', 'name': 'Iraq War begins', 'type': 'Geopolitical', 'region': 'Middle East', 'severity': 'High'},
                {'id': 5, 'date': '2005-08-29', 'name': 'Hurricane Katrina', 'type': 'Natural Disaster', 'region': 'North America', 'severity': 'High'},
                {'id': 6, 'date': '2008-09-15', 'name': 'Lehman Brothers Collapse', 'type': 'Financial', 'region': 'Global', 'severity': 'High'},
                {'id': 7, 'date': '2011-02-15', 'name': 'Arab Spring', 'type': 'Geopolitical', 'region': 'Middle East', 'severity': 'Medium'},
                {'id': 8, 'date': '2014-06-01', 'name': 'Oil Price Crash', 'type': 'Market', 'region': 'Global', 'severity': 'High'},
                {'id': 9, 'date': '2015-12-04', 'name': 'OPEC maintains production', 'type': 'Policy', 'region': 'Global', 'severity': 'Medium'},
                {'id': 10, 'date': '2016-11-30', 'name': 'OPEC production cuts', 'type': 'Policy', 'region': 'Global', 'severity': 'High'},
                {'id': 11, 'date': '2020-03-01', 'name': 'COVID-19 Pandemic', 'type': 'Health', 'region': 'Global', 'severity': 'High'},
                {'id': 12, 'date': '2022-02-24', 'name': 'Russia-Ukraine War', 'type': 'Geopolitical', 'region': 'Europe', 'severity': 'High'},
            ]
            self.events_data = pd.DataFrame(events)
            self.events_data['date'] = pd.to_datetime(self.events_data['date'])
            
            # Save for future use
            events_path.parent.mkdir(parents=True, exist_ok=True)
            self.events_data.to_csv(events_path, index=False)
            print(f"Created and saved events data: {len(self.events_data)} events")
    
    def load_change_points(self):
        """Load change point results from Task 2"""
        cp_path = self.base_path / "results" / "change_point_results.json"
        if cp_path.exists():
            with open(cp_path, 'r') as f:
                self.change_points = json.load(f)
            print("Loaded change point results")
        else:
            # Create mock change points if file doesn't exist
            self.change_points = {
                'change_point': {
                    'index': 5000,
                    'date': '2014-06-15',
                    'description': 'Oil price crash structural break'
                },
                'impact': {
                    'price_before': 105.32,
                    'price_after': 48.76,
                    'price_change_pct': -53.7
                }
            }
            print("Using mock change point data")
    
    def calculate_metrics(self):
        """Calculate key metrics for dashboard"""
        # Ensure data is sorted
        self.price_data = self.price_data.sort_values('date')
        
        # Calculate returns
        self.price_data['daily_return'] = self.price_data['price'].pct_change()
        self.price_data['log_return'] = np.log(self.price_data['price']).diff()
        
        # Rolling statistics
        self.price_data['rolling_mean_30d'] = self.price_data['price'].rolling(window=30).mean()
        self.price_data['rolling_volatility_30d'] = self.price_data['log_return'].rolling(window=30).std() * np.sqrt(252)
        
        # Remove NaN values
        self.price_data = self.price_data.dropna(subset=['log_return'])
    
    def get_price_data(self, start_date=None, end_date=None, limit=5000):
        """Get historical price data with optional date filtering"""
        df = self.price_data.copy()
        
        if start_date:
            df = df[df['date'] >= pd.Timestamp(start_date)]
        
        if end_date:
            df = df[df['date'] <= pd.Timestamp(end_date)]
        
        # Limit for performance
        if len(df) > limit:
            step = len(df) // limit
            df = df.iloc[::step]
        
        return df.to_dict('records')
    
    def get_events(self, event_type=None, start_date=None, end_date=None):
        """Get events with optional filtering"""
        df = self.events_data.copy()
        
        if event_type and event_type != 'all':
            df = df[df['type'] == event_type]
        
        if start_date:
            df = df[df['date'] >= pd.Timestamp(start_date)]
        
        if end_date:
            df = df[df['date'] <= pd.Timestamp(end_date)]
        
        return df.to_dict('records')
    
    def get_change_points(self):
        """Get change point analysis results"""
        return self.change_points
    
    def get_summary_stats(self):
        """Get summary statistics"""
        stats = {
            'date_range': {
                'start': self.price_data['date'].min().strftime('%Y-%m-%d'),
                'end': self.price_data['date'].max().strftime('%Y-%m-%d')
            },
            'price_stats': {
                'min': float(self.price_data['price'].min()),
                'max': float(self.price_data['price'].max()),
                'mean': float(self.price_data['price'].mean()),
                'median': float(self.price_data['price'].median()),
                'std': float(self.price_data['price'].std()),
                'current': float(self.price_data['price'].iloc[-1])
            },
            'returns': {
                'mean_daily_return': float(self.price_data['daily_return'].mean()),
                'volatility': float(self.price_data['rolling_volatility_30d'].iloc[-1])
            }
        }
        return stats
    
    def get_event_impact(self, event_id):
        """Calculate impact of a specific event"""
        event = self.events_data[self.events_data['id'] == int(event_id)]
        if len(event) == 0:
            return None
        
        event = event.iloc[0]
        event_date = event['date']
        
        # Window around event (30 days before and after)
        window = 30
        start_date = event_date - timedelta(days=window)
        end_date = event_date + timedelta(days=window)
        
        # Get price data around event
        mask = (self.price_data['date'] >= start_date) & (self.price_data['date'] <= end_date)
        event_data = self.price_data[mask].copy()
        
        if len(event_data) == 0:
            return None
        
        # Calculate days from event
        event_data['days_from_event'] = (event_data['date'] - event_date).dt.days
        
        # Calculate before/after metrics
        before_event = event_data[event_data['days_from_event'] < 0]
        after_event = event_data[event_data['days_from_event'] > 0]
        
        price_before = float(before_event['price'].mean()) if len(before_event) > 0 else None
        price_after = float(after_event['price'].mean()) if len(after_event) > 0 else None
        
        impact = {
            'event': event.to_dict(),
            'price_before': price_before,
            'price_after': price_after,
            'price_change_pct': None,
            'data_points': event_data.head(100).to_dict('records')  # Limit for performance
        }
        
        if price_before and price_after:
            impact['price_change_pct'] = ((price_after - price_before) / price_before * 100)
        
        return impact

# Initialize API
api = OilDataAPI()

# API Routes
@app.route('/')
def index():
    return jsonify({
        'message': 'Brent Oil Price Dashboard API',
        'status': 'running',
        'data_stats': {
            'price_records': len(api.price_data),
            'events': len(api.events_data),
            'date_range': f"{api.price_data['date'].min().date()} to {api.price_data['date'].max().date()}"
        }
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = int(request.args.get('limit', 5000))
    
    data = api.get_price_data(start_date, end_date, limit)
    return jsonify({
        'success': True,
        'count': len(data),
        'data': data
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    event_type = request.args.get('type', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    data = api.get_events(event_type, start_date, end_date)
    return jsonify({
        'success': True,
        'count': len(data),
        'data': data
    })

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    data = api.get_change_points()
    return jsonify({
        'success': True,
        'data': data
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = api.get_summary_stats()
    return jsonify({
        'success': True,
        'data': data
    })

@app.route('/api/event-impact/<event_id>', methods=['GET'])
def get_event_impact(event_id):
    try:
        data = api.get_event_impact(event_id)
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/event-types', methods=['GET'])
def get_event_types():
    types = api.events_data['type'].unique().tolist()
    return jsonify({
        'success': True,
        'data': types
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("BRENT OIL PRICE DASHBOARD API")
    print("="*60)
    print(f"Price data: {len(api.price_data)} records")
    print(f"Events data: {len(api.events_data)} events")
    print(f"Date range: {api.price_data['date'].min().date()} to {api.price_data['date'].max().date()}")
    print(f"API running on: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
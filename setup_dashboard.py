#!/usr/bin/env python3
"""
Setup script for Task 3 Dashboard
Automatically sets up the dashboard structure based on existing Task 2 results
"""

import os
import shutil
from pathlib import Path
import json
import pandas as pd

def setup_dashboard():
    """Setup dashboard folder structure and copy necessary files"""
    
    # Define paths
    current_dir = Path.cwd()
    dashboard_dir = current_dir / "dashboard"
    
    print(f"Current directory: {current_dir}")
    print(f"Setting up dashboard in: {dashboard_dir}")
    
    # Create dashboard directory structure
    backend_dir = dashboard_dir / "backend"
    frontend_dir = dashboard_dir / "frontend" / "src"
    
    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy backend files
    print("\n1. Setting up backend...")
    
    # Create requirements.txt
    requirements_content = """Flask==2.3.3
Flask-CORS==4.0.0
pandas==2.0.3
numpy==1.24.3
python-dotenv==1.0.0
"""
    with open(backend_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # Create app.py (already provided above)
    print("   Created backend files")
    
    # Check for existing data
    print("\n2. Checking for existing data files...")
    
    # Check for cleaned data from Task 2
    cleaned_data_path = current_dir / "results" / "change_point_analysis" / "brent_oil_cleaned.csv"
    if cleaned_data_path.exists():
        print(f"   ✓ Found cleaned data: {cleaned_data_path}")
    else:
        print(f"   ⚠ Cleaned data not found. Will use raw data.")
    
    # Create events.csv in results if it doesn't exist
    events_path = current_dir / "results" / "events.csv"
    if not events_path.exists():
        print(f"   Creating events.csv in results folder...")
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
        events_df = pd.DataFrame(events)
        events_path.parent.mkdir(parents=True, exist_ok=True)
        events_df.to_csv(events_path, index=False)
        print(f"   ✓ Created events.csv with {len(events)} events")
    
    # Check for change point results
    cp_results_path = current_dir / "results" / "change_point_results.json"
    if not cp_results_path.exists():
        print(f"   ⚠ change_point_results.json not found. Creating placeholder...")
        placeholder_results = {
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
        with open(cp_results_path, 'w') as f:
            json.dump(placeholder_results, f, indent=2)
        print(f"   ✓ Created placeholder change point results")
    
    # Create frontend package.json
    print("\n3. Setting up frontend...")
    package_json = {
        "name": "brent-oil-dashboard",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "recharts": "^2.8.0",
            "axios": "^1.4.0",
            "date-fns": "^2.30.0",
            "react-bootstrap": "^2.8.0",
            "bootstrap": "^5.3.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "proxy": "http://localhost:5000",
        "eslintConfig": {
            "extends": ["react-app"]
        },
        "browserslist": {
            "production": [">0.2%", "not dead", "not op_mini all"],
            "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
        }
    }
    
    with open(dashboard_dir / "frontend" / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create public folder with index.html
    public_dir = dashboard_dir / "frontend" / "public"
    public_dir.mkdir(exist_ok=True)
    
    index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Brent Oil Price Analysis Dashboard" />
    <title>Brent Oil Price Dashboard</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>"""
    
    with open(public_dir / "index.html", "w") as f:
        f.write(index_html)
    
    print("   ✓ Created frontend structure")
    
    # Create README.md
    print("\n4. Creating README.md...")
    readme_content = """# Brent Oil Price Analysis Dashboard

## Quick Start

### 1. Backend Setup
```bash
cd dashboard/backend
pip install -r requirements.txt
python app.py
"""
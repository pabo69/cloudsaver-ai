#!/usr/bin/env python3
"""
Fetch AWS costs from Cost Explorer API
"""
import boto3
from datetime import datetime, timedelta
import json

def fetch_aws_costs(days=1):
    """
    Fetch AWS costs for the last N days
    """
    # Create Cost Explorer client
    ce = boto3.client('ce', region_name='us-east-1')
    
    # Calculate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Format dates for API (YYYY-MM-DD)
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    
    print(f"Fetching costs from {start} to {end}...")
    
    try:
        # Call Cost Explorer API
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End': end
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        
        print("✓ Successfully fetched cost data!")
        return response
        
    except Exception as e:
        print(f"✗ Error fetching costs: {e}")
        return None

if __name__ == "__main__":
    # Fetch costs
    data = fetch_aws_costs(days=1)
    
    if data:
        # Save to file for inspection
        with open('aws_costs_raw.json', 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print("✓ Saved raw data to aws_costs_raw.json")
        
        # Print summary
        print("\n=== COST SUMMARY ===")
        for result in data.get('ResultsByTime', [])[:3]:  # First 3 days
            date = result['TimePeriod']['Start']
            print(f"\nDate: {date}")
            for group in result.get('Groups', [])[:5]:  # Top 5 services
                service = group['Keys'][0]
                cost = group['Metrics']['UnblendedCost']['Amount']
                print(f"  {service}: ${float(cost):.2f}")
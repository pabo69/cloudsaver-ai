#!/usr/bin/env python3
"""
Mock AWS cost data for testing when real data isn't available
"""
from datetime import datetime, timedelta
import random

def generate_mock_costs(days=30):
    """Generate realistic-looking AWS cost data"""
    
    services = [
        'Amazon EC2',
        'Amazon RDS', 
        'Amazon S3',
        'AWS Lambda',
        'Amazon CloudFront',
        'Amazon DynamoDB',
        'AWS Data Transfer',
        'Amazon ECS',
        'Amazon VPC',
        'Amazon Route 53'
    ]
    
    results_by_time = []
    end_date = datetime.now().date()
    
    for i in range(days):
        date = end_date - timedelta(days=days - i - 1)
        
        groups = []
        for service in services:
            # Random cost between $0.50 and $50
            cost = round(random.uniform(0.5, 50.0), 2)
            groups.append({
                'Keys': [service],
                'Metrics': {
                    'UnblendedCost': {
                        'Amount': str(cost),
                        'Unit': 'USD'
                    }
                }
            })
        
        results_by_time.append({
            'TimePeriod': {
                'Start': date.strftime('%Y-%m-%d'),
                'End': date.strftime('%Y-%m-%d')
            },
            'Groups': groups,
            'Total': {},
            'Estimated': False
        })
    
    return {
        'ResultsByTime': results_by_time,
        'DimensionValueAttributes': []
    }

if __name__ == "__main__":
    import json
    
    print("Generating mock data...")
    data = generate_mock_costs(30)
    
    # Save it
    with open('aws_costs_raw.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Created aws_costs_raw.json with mock data")
    print(f"✓ Generated {len(data['ResultsByTime'])} days of cost data")
    
    # Show summary
    total = 0
    for day in data['ResultsByTime']:
        for group in day['Groups']:
            total += float(group['Metrics']['UnblendedCost']['Amount'])
    
    print(f"✓ Total mock costs: ${total:.2f}")
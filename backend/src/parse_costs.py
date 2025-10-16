#!/usr/bin/env python3
"""
Parse AWS Cost Explorer response into clean data structure
"""
from datetime import datetime
from typing import List, Dict
import json

def parse_cost_data(raw_response: dict) -> List[Dict]:
    """
    Convert Cost Explorer API response to clean list of cost records
    
    Returns: List of dicts like:
    {
        'date': '2024-01-15',
        'service': 'Amazon EC2',
        'cost': 45.67
    }
    """
    parsed_records = []
    
    for time_period in raw_response.get('ResultsByTime', []):
        date = time_period['TimePeriod']['Start']
        
        for group in time_period.get('Groups', []):
            service = group['Keys'][0]
            cost_str = group['Metrics']['UnblendedCost']['Amount']
            cost = float(cost_str)
            
            # Only include costs > $0.01
            if cost >= 0.01:
                parsed_records.append({
                    'date': date,
                    'service': service,
                    'cost': round(cost, 2)
                })
    
    return parsed_records

def print_cost_summary(records: List[Dict]):
    """Print human-readable summary"""
    if not records:
        print("No cost data found")
        return
    
    # Group by service
    service_totals = {}
    for record in records:
        service = record['service']
        cost = record['cost']
        service_totals[service] = service_totals.get(service, 0) + cost
    
    # Sort by cost (highest first)
    sorted_services = sorted(service_totals.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
    
    print("\n=== TOP 10 SERVICES BY TOTAL COST ===")
    for service, total_cost in sorted_services[:10]:
        print(f"${total_cost:8.2f}  {service}")
    
    # Calculate total
    total = sum(service_totals.values())
    print(f"\n{'='*40}")
    print(f"TOTAL: ${total:.2f}")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    # Load the raw data we saved earlier
    with open('aws_costs_raw.json', 'r') as f:
        raw_data = json.load(f)
    
    # Parse it
    records = parse_cost_data(raw_data)
    
    print(f"Parsed {len(records)} cost records")
    
    # Print summary
    print_cost_summary(records)
    
    # Save parsed data
    with open('aws_costs_parsed.json', 'w') as f:
        json.dump(records, f, indent=2)
    print("✓ Saved parsed data to aws_costs_parsed.json")
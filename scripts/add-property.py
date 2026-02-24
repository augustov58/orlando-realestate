#!/usr/bin/env python3
"""
Add a property type/floor plan to a community.
Usage: python add-property.py --community "Name" --name "Floor Plan" --beds 4 --baths 3 --sqft 2500 --price 450000
"""

import sys
import argparse
from db import add_property_type, get_community_by_name, init_db, get_db

def main():
    parser = argparse.ArgumentParser(description='Add a property type to a community')
    parser.add_argument('--community', '-c', required=True, help='Community name')
    parser.add_argument('--builder', '-b', help='Builder name (to disambiguate)')
    parser.add_argument('--name', '-n', required=True, help='Floor plan name')
    parser.add_argument('--beds', type=int, help='Number of bedrooms')
    parser.add_argument('--baths', type=float, help='Number of bathrooms')
    parser.add_argument('--sqft', type=int, help='Square footage')
    parser.add_argument('--stories', type=int, default=1, help='Number of stories')
    parser.add_argument('--garage', type=int, default=2, help='Garage spaces')
    parser.add_argument('--price', type=float, help='Current price')
    parser.add_argument('--base-price', type=float, help='Base price (before options)')
    parser.add_argument('--inlaw', action='store_true', help='Has in-law suite')
    parser.add_argument('--url', '-u', help='Property page URL')
    parser.add_argument('--features', nargs='+', help='List of features')
    parser.add_argument('--notes', help='Notes')
    
    args = parser.parse_args()
    
    # Initialize DB
    init_db()
    
    # Find community
    community = get_community_by_name(args.community, args.builder)
    if not community:
        print(f"❌ Community not found: {args.community}")
        print("Available communities:")
        conn = get_db()
        cursor = conn.execute("SELECT name, builder FROM communities ORDER BY builder, name")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]})")
        conn.close()
        return 1
    
    # Add property type
    prop_id = add_property_type(
        community_id=community['id'],
        name=args.name,
        bedrooms=args.beds,
        bathrooms=args.baths,
        sqft=args.sqft,
        stories=args.stories,
        garage_spaces=args.garage,
        has_inlaw_suite=args.inlaw,
        base_price=args.base_price,
        current_price=args.price,
        url=args.url,
        features=args.features or [],
        notes=args.notes
    )
    
    if prop_id > 0:
        print(f"✅ Added floor plan: {args.name}")
        print(f"   Community: {community['name']} ({community['builder']})")
        print(f"   ID: {prop_id}")
        print(f"   {args.beds or '?'}BR | {args.baths or '?'}BA | {args.sqft or '?'} sqft")
        if args.price:
            print(f"   Price: ${args.price:,.0f}")
        if args.inlaw:
            print(f"   🏠👴 Has In-Law Suite")
        return 0
    else:
        print(f"❌ Failed to add (may already exist in this community)")
        return 1

if __name__ == '__main__':
    sys.exit(main())

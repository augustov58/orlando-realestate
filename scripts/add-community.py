#!/usr/bin/env python3
"""
Add a community to the Orlando real estate database.
Usage: python add-community.py "Community Name" "Builder" "City" "https://url"
"""

import sys
import argparse
from db import add_community, init_db, get_community_by_name

def main():
    parser = argparse.ArgumentParser(description='Add a community to the database')
    parser.add_argument('name', help='Community name')
    parser.add_argument('builder', help='Builder name (e.g., Lennar, DR Horton)')
    parser.add_argument('--city', '-c', help='City/area')
    parser.add_argument('--url', '-u', help='Community URL')
    parser.add_argument('--zip', '-z', help='ZIP code')
    parser.add_argument('--address', '-a', help='Address')
    parser.add_argument('--hoa', type=float, help='HOA monthly fee')
    parser.add_argument('--lat', type=float, help='Latitude')
    parser.add_argument('--lng', type=float, help='Longitude')
    parser.add_argument('--amenities', nargs='+', help='List of amenities')
    parser.add_argument('--notes', '-n', help='Notes')
    
    args = parser.parse_args()
    
    # Initialize DB if needed
    init_db()
    
    # Check if exists
    existing = get_community_by_name(args.name, args.builder)
    if existing:
        print(f"❌ Community already exists: {args.name} by {args.builder}")
        print(f"   ID: {existing['id']}")
        return 1
    
    # Add community
    community_id = add_community(
        name=args.name,
        builder=args.builder,
        city=args.city,
        url=args.url,
        zip_code=args.zip,
        address=args.address,
        hoa_monthly=args.hoa,
        lat=args.lat,
        lng=args.lng,
        amenities=args.amenities or [],
        notes=args.notes
    )
    
    if community_id > 0:
        print(f"✅ Added community: {args.name} by {args.builder}")
        print(f"   ID: {community_id}")
        print(f"   City: {args.city or 'N/A'}")
        print(f"   URL: {args.url or 'N/A'}")
        return 0
    else:
        print(f"❌ Failed to add community (may be duplicate)")
        return 1

if __name__ == '__main__':
    sys.exit(main())

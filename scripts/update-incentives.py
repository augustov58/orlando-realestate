#!/usr/bin/env python3
"""
Add or update builder incentives.
Usage: python update-incentives.py --builder "Lennar" --rate-buydown "5.99%" --closing-credit 15000
"""

import sys
import argparse
from db import add_incentive, get_community_by_name, get_active_incentives, init_db, get_db

def main():
    parser = argparse.ArgumentParser(description='Add a builder incentive')
    parser.add_argument('--builder', '-b', required=True, help='Builder name')
    parser.add_argument('--community', '-c', help='Community name (optional, for community-specific)')
    parser.add_argument('--type', '-t', default='rate_buydown', 
                        choices=['rate_buydown', 'closing_credit', 'price_reduction', 'upgrade', 'combo'],
                        help='Incentive type')
    parser.add_argument('--description', '-d', help='Description of the incentive')
    parser.add_argument('--rate-buydown', help='Rate buydown (e.g., "5.99%", "2-1 buydown")')
    parser.add_argument('--rate-after', type=float, help='Rate after buydown (e.g., 5.99)')
    parser.add_argument('--closing-credit', type=float, help='Closing cost credit amount')
    parser.add_argument('--other-value', type=float, help='Other value (upgrades, etc.)')
    parser.add_argument('--terms', help='Terms and conditions')
    parser.add_argument('--lender', help='Required lender (if any)')
    parser.add_argument('--expires', help='Expiration date (YYYY-MM-DD)')
    parser.add_argument('--source-url', help='Source URL')
    
    args = parser.parse_args()
    
    init_db()
    
    # Find community if specified
    community_id = None
    if args.community:
        community = get_community_by_name(args.community)
        if community:
            community_id = community['id']
        else:
            print(f"⚠️ Community '{args.community}' not found, adding as builder-wide incentive")
    
    # Add incentive
    incentive_id = add_incentive(
        builder=args.builder,
        community_id=community_id,
        type=args.type,
        description=args.description,
        rate_buydown=args.rate_buydown,
        rate_after_buydown=args.rate_after,
        closing_credit=args.closing_credit,
        other_value=args.other_value,
        terms=args.terms,
        lender_required=args.lender,
        expires_at=args.expires,
        source_url=args.source_url
    )
    
    print(f"✅ Added incentive for {args.builder}")
    print(f"   ID: {incentive_id}")
    if args.rate_buydown:
        print(f"   Rate: {args.rate_buydown}")
    if args.closing_credit:
        print(f"   Closing Credit: ${args.closing_credit:,.0f}")
    if args.expires:
        print(f"   Expires: {args.expires}")
    if community_id:
        print(f"   Community: {args.community}")
    else:
        print(f"   Applies to: All {args.builder} communities")
    
    # Show current active incentives
    print(f"\n📋 Active {args.builder} Incentives:")
    for inc in get_active_incentives(builder=args.builder):
        comm = f" - {inc['community_name']}" if inc.get('community_name') else " (all communities)"
        rate = f" | Rate: {inc['rate_buydown']}" if inc.get('rate_buydown') else ""
        credit = f" | Credit: ${inc['closing_credit']:,.0f}" if inc.get('closing_credit') else ""
        print(f"   • {args.builder}{comm}{rate}{credit}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

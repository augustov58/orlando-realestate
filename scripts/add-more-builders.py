#!/usr/bin/env python3
"""Add more builders to the Orlando database"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, add_incentive, get_community_by_name

init_db()

# DR Horton communities - America's largest homebuilder
DR_HORTON_DATA = [
    {
        "community": "Astonia",
        "city": "Davenport",
        "url": "https://www.drhorton.com/florida/orlando-metro/davenport/astonia",
        "properties": [
            {"name": "Bluebell", "beds": 4, "baths": 2, "sqft": 1850, "price": 319990},
            {"name": "Dahlia", "beds": 4, "baths": 2.5, "sqft": 2150, "price": 349990},
            {"name": "Lantana", "beds": 5, "baths": 3, "sqft": 2580, "price": 389990},
        ]
    },
    {
        "community": "Sunstone",
        "city": "Sanford",
        "url": "https://www.drhorton.com/florida/orlando-metro/sanford/sunstone",
        "properties": [
            {"name": "Columbia", "beds": 4, "baths": 2, "sqft": 1875, "price": 359990},
            {"name": "Helena", "beds": 4, "baths": 3, "sqft": 2340, "price": 399990},
            {"name": "Juniper", "beds": 5, "baths": 3, "sqft": 2650, "price": 439990},
        ]
    },
    {
        "community": "Storey Creek",
        "city": "Kissimmee",
        "url": "https://www.drhorton.com/florida/orlando-metro/kissimmee/storey-creek",
        "properties": [
            {"name": "Aria", "beds": 4, "baths": 2.5, "sqft": 2100, "price": 385990},
            {"name": "Melody", "beds": 5, "baths": 3, "sqft": 2450, "price": 425990},
        ]
    },
    {
        "community": "Crescent Ridge",
        "city": "Clermont",
        "url": "https://www.drhorton.com/florida/orlando-metro/clermont/crescent-ridge",
        "properties": [
            {"name": "Serenity", "beds": 4, "baths": 3, "sqft": 2200, "price": 429990},
            {"name": "Harmony", "beds": 5, "baths": 3.5, "sqft": 2750, "price": 489990},
        ]
    },
    {
        "community": "Citrus Trails",
        "city": "Haines City",
        "url": "https://www.drhorton.com/florida/orlando-metro/haines-city/citrus-trails",
        "properties": [
            {"name": "Jasmine", "beds": 4, "baths": 2, "sqft": 1750, "price": 289990},
            {"name": "Magnolia", "beds": 4, "baths": 2.5, "sqft": 2050, "price": 319990},
            {"name": "Willow", "beds": 5, "baths": 3, "sqft": 2400, "price": 359990},
        ]
    },
]

# Meritage Homes - Energy efficient builder
MERITAGE_DATA = [
    {
        "community": "Rivington",
        "city": "Debary",
        "url": "https://www.meritagehomes.com/state/fl/orlando/rivington",
        "properties": [
            {"name": "Saguaro", "beds": 4, "baths": 3, "sqft": 2180, "price": 429900},
            {"name": "Cabo", "beds": 4, "baths": 3.5, "sqft": 2450, "price": 469900},
            {"name": "Sedona", "beds": 5, "baths": 3, "sqft": 2780, "price": 509900},
        ]
    },
    {
        "community": "Lake Apopka Reserve",
        "city": "Apopka",
        "url": "https://www.meritagehomes.com/state/fl/orlando/lake-apopka-reserve",
        "properties": [
            {"name": "Cholla", "beds": 4, "baths": 2.5, "sqft": 2050, "price": 399900},
            {"name": "Palo Verde", "beds": 4, "baths": 3, "sqft": 2350, "price": 449900},
        ]
    },
    {
        "community": "Cypress Preserve",
        "city": "Groveland",
        "url": "https://www.meritagehomes.com/state/fl/orlando/cypress-preserve",
        "properties": [
            {"name": "Acacia", "beds": 4, "baths": 2.5, "sqft": 1950, "price": 369900},
            {"name": "Ironwood", "beds": 5, "baths": 3, "sqft": 2550, "price": 429900},
        ]
    },
]

# Taylor Morrison
TAYLOR_MORRISON_DATA = [
    {
        "community": "Hammock Trails",
        "city": "Kissimmee",
        "url": "https://www.taylormorrison.com/new-homes/florida/orlando/kissimmee/hammock-trails",
        "properties": [
            {"name": "Ashbury", "beds": 4, "baths": 3, "sqft": 2250, "price": 419990},
            {"name": "Brentwood", "beds": 5, "baths": 3.5, "sqft": 2680, "price": 479990},
        ]
    },
    {
        "community": "Waterleigh",
        "city": "Winter Garden",
        "url": "https://www.taylormorrison.com/new-homes/florida/orlando/winter-garden/waterleigh",
        "properties": [
            {"name": "Camellia", "beds": 4, "baths": 3, "sqft": 2400, "price": 499990},
            {"name": "Dogwood", "beds": 5, "baths": 4, "sqft": 2850, "price": 549990},
        ]
    },
]

# Pulte Homes
PULTE_DATA = [
    {
        "community": "Summerlake",
        "city": "Winter Garden",
        "url": "https://www.pulte.com/homes/florida/orlando/winter-garden/summerlake",
        "properties": [
            {"name": "Riviera", "beds": 4, "baths": 3, "sqft": 2368, "price": 469990},
            {"name": "Summerwood", "beds": 5, "baths": 3, "sqft": 2650, "price": 519990},
        ]
    },
    {
        "community": "Reunion",
        "city": "Kissimmee",
        "url": "https://www.pulte.com/homes/florida/orlando/kissimmee/reunion",
        "properties": [
            {"name": "Ashby", "beds": 4, "baths": 3, "sqft": 2298, "price": 489990},
            {"name": "Roseland", "beds": 5, "baths": 4, "sqft": 2810, "price": 539990},
        ]
    },
    {
        "community": "Creekside",
        "city": "Saint Cloud",
        "url": "https://www.pulte.com/homes/florida/orlando/saint-cloud/creekside",
        "properties": [
            {"name": "Whitestone", "beds": 4, "baths": 2.5, "sqft": 2150, "price": 419990},
            {"name": "Palmetto", "beds": 4, "baths": 3, "sqft": 2380, "price": 449990},
        ]
    },
]

# KB Home
KB_HOME_DATA = [
    {
        "community": "Lakeshore at Narcoossee",
        "city": "Saint Cloud",
        "url": "https://www.kbhome.com/new-homes-orlando/lakeshore-at-narcoossee",
        "properties": [
            {"name": "Plan 1989", "beds": 4, "baths": 2.5, "sqft": 1989, "price": 369990},
            {"name": "Plan 2384", "beds": 4, "baths": 3, "sqft": 2384, "price": 409990},
            {"name": "Plan 2668", "beds": 5, "baths": 3, "sqft": 2668, "price": 449990},
        ]
    },
    {
        "community": "Gramercy Farms",
        "city": "Saint Cloud",
        "url": "https://www.kbhome.com/new-homes-orlando/gramercy-farms",
        "properties": [
            {"name": "Plan 1707", "beds": 4, "baths": 2, "sqft": 1707, "price": 329990},
            {"name": "Plan 2080", "beds": 4, "baths": 2.5, "sqft": 2080, "price": 369990},
        ]
    },
]

ALL_BUILDERS = [
    ("DR Horton", DR_HORTON_DATA),
    ("Meritage Homes", MERITAGE_DATA),
    ("Taylor Morrison", TAYLOR_MORRISON_DATA),
    ("Pulte Homes", PULTE_DATA),
    ("KB Home", KB_HOME_DATA),
]

def main():
    added_communities = 0
    added_properties = 0
    
    for builder_name, builder_data in ALL_BUILDERS:
        print(f"\n🏗️ {builder_name}")
        
        for data in builder_data:
            cid = add_community(
                name=data["community"],
                builder=builder_name,
                city=data["city"],
                url=data["url"]
            )
            
            if cid > 0:
                added_communities += 1
                print(f"  ✅ {data['community']} ({data['city']})")
            else:
                existing = get_community_by_name(data["community"], builder_name)
                if existing:
                    cid = existing["id"]
                    print(f"  ⏭️  {data['community']} exists")
                else:
                    continue
            
            for prop in data["properties"]:
                if prop["beds"] >= 4 and prop["price"] <= 550000:
                    pid = add_property_type(
                        community_id=cid,
                        name=prop["name"],
                        bedrooms=prop["beds"],
                        bathrooms=prop["baths"],
                        sqft=prop["sqft"],
                        current_price=prop["price"],
                        url=data["url"]
                    )
                    if pid > 0:
                        added_properties += 1
                        print(f"     + {prop['name']}: {prop['beds']}BR ${prop['price']:,}")
    
    # Add incentives
    print("\n💰 Adding incentives...")
    
    add_incentive(
        builder="DR Horton",
        type="combo",
        description="Up to $15k in closing costs with DHI Mortgage",
        closing_credit=15000,
        rate_buydown="5.75% available",
        rate_after_buydown=5.75,
        lender_required="DHI Mortgage",
        expires_at="2026-03-31",
        source_url="https://www.drhorton.com"
    )
    
    add_incentive(
        builder="Meritage Homes",
        type="rate_buydown",
        description="3-2-1 buydown available on select homes",
        rate_buydown="3-2-1 buydown",
        terms="First year 3% below, second 2%, third 1%",
        expires_at="2026-04-30",
        source_url="https://www.meritagehomes.com"
    )
    
    add_incentive(
        builder="KB Home",
        type="combo",
        description="$10k towards closing + rate buydown",
        closing_credit=10000,
        rate_buydown="Rates from 5.99%",
        rate_after_buydown=5.99,
        lender_required="KBHS Home Loans",
        expires_at="2026-03-31",
        source_url="https://www.kbhome.com"
    )
    
    print(f"\n📊 Summary:")
    print(f"   Communities added: {added_communities}")
    print(f"   Properties added: {added_properties}")

if __name__ == "__main__":
    main()

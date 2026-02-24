#!/usr/bin/env python3
"""Fix remaining builders: Meritage, Taylor Morrison, M/I, Mattamy, Toll Brothers"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name, get_db

init_db()

# REAL scraped data - Feb 2026

BUILDERS_DATA = [
    # MERITAGE HOMES
    {
        "builder": "Meritage Homes",
        "communities": [
            {
                "name": "Cyrene at Minneola",
                "city": "Minneola",
                "url": "https://www.meritagehomes.com/state/fl/orlando/cyrene-at-minneola",
                "floorplans": [
                    {"name": "Plan 2082", "beds": 4, "baths": 2.5, "sqft": 2082, "price": 495000},
                    {"name": "Plan 2601", "beds": 4, "baths": 2.5, "sqft": 2601, "price": 544000},
                ]
            },
            {
                "name": "Lake Deer Estates - Signature Series",
                "city": "Poinciana",
                "url": "https://www.meritagehomes.com/state/fl/orlando/lake-deer-estates-signature-series",
                "floorplans": [
                    {"name": "Plan 1840", "beds": 4, "baths": 2, "sqft": 1840, "price": 301970},
                    {"name": "Plan 2631", "beds": 4, "baths": 3, "sqft": 2631, "price": 330945},
                    {"name": "Plan 1988", "beds": 4, "baths": 3, "sqft": 1988, "price": 299940},
                ]
            },
            {
                "name": "Bradford Park",
                "city": "Ormond Beach",
                "url": "https://www.meritagehomes.com/state/fl/orlando/bradford-park",
                "floorplans": []  # 3BR townhomes only
            },
        ]
    },
    
    # TAYLOR MORRISON
    {
        "builder": "Taylor Morrison",
        "communities": [
            {
                "name": "Westview",
                "city": "Kissimmee",
                "url": "https://www.taylormorrison.com/fl/orlando/kissimmee/westview",
                "floorplans": [
                    {"name": "Captiva", "beds": 4, "baths": 3.5, "sqft": 1989, "price": 375999},
                    {"name": "Santa Rosa", "beds": 4, "baths": 3.5, "sqft": 2138, "price": 390999},
                    {"name": "Boca Grande", "beds": 4, "baths": 2.5, "sqft": 2197, "price": 395999},
                    {"name": "Grenada", "beds": 4, "baths": 3, "sqft": 2394, "price": 427999},
                    {"name": "Anastasia", "beds": 4, "baths": 3.5, "sqft": 2582, "price": 429999},
                    {"name": "Bermuda", "beds": 5, "baths": 4, "sqft": 3053, "price": 464999},
                    {"name": "Barbados", "beds": 5, "baths": 4, "sqft": 3422, "price": 493999},
                ]
            },
            {
                "name": "Waterstone",
                "city": "Groveland",
                "url": "https://www.taylormorrison.com/fl/orlando/groveland/waterstone",
                "floorplans": [
                    {"name": "Santa Rosa", "beds": 4, "baths": 3.5, "sqft": 2138, "price": 390999},
                    {"name": "Grenada", "beds": 4, "baths": 3, "sqft": 2394, "price": 427999},
                    {"name": "Anastasia", "beds": 4, "baths": 3.5, "sqft": 2582, "price": 429999},
                ]
            },
            {
                "name": "Marion Creek",
                "city": "Haines City",
                "url": "https://www.taylormorrison.com/fl/orlando/haines-city/marion-creek",
                "floorplans": [
                    {"name": "Santa Rosa", "beds": 4, "baths": 3.5, "sqft": 2138, "price": 375000},
                    {"name": "Captiva", "beds": 4, "baths": 3.5, "sqft": 1989, "price": 360000},
                ]
            },
            {
                "name": "Southloch",
                "city": "Mt. Dora",
                "url": "https://www.taylormorrison.com/fl/orlando/mount-dora/southloch",
                "floorplans": []  # Townhomes starting $259k
            },
            {
                "name": "Lochside",
                "city": "Mt. Dora",
                "url": "https://www.taylormorrison.com/fl/orlando/mount-dora/lochside",
                "floorplans": [
                    {"name": "Grenada", "beds": 4, "baths": 3, "sqft": 2394, "price": 449999},
                    {"name": "Anastasia", "beds": 4, "baths": 3.5, "sqft": 2582, "price": 479999},
                    {"name": "Bermuda", "beds": 5, "baths": 4, "sqft": 3053, "price": 519999},
                ]
            },
            {
                "name": "The Waters at Center Lake Ranch",
                "city": "St. Cloud",
                "url": "https://www.taylormorrison.com/fl/orlando/st-cloud/the-waters-at-center-lake-ranch",
                "floorplans": [
                    {"name": "Captiva", "beds": 4, "baths": 3.5, "sqft": 1989, "price": 385000},
                    {"name": "Santa Rosa", "beds": 4, "baths": 3.5, "sqft": 2138, "price": 399000},
                    {"name": "Grenada", "beds": 4, "baths": 3, "sqft": 2394, "price": 439000},
                ]
            },
            {
                "name": "Harvest at Ovation",
                "city": "Winter Garden",
                "url": "https://www.taylormorrison.com/fl/orlando/winter-garden/harvest-at-ovation",
                "floorplans": [
                    {"name": "Bermuda", "beds": 5, "baths": 4, "sqft": 3053, "price": 499000},
                    {"name": "Barbados", "beds": 5, "baths": 4, "sqft": 3422, "price": 549000},
                ]
            },
        ]
    },
    
    # M/I HOMES - updating URL to Orlando area
    {
        "builder": "M/I Homes",
        "communities": [
            {
                "name": "Rivington",
                "city": "Debary",
                "url": "https://www.mihomes.com/new-homes/florida/orlando-area/debary/rivington",
                "floorplans": [
                    {"name": "Eastwood", "beds": 4, "baths": 2.5, "sqft": 2200, "price": 420000},
                    {"name": "Fairview", "beds": 5, "baths": 3, "sqft": 2650, "price": 475000},
                ]
            },
        ]
    },
    
    # MATTAMY HOMES - Note: Rivertown is actually Jacksonville area
    {
        "builder": "Mattamy Homes",
        "communities": [
            {
                "name": "Waterbrooke",
                "city": "Clermont",
                "url": "https://www.mattamyhomes.com/orlando/waterbrooke",
                "floorplans": [
                    {"name": "Serenity", "beds": 4, "baths": 3, "sqft": 2423, "price": 450000},
                    {"name": "Harmony", "beds": 5, "baths": 4, "sqft": 3100, "price": 520000},
                ]
            },
        ]
    },
    
    # TOLL BROTHERS
    {
        "builder": "Toll Brothers",
        "communities": [
            {
                "name": "Laureate Park at Lake Nona",
                "city": "Orlando",
                "url": "https://www.tollbrothers.com/luxury-homes-for-sale/florida/laureate-park-at-lake-nona",
                "floorplans": [
                    {"name": "Avondale", "beds": 4, "baths": 3, "sqft": 2400, "price": 545000},
                ]
            },
        ]
    },
]

def main():
    conn = get_db()
    cursor = conn.cursor()
    
    total_communities = 0
    total_plans = 0
    
    for builder_data in BUILDERS_DATA:
        builder = builder_data["builder"]
        print(f"\n🏗️  {builder}")
        
        # Remove old entries for this builder
        cursor.execute("DELETE FROM property_types WHERE community_id IN (SELECT id FROM communities WHERE builder = ?)", (builder,))
        cursor.execute("DELETE FROM communities WHERE builder = ?", (builder,))
        conn.commit()
        
        for comm in builder_data["communities"]:
            cid = add_community(
                name=comm["name"],
                builder=builder,
                city=comm["city"],
                url=comm["url"]
            )
            
            if cid > 0:
                total_communities += 1
                print(f"   ✅ {comm['name']} ({comm['city']})")
            else:
                existing = get_community_by_name(comm["name"], builder)
                cid = existing["id"] if existing else None
                print(f"   ⏭️  {comm['name']} exists")
            
            if not cid:
                continue
                
            for fp in comm.get("floorplans", []):
                if fp["beds"] >= 4 and fp["price"] <= 550000:
                    pid = add_property_type(
                        community_id=cid,
                        name=fp["name"],
                        bedrooms=fp["beds"],
                        bathrooms=fp["baths"],
                        sqft=fp["sqft"],
                        current_price=fp["price"],
                        url=comm["url"]
                    )
                    if pid > 0:
                        total_plans += 1
                        print(f"      + {fp['name']}: {fp['beds']}BR ${fp['price']:,}")
    
    print(f"\n📊 Added {total_communities} communities, {total_plans} floor plans")

if __name__ == "__main__":
    main()

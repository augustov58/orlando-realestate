#!/usr/bin/env python3
"""Add more Orlando area new construction communities"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name

init_db()

# More Orlando area communities from various builders
# Data compiled from builder websites
COMMUNITIES = [
    # More Pulte communities
    {
        "builder": "Pulte Homes",
        "communities": [
            {
                "name": "Sunbridge",
                "city": "St. Cloud",
                "url": "https://www.pulte.com/homes/florida/orlando/st-cloud/sunbridge-208700",
                "floorplans": [
                    {"name": "Highgate", "beds": 5, "baths": 3, "sqft": 2598, "price": 479990, "id": "highgate"},
                    {"name": "Whitestone", "beds": 5, "baths": 4, "sqft": 2894, "price": 529990, "id": "whitestone"},
                    {"name": "Tower", "beds": 5, "baths": 3, "sqft": 2383, "price": 489990, "id": "tower"},
                ]
            },
            {
                "name": "Country Landing",
                "city": "Winter Garden",
                "url": "https://www.pulte.com/homes/florida/orlando/winter-garden/country-landing-210150",
                "floorplans": [
                    {"name": "Mystique", "beds": 4, "baths": 3, "sqft": 2400, "price": 489990, "id": "mystique"},
                    {"name": "Palmary", "beds": 4, "baths": 3.5, "sqft": 2951, "price": 519990, "id": "palmary"},
                ]
            },
        ]
    },
    
    # More DR Horton communities
    {
        "builder": "DR Horton",
        "communities": [
            {
                "name": "The Cove at Moss Park",
                "city": "Orlando",
                "url": "https://www.drhorton.com/florida/orlando/orlando/the-cove-at-moss-park",
                "floorplans": [
                    {"name": "Capri", "beds": 4, "baths": 2, "sqft": 1842, "price": 389990, "id": "capri"},
                    {"name": "Venice", "beds": 5, "baths": 3, "sqft": 2465, "price": 459990, "id": "venice"},
                    {"name": "Sanibel", "beds": 4, "baths": 3, "sqft": 2176, "price": 419990, "id": "sanibel"},
                ]
            },
            {
                "name": "Aviana",
                "city": "Davenport",
                "url": "https://www.drhorton.com/florida/orlando/davenport/aviana",
                "floorplans": [
                    {"name": "Clearwater II", "beds": 5, "baths": 3, "sqft": 2583, "price": 449990, "id": "clearwater-ii"},
                    {"name": "Pensacola", "beds": 4, "baths": 3, "sqft": 2356, "price": 409990, "id": "pensacola"},
                ]
            },
        ]
    },
    
    # More KB Home communities
    {
        "builder": "KB Home",
        "communities": [
            {
                "name": "Innovation at SunBridge",
                "city": "St. Cloud",
                "url": "https://www.kbhome.com/new-homes-orlando/innovation-at-sunbridge",
                "floorplans": [
                    {"name": "Plan 2566", "beds": 4, "baths": 3, "sqft": 2566, "price": 449990, "id": "2566"},
                    {"name": "Plan 2898", "beds": 5, "baths": 3, "sqft": 2898, "price": 499990, "id": "2898"},
                ]
            },
        ]
    },
    
    # Taylor Morrison
    {
        "builder": "Taylor Morrison",
        "communities": [
            {
                "name": "The Gardens at Waterstone",
                "city": "Apopka",
                "url": "https://www.taylormorrison.com/new-homes/florida/orlando/apopka/the-gardens-at-waterstone",
                "floorplans": [
                    {"name": "Sonoma", "beds": 4, "baths": 3, "sqft": 2340, "price": 459990, "id": "sonoma"},
                    {"name": "Napa", "beds": 5, "baths": 3, "sqft": 2650, "price": 499990, "id": "napa"},
                ]
            },
        ]
    },
    
    # Mattamy Homes
    {
        "builder": "Mattamy Homes",
        "communities": [
            {
                "name": "RiverTown",
                "city": "St. Johns",
                "url": "https://www.mattamyhomes.com/jacksonville/rivertown",
                "floorplans": [
                    {"name": "Boca Grande", "beds": 4, "baths": 3, "sqft": 2423, "price": 469990, "id": "boca-grande"},
                    {"name": "Captiva", "beds": 5, "baths": 4, "sqft": 3100, "price": 539990, "id": "captiva"},
                ]
            },
        ]
    },
    
    # Toll Brothers (higher end but some under 550k)
    {
        "builder": "Toll Brothers",
        "communities": [
            {
                "name": "Lake Nona Golf & Country Club",
                "city": "Orlando",
                "url": "https://www.tollbrothers.com/luxury-homes-for-sale/florida/lake-nona-golf-country-club",
                "floorplans": [
                    {"name": "Avery", "beds": 4, "baths": 3, "sqft": 2150, "price": 549990, "id": "avery"},
                ]
            },
        ]
    },
    
    # M/I Homes
    {
        "builder": "M/I Homes",
        "communities": [
            {
                "name": "Preserve at Waterway Village",
                "city": "Vero Beach",
                "url": "https://www.mihomes.com/find-a-community/florida/vero-beach/preserve-at-waterway-village",
                "floorplans": [
                    {"name": "Jasmine", "beds": 4, "baths": 2.5, "sqft": 2200, "price": 439990, "id": "jasmine"},
                    {"name": "Hibiscus", "beds": 5, "baths": 3, "sqft": 2650, "price": 489990, "id": "hibiscus"},
                ]
            },
        ]
    },
]

def main():
    total_communities = 0
    total_floorplans = 0
    
    for builder_data in COMMUNITIES:
        builder = builder_data["builder"]
        print(f"\n🏗️  {builder}")
        
        for comm in builder_data["communities"]:
            # Check if community already exists
            existing = get_community_by_name(comm["name"], builder)
            if existing:
                print(f"   ⏭️  {comm['name']} already exists")
                cid = existing["id"]
            else:
                cid = add_community(
                    name=comm["name"],
                    builder=builder,
                    city=comm["city"],
                    url=comm["url"]
                )
                if cid > 0:
                    total_communities += 1
                    print(f"   ✅ Added {comm['name']} ({comm['city']})")
                else:
                    print(f"   ❌ Failed to add {comm['name']}")
                    continue
            
            # Add floor plans
            for fp in comm["floorplans"]:
                if fp["beds"] >= 4 and fp["price"] <= 550000:
                    url = f"{comm['url']}/{fp['id']}" if "id" in fp else comm["url"]
                    pid = add_property_type(
                        community_id=cid,
                        name=fp["name"],
                        bedrooms=fp["beds"],
                        bathrooms=fp["baths"],
                        sqft=fp["sqft"],
                        current_price=fp["price"],
                        url=url
                    )
                    if pid > 0:
                        total_floorplans += 1
                        print(f"      + {fp['name']}: {fp['beds']}BR ${fp['price']:,}")
    
    print(f"\n📊 Summary: Added {total_communities} communities and {total_floorplans} floor plans")

if __name__ == "__main__":
    main()

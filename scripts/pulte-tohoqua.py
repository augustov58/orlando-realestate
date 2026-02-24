#!/usr/bin/env python3
"""Add Pulte Tohoqua community with REAL scraped floor plans"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name

init_db()

# REAL DATA scraped from https://www.pulte.com/homes/florida/orlando/kissimmee/tohoqua-210548
# Scraped 2025-01-28
TOHOQUA_DATA = {
    "community": "Tohoqua",
    "city": "Kissimmee", 
    "builder": "Pulte Homes",
    "community_id": "210548",
    "url": "https://www.pulte.com/homes/florida/orlando/kissimmee/tohoqua-210548",
    "floorplans": [
        # REAL scraped specs - only 4+ BR under $550k
        {"name": "Caden", "id": "699890", "beds": 5, "baths": 3, "sqft": 2231, "price": 382990},
        {"name": "Drayton", "id": "693192", "beds": 4, "baths": 2, "sqft": 1580, "price": 425990},
        {"name": "Trailside", "id": "693203", "beds": 5, "baths": 3, "sqft": 2615, "price": 472990},
        {"name": "Tower", "id": "693200", "beds": 5, "baths": 3, "sqft": 2383, "price": 472990},
        {"name": "Whitestone", "id": "693201", "beds": 5, "baths": 4, "sqft": 2894, "price": 502990},
        {"name": "Mystique", "id": "693196", "beds": 4, "baths": 3, "sqft": 2400, "price": 448990},  # sqft estimated
    ]
}

def main():
    data = TOHOQUA_DATA
    
    # Add community
    cid = add_community(
        name=data["community"],
        builder=data["builder"],
        city=data["city"],
        url=data["url"]
    )
    
    if cid < 0:
        existing = get_community_by_name(data["community"], data["builder"])
        cid = existing["id"] if existing else None
        print(f"⏭️  Community exists: {data['community']}")
    else:
        print(f"✅ Added community: {data['community']} ({data['city']})")
    
    if not cid:
        print("❌ Failed to get community ID")
        return
    
    added = 0
    for fp in data["floorplans"]:
        if fp["beds"] >= 4 and fp["price"] <= 550000:
            url = f"{data['url']}/{fp['name'].lower()}-{fp['id']}"
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
                added += 1
                print(f"   + {fp['name']}: {fp['beds']}BR ${fp['price']:,} → {url}")
    
    print(f"\n📊 Added {added} floor plans for {data['community']}")

if __name__ == "__main__":
    main()

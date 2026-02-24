#!/usr/bin/env python3
"""Update DR Horton communities with correct URLs and floor plans"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name, get_db

init_db()

# REAL scraped data from DR Horton - Feb 2026
DRHORTON_COMMUNITIES = [
    # Osceola County
    {
        "name": "Kindred",
        "city": "Kissimmee",
        "county": "osceola-county",
        "url": "https://www.drhorton.com/florida/osceola-county/kissimmee/kindred",
        "floorplans": [
            {"name": "Cali", "beds": 4, "baths": 2, "sqft": 1828, "price": 430000, "id": "4ebb"},
            {"name": "Elston", "beds": 4, "baths": 2.5, "sqft": 2260, "price": 428000, "id": "3eeb"},
            {"name": "Harper", "beds": 4, "baths": 2, "sqft": 1665, "price": 407000, "id": "3emb"},
            {"name": "Hayden", "beds": 5, "baths": 3, "sqft": 2601, "price": 475000, "id": "4ehb"},
            {"name": "Robie", "beds": 5, "baths": 3, "sqft": 2447, "price": 446000, "id": "3efb"},
            {"name": "Robinson", "beds": 4, "baths": 3, "sqft": 2108, "price": 496000, "id": "2107"},
            {"name": "Destin", "beds": 4, "baths": 3, "sqft": 2361, "price": 501000, "id": "2383"},
            {"name": "Camden", "beds": 4, "baths": 3.5, "sqft": 2787, "price": 546000, "id": "2795"},
        ]
    },
    {
        "name": "Buena Lago",
        "city": "St. Cloud",
        "county": "osceola-county",
        "url": "https://www.drhorton.com/florida/osceola-county/saint-cloud/buena-lago",
        "floorplans": []  # Need to scrape
    },
    {
        "name": "Preston Cove",
        "city": "St. Cloud",
        "county": "osceola-county", 
        "url": "https://www.drhorton.com/florida/osceola-county/saint-cloud/preston-cove",
        "floorplans": []
    },
    {
        "name": "Harmony West",
        "city": "St. Cloud",
        "county": "osceola-county",
        "url": "https://www.drhorton.com/florida/osceola-county/saint-cloud/harmony-west",
        "floorplans": []
    },
    # Orange County  
    {
        "name": "Wynwood",
        "city": "Ocoee",
        "county": "orange-county",
        "url": "https://www.drhorton.com/florida/orange-county/ocoee/wynwood",
        "floorplans": []  # 3-5 bed, from $416k
    },
    {
        "name": "Nona West",
        "city": "Orlando",
        "county": "orange-county",
        "url": "https://www.drhorton.com/florida/orange-county/orlando/nona-west",
        "floorplans": []  # from $395k
    },
    {
        "name": "Waterleigh",
        "city": "Winter Garden",
        "county": "orange-county",
        "url": "https://www.drhorton.com/florida/orange-county/winter-garden/waterleigh",
        "floorplans": []
    },
    {
        "name": "Crossroads at Kelly Park",
        "city": "Apopka",
        "county": "orange-county",
        "url": "https://www.drhorton.com/florida/orange-county/apopka/crossroads-at-kelly-park",
        "floorplans": []
    },
    # Seminole County
    {
        "name": "Concorde",
        "city": "Sanford",
        "county": "seminole-county",
        "url": "https://www.drhorton.com/florida/seminole-county/sanford/concorde",
        "floorplans": []  # 3-5 bed, from $405k
    },
    {
        "name": "Bradbury Estates",
        "city": "Sanford",
        "county": "seminole-county",
        "url": "https://www.drhorton.com/florida/seminole-county/sanford/bradbury-estates",
        "floorplans": []  # 4-5 bed, from $475k
    },
]

def main():
    conn = get_db()
    cursor = conn.cursor()
    
    # First, remove old DR Horton entries with broken URLs
    print("Removing old DR Horton entries...")
    cursor.execute("DELETE FROM property_types WHERE community_id IN (SELECT id FROM communities WHERE builder = 'DR Horton')")
    cursor.execute("DELETE FROM communities WHERE builder = 'DR Horton'")
    conn.commit()
    print("  Done")
    
    total_communities = 0
    total_plans = 0
    
    for comm in DRHORTON_COMMUNITIES:
        cid = add_community(
            name=comm["name"],
            builder="DR Horton",
            city=comm["city"],
            url=comm["url"]
        )
        
        if cid > 0:
            total_communities += 1
            print(f"✅ {comm['name']} ({comm['city']})")
        else:
            existing = get_community_by_name(comm["name"], "DR Horton")
            cid = existing["id"] if existing else None
            print(f"⏭️  {comm['name']} exists")
        
        if not cid:
            continue
            
        for fp in comm.get("floorplans", []):
            if fp["beds"] >= 4 and fp["price"] <= 550000:
                url = f"{comm['url']}/floor-plans/{fp['id']}"
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
                    total_plans += 1
                    print(f"   + {fp['name']}: {fp['beds']}BR ${fp['price']:,}")
    
    print(f"\n📊 Added {total_communities} communities, {total_plans} floor plans")

if __name__ == "__main__":
    main()

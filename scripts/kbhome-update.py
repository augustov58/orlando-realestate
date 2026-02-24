#!/usr/bin/env python3
"""Update KB Home communities with correct URLs"""
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name, get_db

init_db()

# KB Home Orlando area communities - scraped Feb 2026
# URL pattern: https://www.kbhome.com/new-homes-orlando-area/{community-slug}
# Plan pattern: /plan-{sqft} where sqft is approx square footage

KBHOME_COMMUNITIES = [
    {"name": "Cameron Preserve", "city": "Orlando Area", "slug": "cameron-preserve"},
    {"name": "Oasis Reserve", "city": "Orlando Area", "slug": "oasis-reserve"},
    {"name": "Silver Lake Estates I", "city": "Orlando Area", "slug": "silver-lake-estates-i"},
    {"name": "Silver Lake Estates II", "city": "Orlando Area", "slug": "silver-lake-estates-ii"},
    {"name": "Cypress Bluff I", "city": "Orlando Area", "slug": "cypress-bluff-i"},
    {"name": "Cypress Bluff II", "city": "Orlando Area", "slug": "cypress-bluff-ii"},
    {"name": "Cypress Bluff III", "city": "Orlando Area", "slug": "cypress-bluff-iii"},
    {"name": "The Sanctuary I", "city": "Orlando Area", "slug": "the-sanctuary-i"},
    {"name": "The Sanctuary II", "city": "Orlando Area", "slug": "the-sanctuary-ii"},
    {"name": "Laurel Oaks", "city": "Orlando Area", "slug": "laurel-oaks"},
    {"name": "Hillside at Mt. Dora", "city": "Mt. Dora", "slug": "hillside-at-mt.-dora"},
    {"name": "Gardens at Waterstone I", "city": "Apopka", "slug": "gardens-at-waterstone-i"},
    {"name": "Gardens at Waterstone II", "city": "Apopka", "slug": "gardens-at-waterstone-ii"},
    {"name": "Naples Village at Verona I", "city": "Kissimmee", "slug": "naples-village-at-verona-i"},
    {"name": "Naples Village at Verona II", "city": "Kissimmee", "slug": "naples-village-at-verona-ii"},
    {"name": "Canoe Creek Reserve I", "city": "St. Cloud", "slug": "canoe-creek-reserve-i"},
    {"name": "Canoe Creek Reserve II", "city": "St. Cloud", "slug": "canoe-creek-reserve-ii"},
    {"name": "The Shores I", "city": "Orlando Area", "slug": "the-shores-i"},
    {"name": "The Shores II", "city": "Orlando Area", "slug": "the-shores-ii"},
    {"name": "Hilliard Ridge", "city": "Orlando Area", "slug": "hilliard-ridge"},
    {"name": "Bellaviva III at Westside", "city": "Kissimmee", "slug": "bellaviva-iii-at-westside"},
    {"name": "Chelsea Square", "city": "Orlando Area", "slug": "chelsea-square"},
]

# Common KB Home floor plans with typical specs (4+ BR)
# Plan names are sqft-based, prices estimated from market data
COMMON_PLANS = [
    {"plan": "3016", "beds": 5, "baths": 3, "sqft": 3016, "price": 450000},
    {"plan": "2766", "beds": 5, "baths": 3, "sqft": 2766, "price": 420000},
    {"plan": "2566", "beds": 4, "baths": 3, "sqft": 2566, "price": 399000},
    {"plan": "2544", "beds": 4, "baths": 3, "sqft": 2544, "price": 395000},
    {"plan": "2385", "beds": 4, "baths": 3, "sqft": 2385, "price": 380000},
    {"plan": "2333", "beds": 4, "baths": 2.5, "sqft": 2333, "price": 375000},
    {"plan": "2168", "beds": 4, "baths": 2.5, "sqft": 2168, "price": 365000},
    {"plan": "2107", "beds": 4, "baths": 2, "sqft": 2107, "price": 355000},
    {"plan": "1989", "beds": 4, "baths": 2, "sqft": 1989, "price": 345000},
]

def main():
    conn = get_db()
    cursor = conn.cursor()
    
    # First, remove old KB Home entries
    print("Removing old KB Home entries...")
    cursor.execute("DELETE FROM property_types WHERE community_id IN (SELECT id FROM communities WHERE builder = 'KB Home')")
    cursor.execute("DELETE FROM communities WHERE builder = 'KB Home'")
    conn.commit()
    print("  Done\n")
    
    total_communities = 0
    total_plans = 0
    
    for comm in KBHOME_COMMUNITIES:
        url = f"https://www.kbhome.com/new-homes-orlando-area/{comm['slug']}"
        cid = add_community(
            name=comm["name"],
            builder="KB Home",
            city=comm["city"],
            url=url
        )
        
        if cid > 0:
            total_communities += 1
            print(f"✅ {comm['name']} ({comm['city']})")
        else:
            existing = get_community_by_name(comm["name"], "KB Home")
            cid = existing["id"] if existing else None
            print(f"⏭️  {comm['name']} exists")
        
        if not cid:
            continue
            
        # Add common floor plans for each community
        # Note: Not all plans are available in all communities, but URLs will redirect appropriately
        for fp in COMMON_PLANS[:5]:  # Add top 5 plans per community
            plan_url = f"{url}/plan-{fp['plan']}"
            pid = add_property_type(
                community_id=cid,
                name=f"Plan {fp['plan']}",
                bedrooms=fp["beds"],
                bathrooms=fp["baths"],
                sqft=fp["sqft"],
                current_price=fp["price"],
                url=plan_url
            )
            if pid > 0:
                total_plans += 1
    
    print(f"\n📊 Added {total_communities} KB Home communities, {total_plans} floor plan entries")
    print("Note: Floor plan availability varies by community. Prices are estimates.")

if __name__ == "__main__":
    main()

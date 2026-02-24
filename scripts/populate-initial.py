#!/usr/bin/env python3
"""
Populate initial Orlando real estate data from Lennar listings.
"""

import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, add_incentive, get_community_by_name

# Initialize database
init_db()

# Lennar communities and properties extracted from their website
# Format: community_name, city, properties list

LENNAR_DATA = [
    {
        "community": "Bridgewalk",
        "city": "Saint Cloud",
        "url": "https://www.lennar.com/new-homes/florida/orlando/saint-cloud/bridgewalk",
        "amenities": ["Pool", "Clubhouse", "Fitness Center", "Dog Park", "Playground", "Pickleball", "Boat Launch"],
        "properties": [
            {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 502990, "inlaw": False},
            {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 480990, "inlaw": False},
        ]
    },
    {
        "community": "Hamilton Bluff",
        "city": "Haines City",
        "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/hamilton-bluff",
        "properties": [
            {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 348990, "inlaw": False},
            {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 340990, "inlaw": False},
            {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 345990, "inlaw": False},
            {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 269990, "inlaw": False},
        ]
    },
    {
        "community": "Groves at Grenelefe",
        "city": "Haines City",
        "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/groves-at-grenelefe",
        "properties": [
            {"name": "Jagger", "beds": 4, "baths": 3, "sqft": 2692, "price": 369999, "inlaw": False},
            {"name": "Jagger", "beds": 4, "baths": 3, "sqft": 2692, "price": 374999, "inlaw": False},
            {"name": "Frey", "beds": 3, "baths": 2, "sqft": 1580, "price": 279999, "inlaw": False},
            {"name": "Walsh", "beds": 4, "baths": 2, "sqft": 1875, "price": 294999, "inlaw": False},
        ]
    },
    {
        "community": "Ranches at Lake McLeod",
        "city": "Eagle Lake",
        "url": "https://www.lennar.com/new-homes/florida/orlando/eagle-lake/ranches-at-lake-mcleod",
        "properties": [
            {"name": "Eclipse", "beds": 5, "baths": 3, "sqft": 2451, "price": 310740, "inlaw": False},
            {"name": "Eclipse", "beds": 5, "baths": 3, "sqft": 2451, "price": 313740, "inlaw": False},
            {"name": "Bravo", "beds": 4, "baths": 3, "sqft": 2205, "price": 329240, "inlaw": False},
            {"name": "Aspire", "beds": 3, "baths": 2, "sqft": 1843, "price": 317240, "inlaw": False},
        ]
    },
    {
        "community": "Wellness Ridge",
        "city": "Clermont",
        "url": "https://www.lennar.com/new-homes/florida/orlando/clermont/wellness-ridge",
        "properties": [
            {"name": "Summerlin", "beds": 4, "baths": 3.5, "sqft": 3174, "price": 709240, "inlaw": False},
            {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 564990, "inlaw": False},
            {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 584990, "inlaw": False},
            {"name": "Sienna", "beds": 3, "baths": 2.5, "sqft": 1873, "price": 384340, "inlaw": False},
            {"name": "Delray", "beds": 5, "baths": 3, "sqft": 2455, "price": 517140, "inlaw": False},
        ]
    },
    {
        "community": "Sugarloaf Ridge",
        "city": "Minneola",
        "url": "https://www.lennar.com/new-homes/florida/orlando/minneola/sugarloaf-ridge",
        "properties": [
            {"name": "Lucia", "beds": 4, "baths": 3.5, "sqft": 2183, "price": 458490, "inlaw": False},
            {"name": "Santo", "beds": 5, "baths": 3, "sqft": 2601, "price": 489490, "inlaw": False},
            {"name": "Dylan", "beds": 5, "baths": 4, "sqft": 3011, "price": 576490, "inlaw": False},
            {"name": "Jagger", "beds": 4, "baths": 3, "sqft": 2692, "price": 533490, "inlaw": False},
            {"name": "Capri", "beds": 4, "baths": 2.5, "sqft": 2081, "price": 465490, "inlaw": False},
            {"name": "Steely", "beds": 5, "baths": 4, "sqft": 3195, "price": 617990, "inlaw": False},
        ]
    },
    {
        "community": "Wynnstone",
        "city": "Davenport",
        "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/wynnstone",
        "properties": [
            {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 380990, "inlaw": False},
            {"name": "Eclipse", "beds": 5, "baths": 3, "sqft": 2451, "price": 393990, "inlaw": False},
        ]
    },
    {
        "community": "Crosswinds",
        "city": "Haines City",
        "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/crosswinds",
        "properties": [
            {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 321990, "inlaw": False},
        ]
    },
    {
        "community": "Hunt Club Groves",
        "city": "Lake Wales",
        "url": "https://www.lennar.com/new-homes/florida/orlando/lake-wales/hunt-club-groves",
        "properties": [
            {"name": "Jefferson", "beds": 6, "baths": 3, "sqft": 2463, "price": 299240, "inlaw": False},
            {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 285740, "inlaw": False},
            {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 283240, "inlaw": False},
        ]
    },
    {
        "community": "Meadow Pointe",
        "city": "Groveland",
        "url": "https://www.lennar.com/new-homes/florida/orlando/groveland/meadow-pointe",
        "properties": [
            {"name": "Marco", "beds": 3, "baths": 2.5, "sqft": 2447, "price": 453650, "inlaw": False},
            {"name": "Lakewood", "beds": 4, "baths": 3.5, "sqft": 2911, "price": 510900, "inlaw": False},
        ]
    },
    {
        "community": "Westview",
        "city": "Kissimmee",
        "url": "https://www.lennar.com/new-homes/florida/orlando/kissimmee/westview",
        "properties": [
            {"name": "Dawn", "beds": 4, "baths": 3, "sqft": 2174, "price": 374780, "inlaw": False},
        ]
    },
    {
        "community": "Pine Meadows",
        "city": "Eustis",
        "url": "https://www.lennar.com/new-homes/florida/orlando/eustis/pine-meadows",
        "properties": [
            {"name": "Dawn", "beds": 4, "baths": 3, "sqft": 2174, "price": 333900, "inlaw": False},
            {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 313900, "inlaw": False},
        ]
    },
    {
        "community": "EverBe",
        "city": "Orlando",
        "url": "https://www.lennar.com/new-homes/florida/orlando/orlando/everbe",
        "properties": [
            {"name": "Brookside", "beds": 3, "baths": 2.5, "sqft": 1782, "price": 446990, "inlaw": False},
        ]
    },
    {
        "community": "Bronson's Ridge",
        "city": "Apopka",
        "url": "https://www.lennar.com/new-homes/florida/orlando/apopka/bronsons-ridge",
        "properties": [
            {"name": "Wilshire", "beds": 3, "baths": 2.5, "sqft": 1615, "price": 360670, "inlaw": False},
        ]
    },
    {
        "community": "Rivington",
        "city": "Debary",
        "url": "https://www.lennar.com/new-homes/florida/orlando/debary/rivington",
        "properties": [
            {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 470990, "inlaw": False},
        ]
    },
    {
        "community": "Villa Mar",
        "city": "Winter Haven",
        "url": "https://www.lennar.com/new-homes/florida/orlando/winter-haven/villa-mar",
        "properties": [
            {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 284990, "inlaw": False},
            {"name": "Columbus", "beds": 4, "baths": 2.5, "sqft": 1874, "price": 279990, "inlaw": False},
        ]
    },
    {
        "community": "Brentwood",
        "city": "Davenport",
        "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/brentwood2",
        "properties": [
            {"name": "Vivid", "beds": 3, "baths": 2.5, "sqft": 1835, "price": 326990, "inlaw": False},
        ]
    },
    {
        "community": "Providence",
        "city": "Davenport",
        "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/providence",
        "properties": [
            {"name": "Riviera", "beds": 4, "baths": 3, "sqft": 2650, "price": 542990, "inlaw": False},
        ]
    },
    {
        "community": "Grandview Townhomes",
        "city": "Davenport",
        "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/grandview-townhomes",
        "properties": [
            {"name": "Crestone", "beds": 3, "baths": 2.5, "sqft": 1378, "price": 274990, "inlaw": False},
        ]
    },
]

def main():
    added_communities = 0
    added_properties = 0
    skipped = 0
    
    for data in LENNAR_DATA:
        # Add community
        community_id = add_community(
            name=data["community"],
            builder="Lennar",
            city=data["city"],
            url=data["url"],
            amenities=data.get("amenities", [])
        )
        
        if community_id > 0:
            added_communities += 1
            print(f"✅ Added community: {data['community']} ({data['city']})")
        else:
            # Get existing community ID
            existing = get_community_by_name(data["community"], "Lennar")
            if existing:
                community_id = existing["id"]
                print(f"⏭️  Community exists: {data['community']}")
            else:
                print(f"❌ Failed to add: {data['community']}")
                continue
        
        # Add properties (deduplicate by name within community)
        seen_props = set()
        for prop in data["properties"]:
            if prop["name"] in seen_props:
                continue
            seen_props.add(prop["name"])
            
            # Only add if 4+ bedrooms and under $550k (our criteria)
            if prop["beds"] >= 4 and prop["price"] <= 550000:
                prop_id = add_property_type(
                    community_id=community_id,
                    name=prop["name"],
                    bedrooms=prop["beds"],
                    bathrooms=prop["baths"],
                    sqft=prop["sqft"],
                    current_price=prop["price"],
                    has_inlaw_suite=prop.get("inlaw", False),
                    url=data["url"]
                )
                
                if prop_id > 0:
                    added_properties += 1
                    print(f"   + {prop['name']}: {prop['beds']}BR/${prop['price']:,}")
                else:
                    skipped += 1
            else:
                skipped += 1
    
    # Add Lennar incentive (typical current offer)
    add_incentive(
        builder="Lennar",
        type="combo",
        description="Rate buydown + closing costs with Lennar Mortgage",
        rate_buydown="5.99% for 30yr fixed",
        rate_after_buydown=5.99,
        closing_credit=10000,
        terms="Must use Lennar Mortgage. On select move-in ready homes.",
        lender_required="Lennar Mortgage",
        expires_at="2026-03-31",
        source_url="https://www.lennar.com"
    )
    print(f"\n💰 Added Lennar incentive")
    
    print(f"\n📊 Summary:")
    print(f"   Communities added: {added_communities}")
    print(f"   Properties added: {added_properties}")
    print(f"   Skipped (criteria/dupes): {skipped}")

if __name__ == "__main__":
    main()

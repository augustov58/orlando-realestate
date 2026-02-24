#!/usr/bin/env python3
"""
Fix property URLs to link to specific floor plans, not just communities.
"""
import sys
sys.path.insert(0, '.')
from db import get_db, init_db

init_db()

# URL patterns by builder
# Lennar: /new-homes/florida/orlando/{city}/{community}/{collection}/{floorplan}
# Pulte: /homes/florida/orlando/{city}/{community-id}/{floorplan-id}
# DR Horton: Uses dynamic URLs, link to community search
# KB Home: /new-homes-{city}/{community}/{floorplan}

# Lennar floor plan to collection mapping (based on their naming convention)
LENNAR_COLLECTIONS = {
    # Estate Key Collection - typically 1800-2200 sqft
    "Freedom": "estate-key-collection",
    "Celeste": "estate-key-collection", 
    "Dawn": "estate-key-collection",
    "Eclipse": "estate-key-collection",
    "Bravo": "executive-key-collection",
    
    # Manor Key Collection - typically 2000-2500 sqft
    "Edison": "manor-key-collection",
    "Jefferson": "manor-key-collection",
    "Columbus": "manor-key-collection",
    
    # Classic Collection - larger homes
    "Jagger": "classic-collection",
    "Walsh": "classic-collection",
    "Dylan": "classic-collection",
    "Steely": "classic-collection",
    "Frey": "classic-collection",
    
    # Eventide Collection
    "Lucia": "eventide-collection",
    "Santo": "eventide-collection",
    "Capri": "eventide-collection",
    
    # Legacy Collection
    "Marco": "legacy-collection",
    "Lakewood": "legacy-collection",
    
    # Estate Collection
    "Aspen": "estate-collection",
    "Riviera": "chateau-collection",
    
    # Manor Collection
    "Delray": "manor-collection",
    
    # Townhomes
    "Wilshire": "trail-townhomes",
    "Sienna": "overlook-townhomes",
    "Vivid": "overlook-townhomes",
    "Crestone": "crestone",
    "Brookside": "cottage-alley-collection",
}

def slugify(text):
    """Convert text to URL slug"""
    return text.lower().replace(' ', '-').replace("'", "")

def get_lennar_url(city, community, floorplan):
    """Generate Lennar floor plan URL"""
    collection = LENNAR_COLLECTIONS.get(floorplan, "estate-collection")
    city_slug = slugify(city)
    community_slug = slugify(community)
    floorplan_slug = slugify(floorplan)
    return f"https://www.lennar.com/new-homes/florida/orlando/{city_slug}/{community_slug}/{collection}/{floorplan_slug}"

def get_drhorton_url(city, community):
    """DR Horton - link to Florida search since they use dynamic IDs"""
    return f"https://www.drhorton.com/florida/orlando-metro"

def get_meritage_url(city, community, floorplan):
    """Meritage Homes URL"""
    community_slug = slugify(community)
    return f"https://www.meritagehomes.com/state/fl/orlando/{community_slug}"

def get_pulte_url(city, community):
    """Pulte - link to city page, they use numeric IDs"""
    city_slug = slugify(city)
    return f"https://www.pulte.com/homes/florida/orlando/{city_slug}"

def get_kbhome_url(city, community):
    """KB Home URL"""
    return "https://www.kbhome.com/new-homes-orlando"

def get_taylor_morrison_url(city, community):
    """Taylor Morrison URL"""
    return "https://www.taylormorrison.com/new-homes/florida/orlando"

def main():
    conn = get_db()
    
    # Get all properties with their community and builder info
    cursor = conn.execute("""
        SELECT pt.id, pt.name as floorplan, pt.url as current_url,
               c.name as community, c.city, c.builder
        FROM property_types pt
        JOIN communities c ON pt.community_id = c.id
    """)
    
    properties = cursor.fetchall()
    updated = 0
    
    for prop in properties:
        prop_id = prop['id']
        floorplan = prop['floorplan']
        community = prop['community']
        city = prop['city']
        builder = prop['builder']
        
        # Generate new URL based on builder
        if builder == "Lennar":
            new_url = get_lennar_url(city, community, floorplan)
        elif builder == "DR Horton":
            new_url = get_drhorton_url(city, community)
        elif builder == "Meritage Homes":
            new_url = get_meritage_url(city, community, floorplan)
        elif builder == "Pulte Homes":
            new_url = get_pulte_url(city, community)
        elif builder == "KB Home":
            new_url = get_kbhome_url(city, community)
        elif builder == "Taylor Morrison":
            new_url = get_taylor_morrison_url(city, community)
        else:
            continue
        
        # Update the URL
        conn.execute("UPDATE property_types SET url = ? WHERE id = ?", (new_url, prop_id))
        print(f"✅ {builder} | {floorplan} @ {community}")
        print(f"   → {new_url}")
        updated += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Updated {updated} property URLs")

if __name__ == "__main__":
    main()

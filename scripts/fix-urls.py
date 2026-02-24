#!/usr/bin/env python3
"""Fix and validate builder URLs in the database"""
import sys
sys.path.insert(0, '.')
from db import init_db, get_db

init_db()
conn = get_db()

# Correct URL patterns for each builder
URL_FIXES = {
    "DR Horton": {
        # DR Horton doesn't currently have Orlando-area communities 
        # Mark URLs as needing update
        "community_url": "https://www.drhorton.com/florida",  # Redirect to Florida page
        "plan_url": None  # Clear individual plan URLs
    },
    "KB Home": {
        # KB Home Orlando page exists but shows no communities
        "community_url": "https://www.kbhome.com/new-homes-orlando-area",
        "plan_url": None
    },
    "Meritage Homes": {
        # Meritage works
        "community_prefix": "https://www.meritagehomes.com/state/fl/orlando/"
    },
    "Taylor Morrison": {
        # Taylor Morrison redirects
        "community_url": "https://www.taylormorrison.com/fl"
    }
}

def fix_urls():
    cursor = conn.cursor()
    
    # Fix DR Horton - just update to community-level URLs
    print("Fixing DR Horton URLs...")
    cursor.execute('''
        UPDATE property_types 
        SET url = (
            SELECT c.url FROM communities c WHERE c.id = property_types.community_id
        )
        WHERE community_id IN (SELECT id FROM communities WHERE builder = 'DR Horton')
    ''')
    print(f"  Updated {cursor.rowcount} DR Horton floor plan URLs")
    
    # Fix KB Home
    print("Fixing KB Home URLs...")
    cursor.execute('''
        UPDATE communities SET url = 'https://www.kbhome.com/new-homes-orlando-area'
        WHERE builder = 'KB Home'
    ''')
    cursor.execute('''
        UPDATE property_types 
        SET url = 'https://www.kbhome.com/new-homes-orlando-area'
        WHERE community_id IN (SELECT id FROM communities WHERE builder = 'KB Home')
    ''')
    print(f"  Updated KB Home URLs")
    
    # Fix Taylor Morrison
    print("Fixing Taylor Morrison URLs...")
    cursor.execute('''
        UPDATE communities SET url = 'https://www.taylormorrison.com/fl'
        WHERE builder = 'Taylor Morrison'
    ''')
    cursor.execute('''
        UPDATE property_types 
        SET url = 'https://www.taylormorrison.com/fl'
        WHERE community_id IN (SELECT id FROM communities WHERE builder = 'Taylor Morrison')
    ''')
    print(f"  Updated Taylor Morrison URLs")
    
    conn.commit()
    print("\n✅ URL fixes applied")
    
    # Summary
    print("\n=== URL Summary by Builder ===")
    for row in cursor.execute('''
        SELECT c.builder, COUNT(DISTINCT c.id) as communities, COUNT(p.id) as plans,
               GROUP_CONCAT(DISTINCT SUBSTR(c.url, 1, 50)) as sample_url
        FROM communities c
        LEFT JOIN property_types p ON p.community_id = c.id
        GROUP BY c.builder
        ORDER BY c.builder
    '''):
        print(f"{row[0]}: {row[1]} communities, {row[2]} plans")
        print(f"  Sample URL: {row[3][:60]}...")

if __name__ == "__main__":
    fix_urls()

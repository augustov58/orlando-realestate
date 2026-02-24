#!/usr/bin/env python3
"""
Parse Lennar Orlando listings and update database with real URLs and prices.
"""
import re
import sys
sys.path.insert(0, '.')
from db import init_db, add_community, add_property_type, get_community_by_name, get_db

init_db()

# Raw data from Lennar Orlando page
RAW_DATA = """
[Move-in ready$458,4904 bd3 ba1 half ba2,183 ft²3118 Granite Ridge Avenue Minneola, FLHomesite #0468Lucia in Sugarloaf Ridge](/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/lucia/11183720468)
[Move-in ready$348,9904 bd3 ba2,109 ft²2705 LOOKOUT RIDGE ROAD Haines City, FLHomesite #3930Freedom in Hamilton Bluff](/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/freedom/26320723930)
[Move-in ready$369,9994 bd3 ba2,692 ft²809 HOUSE BOULEVARD Haines City, FLHomesite #0002Jagger in Groves at Grenelefe](/new-homes/florida/orlando/haines-city/groves-at-grenelefe/classic-collection/jagger/26341730002)
[Next GenMove-in ready$502,9904 bd3 ba2,109 ft²5631 NINA WAY Saint Cloud, FLHomesite #0028Freedom in Bridgewalk](/new-homes/florida/orlando/saint-cloud/bridgewalk/estate-collection2/freedom/26302720028)
[Move-in ready$340,9904 bd3 ba2,109 ft²3024 Chicago Avenue Haines City, FLHomesite #3702Freedom in Hamilton Bluff](/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/freedom/26320723702)
[Move-in ready$345,9904 bd3 ba2,109 ft²2905 Yukon Trail Drive Haines City, FLHomesite #3612Freedom in Hamilton Bluff](/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/freedom/26320723612)
[Move-in ready$310,7405 bd3 ba2,451 ft²3095 TOTEM ROAD Eagle Lake, FLHomesite #0591Eclipse in Ranches at Lake McLeod](/new-homes/florida/orlando/eagle-lake/ranches-at-lake-mcleod/estate-key-collection/eclipse/26332730591)
[Move-in ready$380,9905 bd2 ba1 half ba2,112 ft²5455 MEADOW WALK DRIVE Davenport, FLHomesite #3114Edison in Wynnstone](/new-homes/florida/orlando/davenport/wynnstone/manor-key-collection/edison/26315723114)
[Move-in ready$299,2406 bd3 ba2,463 ft²3623 HARDMAN DRIVE Lake Wales, FLHomesite #0287Jefferson in Hunt Club Groves](/new-homes/florida/orlando/lake-wales/hunt-club-groves/manor-key-collection/jefferson/11161720287)
[Move-in ready$329,2404 bd3 ba2,205 ft²3163 TOTEM ROAD Eagle Lake, FLHomesite #0574Bravo in Ranches at Lake McLeod](/new-homes/florida/orlando/eagle-lake/ranches-at-lake-mcleod/executive-key-collection/bravo/11129720574)
[Move-in ready$269,9904 bd2 ba1,824 ft²2913 Yukon Trial Drive Haines City, FLHomesite #3610Celeste in Hamilton Bluff](/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/celeste/26320723610)
[Move-in ready$393,9905 bd3 ba2,451 ft²3628 ROLLING RIDGE BEND Davenport, FLHomesite #2316Eclipse in Wynnstone](/new-homes/florida/orlando/davenport/wynnstone/estate-key-collection/eclipse/26316722316)
[Move-in ready$510,9004 bd3 ba1 half ba2,911 ft²721 TUNDRA LOOP Groveland, FLHomesite #M053Lakewood in Meadow Pointe](/new-homes/florida/orlando/groveland/meadow-pointe/legacy-collection/lakewood/2636172m053)
[Move-in ready$470,9904 bd3 ba2,199 ft²671 TERRAPIN DRIVE Debary, FLHomesite #0682Aspen in Rivington](/new-homes/florida/orlando/debary/rivington/estate-collection/aspen/26312720682)
[Move-in ready$284,9905 bd2 ba1 half ba2,112 ft²6444 Domizio Drive Winter Haven, FLHomesite #0250Edison in Villa Mar](/new-homes/florida/orlando/winter-haven/villa-mar/edison/26362720250)
[Move-in ready$480,9904 bd3 ba2,199 ft²3251 ADDISON BOULEVARD Saint Cloud, FLHomesite #0233Aspen in Bridgewalk](/new-homes/florida/orlando/saint-cloud/bridgewalk/estate-collection2/aspen/26302720233)
[Move-in ready$489,4905 bd3 ba2,601 ft²3110 Granite Ridge Avenue Minneola, FLHomesite #0466Santo in Sugarloaf Ridge](/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/santo/11183720466)
[Move-in ready$374,9994 bd3 ba2,692 ft²821 HOUSE BOULEVARD Haines City, FLHomesite #0005Jagger in Groves at Grenelefe](/new-homes/florida/orlando/haines-city/groves-at-grenelefe/classic-collection/jagger/26341730005)
[Move-in ready$285,7405 bd2 ba1 half ba2,112 ft²3370 ALEXANDER DRIVE Lake Wales, FLHomesite #0153Edison in Hunt Club Groves](/new-homes/florida/orlando/lake-wales/hunt-club-groves/manor-key-collection/edison/11161720153)
[Move-in ready$542,9904 bd3 ba2,650 ft²4076 EAST MINSTER ROAD Davenport, FLHomesite #0541Riviera in Providence](/new-homes/florida/orlando/davenport/providence/garden-hills-chateau-collection/riviera/11144720541)
[Move-in ready$283,2404 bd2 ba1,824 ft²303 Artemis Street Lake Wales, FLHomesite #S007Celeste in Hunt Club Groves](/new-homes/florida/orlando/lake-wales/hunt-club-groves/estate-key-collections/celeste/1116272s007)
[Move-in ready$321,9905 bd2 ba1 half ba2,112 ft²3878 AMERS LOOP Haines City, FLHomesite #0409Edison in Crosswinds](/new-homes/florida/orlando/haines-city/crosswinds/manor-key-collection/edison/11135720409)
[Move-in ready$294,9994 bd2 ba1,875 ft²813 HOUSE BOULEVARD Haines City, FLHomesite #0003Walsh in Groves at Grenelefe](/new-homes/florida/orlando/haines-city/groves-at-grenelefe/classic-collection/walsh/26341730003)
[Move-in ready$333,9004 bd3 ba2,174 ft²1912 PINE MEADOWS GOLFCOURSE R Eustis, FLHomesite #0314Dawn in Pine Meadows](/new-homes/florida/orlando/eustis/pine-meadows/estate-key-collection/dawn/26347720314)
[Move-in ready$313,9004 bd2 ba1,824 ft²1910 PINE MEADOWS GOLFCOURSE R Eustis, FLHomesite #0315Celeste in Pine Meadows](/new-homes/florida/orlando/eustis/pine-meadows/estate-key-collection/celeste/26347720315)
[Move-in ready$374,7804 bd3 ba2,174 ft²5674 Portico Place Kissimmee, FLHomesite #0381Dawn in Westview](/new-homes/florida/orlando/kissimmee/westview/aden-south-key-iii/dawn/26335730381)
[Move-in ready$279,9904 bd2 ba1 half ba1,874 ft²6448 Domizio Drive Winter Haven, FLHomesite #0251Columbus in Villa Mar](/new-homes/florida/orlando/winter-haven/villa-mar/columbus/26362720251)
[Move-in ready$517,1405 bd3 ba2,455 ft²2981 GOOD VIBES WAY Clermont, FLHomesite #1000Delray in Wellness Ridge](/new-homes/florida/orlando/clermont/wellness-ridge/manor-collection/delray/11139721000)
[Move-in ready$458,4904 bd3 ba1 half ba2,183 ft²3118 Granite Ridge Avenue Minneola, FLHomesite #0468Lucia in Sugarloaf Ridge](/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/lucia/11183720468)
[Move-in ready$533,4904 bd3 ba2,692 ft²3127 Granite Ridge Avenue Minneola, FLHomesite #0481Jagger in Sugarloaf Ridge](/new-homes/florida/orlando/minneola/sugarloaf-ridge/classic-collection/jagger/11184720481)
[Move-in ready$465,4904 bd2 ba1 half ba2,081 ft²3114 Granite Ridge Avenue Minneola, FLHomesite #0467Capri in Sugarloaf Ridge](/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/capri/11183720467)
"""

def parse_listing(line):
    """Parse a single listing line"""
    # Extract URL
    url_match = re.search(r'\]\((\/new-homes\/[^)]+)\)', line)
    if not url_match:
        return None
    
    url = "https://www.lennar.com" + url_match.group(1)
    
    # Extract price - format is $XXX,XXX followed by number of beds
    # e.g., "$348,9904 bd" means $348,990 and 4 bd
    price_beds_match = re.search(r'\$([0-9,]+)(\d)\s*bd', line)
    if price_beds_match:
        price_str = price_beds_match.group(1)
        beds = int(price_beds_match.group(2))
        price = int(price_str.replace(',', ''))
    else:
        price = None
        beds = None
    
    # Extract baths (handle "3 ba" or "3 ba1 half ba" format)
    baths_match = re.search(r'(\d+)\s*ba', line)
    half_bath = 'half ba' in line
    baths = float(baths_match.group(1)) + (0.5 if half_bath else 0) if baths_match else None
    
    # Extract sqft - format is X,XXX ft²
    sqft_match = re.search(r'([\d,]+)\s*ft', line)
    sqft = int(sqft_match.group(1).replace(',', '')) if sqft_match else None
    
    # Extract floor plan and community from URL
    url_parts = url_match.group(1).split('/')
    # /new-homes/florida/orlando/{city}/{community}/{collection}/{floorplan}/{id}
    if len(url_parts) >= 8:
        city = url_parts[4].replace('-', ' ').title()
        community = url_parts[5].replace('-', ' ').title()
        collection = url_parts[6]
        floorplan = url_parts[7].title()
    else:
        return None
    
    # Check for Next Gen (in-law suite)
    is_nextgen = 'Next Gen' in line
    
    return {
        'city': city,
        'community': community,
        'collection': collection,
        'floorplan': floorplan,
        'beds': beds,
        'baths': baths,
        'sqft': sqft,
        'price': price,
        'url': url,
        'nextgen': is_nextgen
    }

def main():
    listings = []
    for line in RAW_DATA.strip().split('\n'):
        if line.strip():
            parsed = parse_listing(line)
            if parsed:
                listings.append(parsed)
    
    print(f"📥 Parsed {len(listings)} listings from Lennar\n")
    
    # Clear existing Lennar data and re-add with real URLs
    conn = get_db()
    conn.execute("DELETE FROM property_types WHERE community_id IN (SELECT id FROM communities WHERE builder = 'Lennar')")
    conn.execute("DELETE FROM communities WHERE builder = 'Lennar'")
    conn.commit()
    conn.close()
    
    # Group by community
    communities = {}
    for l in listings:
        key = (l['community'], l['city'])
        if key not in communities:
            communities[key] = []
        communities[key].append(l)
    
    added_communities = 0
    added_properties = 0
    
    for (community, city), props in communities.items():
        # Get community URL (without specific listing ID)
        community_url = '/'.join(props[0]['url'].split('/')[:-2])
        
        cid = add_community(
            name=community,
            builder="Lennar",
            city=city,
            url=community_url
        )
        
        if cid > 0:
            added_communities += 1
            print(f"✅ {community} ({city})")
        else:
            existing = get_community_by_name(community, "Lennar")
            cid = existing['id'] if existing else None
            if not cid:
                continue
        
        # Add unique floor plans (by name)
        seen_plans = {}
        for p in props:
            plan_key = p['floorplan']
            # Only add if meets criteria (4+ beds, under $550k) OR keep best price for each plan
            if p['beds'] and p['beds'] >= 4 and p['price'] and p['price'] <= 550000:
                if plan_key not in seen_plans or p['price'] < seen_plans[plan_key]['price']:
                    seen_plans[plan_key] = p
        
        for plan_name, p in seen_plans.items():
            pid = add_property_type(
                community_id=cid,
                name=plan_name,
                bedrooms=p['beds'],
                bathrooms=p['baths'],
                sqft=p['sqft'],
                current_price=p['price'],
                has_inlaw_suite=p['nextgen'],
                url=p['url']
            )
            if pid > 0:
                added_properties += 1
                nextgen_flag = " 👴 NEXT GEN" if p['nextgen'] else ""
                print(f"   + {plan_name}: {p['beds']}BR ${p['price']:,} → {p['url'][-20:]}{nextgen_flag}")
    
    print(f"\n📊 Lennar Summary:")
    print(f"   Communities: {added_communities}")
    print(f"   Floor Plans (4+BR <$550k): {added_properties}")

if __name__ == "__main__":
    main()

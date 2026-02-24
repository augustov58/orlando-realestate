---
name: orlando-realestate
description: Research Orlando area new construction homes. Track communities, property types, builder incentives, and financing deals. Focus on 4BR+ single family homes and in-law suites under $550k.
---

# Orlando Real Estate Research

Track new construction homes in the greater Orlando, FL area with a focus on builder communities and incentives.

## Target Criteria

- **Property Type:** Single family homes, in-law suites/multi-gen
- **Bedrooms:** 4+
- **Max Price:** $550,000
- **Key Features:** Builder incentives, rate buy-downs, closing cost credits

## Database Structure

Properties are tracked by **community** (builder development), not individual listings:
- Each community can have multiple property types/floor plans
- Track incentives separately (they change frequently)
- Avoid duplicate entries for same floor plan in same community

## Sources

### Builder Websites (Primary)
- **Lennar** - lennar.com (Orlando/Central FL)
- **DR Horton** - drhorton.com/florida
- **Pulte Homes** - pulte.com
- **Taylor Morrison** - taylormorrison.com
- **Meritage Homes** - meritagehomes.com
- **KB Home** - kbhome.com
- **M/I Homes** - mihomes.com
- **Toll Brothers** - tollbrothers.com
- **Beazer Homes** - beazer.com
- **Richmond American** - richmondhomes.com

### Aggregators
- **NewHomeSource** - newhomesource.com
- **BDX/Builder Homesite** - builderonline.com
- **Realtor.com** (new construction filter)
- **Zillow** (new construction filter)

## Usage

```bash
# Add a community manually
python3 ./scripts/add-community.py "Community Name" "Builder" "City" "https://url"

# Add a property type to a community
python3 ./scripts/add-property.py --community "Community Name" --type "Floor Plan" --beds 4 --baths 3 --sqft 2500 --price 450000

# Add/update incentives
python3 ./scripts/update-incentives.py --community "Community Name" --rate-buydown "5.99%" --closing-credit 15000 --expires "2024-03-31"

# Search web for new communities
python3 ./scripts/search-builders.py "Orlando 4 bedroom new construction"

# Run dashboard
streamlit run dashboard.py
```

## Dashboard Features

- **Community Map:** Geographic view of all tracked communities
- **Price Comparison:** Compare similar floor plans across builders
- **Incentive Tracker:** Current deals with expiration dates
- **Monthly Payment Calculator:** Factor in rate buy-downs
- **Alerts:** Notify when new communities or incentives appear

## Orlando Areas of Interest

- Lake Nona
- Horizon West
- Winter Garden
- Clermont
- St. Cloud
- Kissimmee
- Apopka
- Sanford
- Davenport
- Champions Gate

## Telegram Delivery
- **Group:** -1003777728309 (topic: 1013)

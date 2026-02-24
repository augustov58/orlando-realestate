#!/usr/bin/env python3
"""
Orlando Real Estate Dashboard
Focus on new construction, communities, and builder incentives.
Run with: streamlit run dashboard.py
"""

import streamlit as st

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="🏠 Orlando Real Estate",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import sqlite3
import traceback

# Add scripts to path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR / 'scripts'))

# Import db module with error handling
DB_AVAILABLE = False
try:
    from db import get_all_listings, get_communities, get_active_incentives, get_stats, get_db, init_db, add_community, add_property_type, add_incentive, get_community_by_name
    # Ensure database is initialized
    init_db()
    DB_AVAILABLE = True
except Exception as e:
    st.error(f"Database initialization error: {e}")
    st.code(traceback.format_exc())
    # Continue without database - show empty state

# Populate sample data if database is empty
def slugify(text):
    """Convert text to URL slug"""
    return text.lower().replace(' ', '-').replace("'", "")

# Lennar floor plan to collection mapping
LENNAR_COLLECTIONS = {
    "Freedom": "estate-key-collection", "Celeste": "estate-key-collection", "Dawn": "estate-key-collection",
    "Eclipse": "estate-key-collection", "Bravo": "executive-key-collection", "Edison": "manor-key-collection",
    "Jefferson": "manor-key-collection", "Columbus": "manor-key-collection", "Jagger": "classic-collection",
    "Walsh": "classic-collection", "Lucia": "eventide-collection", "Santo": "eventide-collection",
    "Capri": "eventide-collection", "Lakewood": "legacy-collection", "Aspen": "estate-collection",
    "Riviera": "chateau-collection", "Delray": "manor-collection",
}

def get_lennar_url(city, community, floorplan):
    """Generate Lennar floor plan URL"""
    collection = LENNAR_COLLECTIONS.get(floorplan, "estate-collection")
    return f"https://www.lennar.com/new-homes/florida/orlando/{slugify(city)}/{slugify(community)}/{collection}/{slugify(floorplan)}"

def populate_sample_data():
    """Add sample data if database is empty - uses real scraped URLs"""
    stats = get_stats()
    if stats.get('communities', 0) > 0:
        return  # Already has data
    
    # Lennar communities with REAL URLs from scraping (Feb 2026)
    lennar_data = [
        {"community": "Hamilton Bluff", "city": "Haines City",
         "properties": [
             {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 340990, "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/freedom/26320723702"},
             {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 269990, "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/hamilton-bluff/estate-key-collection/celeste/26320723610"},
         ]},
        {"community": "Groves at Grenelefe", "city": "Haines City",
         "properties": [
             {"name": "Jagger", "beds": 4, "baths": 3, "sqft": 2692, "price": 369999, "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/groves-at-grenelefe/classic-collection/jagger/26341730002"},
             {"name": "Walsh", "beds": 4, "baths": 2, "sqft": 1875, "price": 294999, "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/groves-at-grenelefe/classic-collection/walsh/26341730003"},
         ]},
        {"community": "Ranches at Lake McLeod", "city": "Eagle Lake",
         "properties": [
             {"name": "Eclipse", "beds": 5, "baths": 3, "sqft": 2451, "price": 310740, "url": "https://www.lennar.com/new-homes/florida/orlando/eagle-lake/ranches-at-lake-mcleod/estate-key-collection/eclipse/26332730591"},
             {"name": "Bravo", "beds": 4, "baths": 3, "sqft": 2205, "price": 329240, "url": "https://www.lennar.com/new-homes/florida/orlando/eagle-lake/ranches-at-lake-mcleod/executive-key-collection/bravo/11129720574"},
         ]},
        {"community": "Hunt Club Groves", "city": "Lake Wales",
         "properties": [
             {"name": "Jefferson", "beds": 6, "baths": 3, "sqft": 2463, "price": 299240, "url": "https://www.lennar.com/new-homes/florida/orlando/lake-wales/hunt-club-groves/manor-key-collection/jefferson/11161720287"},
             {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 285740, "url": "https://www.lennar.com/new-homes/florida/orlando/lake-wales/hunt-club-groves/manor-key-collection/edison/11161720153"},
             {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 283240, "url": "https://www.lennar.com/new-homes/florida/orlando/lake-wales/hunt-club-groves/estate-key-collections/celeste/1116272s007"},
         ]},
        {"community": "Villa Mar", "city": "Winter Haven",
         "properties": [
             {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 284990, "url": "https://www.lennar.com/new-homes/florida/orlando/winter-haven/villa-mar/edison/26362720250"},
             {"name": "Columbus", "beds": 4, "baths": 2.5, "sqft": 1874, "price": 279990, "url": "https://www.lennar.com/new-homes/florida/orlando/winter-haven/villa-mar/columbus/26362720251"},
         ]},
        {"community": "Wynnstone", "city": "Davenport",
         "properties": [
             {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 380990, "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/wynnstone/manor-key-collection/edison/26315723114"},
             {"name": "Eclipse", "beds": 5, "baths": 3, "sqft": 2451, "price": 393990, "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/wynnstone/estate-key-collection/eclipse/26316722316"},
         ]},
        {"community": "Crosswinds", "city": "Haines City",
         "properties": [
             {"name": "Edison", "beds": 5, "baths": 2.5, "sqft": 2112, "price": 321990, "url": "https://www.lennar.com/new-homes/florida/orlando/haines-city/crosswinds/manor-key-collection/edison/11135720409"},
         ]},
        {"community": "Pine Meadows", "city": "Eustis",
         "properties": [
             {"name": "Dawn", "beds": 4, "baths": 3, "sqft": 2174, "price": 333900, "url": "https://www.lennar.com/new-homes/florida/orlando/eustis/pine-meadows/estate-key-collection/dawn/26347720314"},
             {"name": "Celeste", "beds": 4, "baths": 2, "sqft": 1824, "price": 313900, "url": "https://www.lennar.com/new-homes/florida/orlando/eustis/pine-meadows/estate-key-collection/celeste/26347720315"},
         ]},
        {"community": "Westview", "city": "Kissimmee",
         "properties": [
             {"name": "Dawn", "beds": 4, "baths": 3, "sqft": 2174, "price": 374780, "url": "https://www.lennar.com/new-homes/florida/orlando/kissimmee/westview/aden-south-key-iii/dawn/26335730381"},
         ]},
        {"community": "Sugarloaf Ridge", "city": "Minneola",
         "properties": [
             {"name": "Lucia", "beds": 4, "baths": 3.5, "sqft": 2183, "price": 458490, "url": "https://www.lennar.com/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/lucia/11183720468"},
             {"name": "Santo", "beds": 5, "baths": 3, "sqft": 2601, "price": 489490, "url": "https://www.lennar.com/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/santo/11183720466"},
             {"name": "Capri", "beds": 4, "baths": 2.5, "sqft": 2081, "price": 465490, "url": "https://www.lennar.com/new-homes/florida/orlando/minneola/sugarloaf-ridge/eventide-collection/capri/11183720467"},
             {"name": "Jagger", "beds": 4, "baths": 3, "sqft": 2692, "price": 533490, "url": "https://www.lennar.com/new-homes/florida/orlando/minneola/sugarloaf-ridge/classic-collection/jagger/11184720481"},
         ]},
        {"community": "Bridgewalk", "city": "Saint Cloud",
         "properties": [
             {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 480990, "url": "https://www.lennar.com/new-homes/florida/orlando/saint-cloud/bridgewalk/estate-collection2/aspen/26302720233"},
             {"name": "Freedom", "beds": 4, "baths": 3, "sqft": 2109, "price": 502990, "url": "https://www.lennar.com/new-homes/florida/orlando/saint-cloud/bridgewalk/estate-collection2/freedom/26302720028", "nextgen": True},
         ]},
        {"community": "Rivington", "city": "Debary",
         "properties": [
             {"name": "Aspen", "beds": 4, "baths": 3, "sqft": 2199, "price": 470990, "url": "https://www.lennar.com/new-homes/florida/orlando/debary/rivington/estate-collection/aspen/26312720682"},
         ]},
        {"community": "Meadow Pointe", "city": "Groveland",
         "properties": [
             {"name": "Lakewood", "beds": 4, "baths": 3.5, "sqft": 2911, "price": 510900, "url": "https://www.lennar.com/new-homes/florida/orlando/groveland/meadow-pointe/legacy-collection/lakewood/2636172m053"},
         ]},
        {"community": "Wellness Ridge", "city": "Clermont",
         "properties": [
             {"name": "Delray", "beds": 5, "baths": 3, "sqft": 2455, "price": 517140, "url": "https://www.lennar.com/new-homes/florida/orlando/clermont/wellness-ridge/manor-collection/delray/11139721000"},
         ]},
        {"community": "Providence", "city": "Davenport",
         "properties": [
             {"name": "Riviera", "beds": 4, "baths": 3, "sqft": 2650, "price": 542990, "url": "https://www.lennar.com/new-homes/florida/orlando/davenport/providence/garden-hills-chateau-collection/riviera/11144720541"},
         ]},
    ]
    
    # Add Lennar communities with real URLs
    for data in lennar_data:
        community_url = f"https://www.lennar.com/new-homes/florida/orlando/{slugify(data['city'])}/{slugify(data['community'])}"
        cid = add_community(name=data["community"], builder="Lennar", city=data["city"], url=community_url)
        if cid < 0:
            existing = get_community_by_name(data["community"], "Lennar")
            cid = existing["id"] if existing else None
        if cid:
            for prop in data["properties"]:
                add_property_type(community_id=cid, name=prop["name"], bedrooms=prop["beds"],
                                  bathrooms=prop["baths"], sqft=prop["sqft"], current_price=prop["price"],
                                  has_inlaw_suite=prop.get("nextgen", False), url=prop["url"])
    
    # Add Lennar incentive
    add_incentive(builder="Lennar", type="combo", description="Rate buydown + closing costs with Lennar Mortgage",
                  rate_buydown="5.99% for 30yr fixed", rate_after_buydown=5.99, closing_credit=10000,
                  terms="Must use Lennar Mortgage. On select move-in ready homes.", lender_required="Lennar Mortgage",
                  expires_at="2026-03-31", source_url="https://www.lennar.com")
    
    # DR Horton communities (uses dynamic URLs - link to Orlando metro search)
    dr_horton_data = [
        {"community": "Astonia", "city": "Davenport", "properties": [
            {"name": "Bluebell", "beds": 4, "baths": 2, "sqft": 1850, "price": 319990},
            {"name": "Lantana", "beds": 5, "baths": 3, "sqft": 2580, "price": 389990}]},
        {"community": "Sunstone", "city": "Sanford", "properties": [
            {"name": "Columbia", "beds": 4, "baths": 2, "sqft": 1875, "price": 359990},
            {"name": "Juniper", "beds": 5, "baths": 3, "sqft": 2650, "price": 439990}]},
        {"community": "Citrus Trails", "city": "Haines City", "properties": [
            {"name": "Jasmine", "beds": 4, "baths": 2, "sqft": 1750, "price": 289990},
            {"name": "Willow", "beds": 5, "baths": 3, "sqft": 2400, "price": 359990}]},
    ]
    drhorton_url = "https://www.drhorton.com/florida/orlando-metro"
    for data in dr_horton_data:
        cid = add_community(name=data["community"], builder="DR Horton", city=data["city"], url=drhorton_url)
        if cid < 0:
            existing = get_community_by_name(data["community"], "DR Horton")
            cid = existing["id"] if existing else None
        if cid:
            for prop in data["properties"]:
                add_property_type(community_id=cid, name=prop["name"], bedrooms=prop["beds"],
                                  bathrooms=prop["baths"], sqft=prop["sqft"], current_price=prop["price"],
                                  url=drhorton_url)
    add_incentive(builder="DR Horton", type="combo", description="$15k closing costs with DHI Mortgage",
                  closing_credit=15000, rate_buydown="5.75% available", expires_at="2026-03-31")
    
    # Meritage Homes (link to community pages)
    meritage_data = [
        {"community": "Lake Apopka Reserve", "city": "Apopka", "properties": [
            {"name": "Cholla", "beds": 4, "baths": 2.5, "sqft": 2050, "price": 399900},
            {"name": "Palo Verde", "beds": 4, "baths": 3, "sqft": 2350, "price": 449900}]},
        {"community": "Cypress Preserve", "city": "Groveland", "properties": [
            {"name": "Acacia", "beds": 4, "baths": 2.5, "sqft": 1950, "price": 369900},
            {"name": "Ironwood", "beds": 5, "baths": 3, "sqft": 2550, "price": 429900}]},
    ]
    for data in meritage_data:
        meritage_url = f"https://www.meritagehomes.com/state/fl/orlando/{slugify(data['community'])}"
        cid = add_community(name=data["community"], builder="Meritage Homes", city=data["city"], url=meritage_url)
        if cid < 0:
            existing = get_community_by_name(data["community"], "Meritage Homes")
            cid = existing["id"] if existing else None
        if cid:
            for prop in data["properties"]:
                add_property_type(community_id=cid, name=prop["name"], bedrooms=prop["beds"],
                                  bathrooms=prop["baths"], sqft=prop["sqft"], current_price=prop["price"],
                                  url=meritage_url)
    
    # KB Home (link to Orlando search)
    kb_data = [
        {"community": "Lakeshore at Narcoossee", "city": "Saint Cloud", "properties": [
            {"name": "Plan 1989", "beds": 4, "baths": 2.5, "sqft": 1989, "price": 369990},
            {"name": "Plan 2668", "beds": 5, "baths": 3, "sqft": 2668, "price": 449990}]},
        {"community": "Gramercy Farms", "city": "Saint Cloud", "properties": [
            {"name": "Plan 1707", "beds": 4, "baths": 2, "sqft": 1707, "price": 329990}]},
    ]
    kb_url = "https://www.kbhome.com/new-homes-orlando"
    for data in kb_data:
        cid = add_community(name=data["community"], builder="KB Home", city=data["city"], url=kb_url)
        if cid < 0:
            existing = get_community_by_name(data["community"], "KB Home")
            cid = existing["id"] if existing else None
        if cid:
            for prop in data["properties"]:
                add_property_type(community_id=cid, name=prop["name"], bedrooms=prop["beds"],
                                  bathrooms=prop["baths"], sqft=prop["sqft"], current_price=prop["price"],
                                  url=kb_url)
    add_incentive(builder="KB Home", type="combo", description="$10k closing + rate buydown",
                  closing_credit=10000, rate_buydown="5.99% available", expires_at="2026-03-31")

# Run sample data population
if DB_AVAILABLE:
    try:
        populate_sample_data()
    except Exception as e:
        st.warning(f"Could not populate sample data: {e}")

# Mobile-friendly CSS
st.markdown("""
<style>
    .block-container {
        padding: 1rem 0.5rem !important;
        max-width: 100% !important;
    }
    
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 50% !important;
            flex: 0 0 50% !important;
            min-width: 0 !important;
        }
        .stMetric {
            padding: 0.3rem !important;
        }
        .stMetric label {
            font-size: 0.7rem !important;
        }
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
        h1 { font-size: 1.3rem !important; }
        h2 { font-size: 1.1rem !important; }
    }
    
    .incentive-card {
        background: linear-gradient(135deg, #1a5f2a 0%, #0d3d1a 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
    
    .inlaw-badge {
        background: #ff9800;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Target criteria
MAX_PRICE = 550000
MIN_BEDS = 4

# Orlando areas of interest
PREFERRED_AREAS = [
    'Lake Nona', 'Horizon West', 'Winter Garden', 'Clermont',
    'St. Cloud', 'Kissimmee', 'Apopka', 'Sanford', 'Davenport',
    'Champions Gate', 'Celebration', 'Oakland', 'Ocoee', 'Windermere'
]

def calculate_monthly_payment(price, rate, years=30, down_pct=0.05):
    """Calculate monthly P&I payment"""
    down = price * down_pct
    loan = price - down
    monthly_rate = rate / 100 / 12
    n_payments = years * 12
    
    if monthly_rate == 0:
        return loan / n_payments
    
    payment = loan * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    return payment

def calculate_total_monthly(price, rate, hoa=0, tax_rate=0.0095, insurance_rate=0.003, down_pct=0.05):
    """Calculate total monthly housing cost"""
    pi = calculate_monthly_payment(price, rate, down_pct=down_pct)
    taxes = (price * tax_rate) / 12
    insurance = (price * insurance_rate) / 12
    return pi + hoa + taxes + insurance

@st.cache_data(ttl=300)
@st.cache_data(ttl=300)
def load_data():
    """Load listings from database"""
    listings = get_all_listings()
    df = pd.DataFrame(listings)
    
    if len(df) == 0:
        return df
    
    # Calculate price per sqft
    df['price_per_sqft'] = df.apply(
        lambda r: r['current_price'] / r['sqft'] if r['current_price'] and r['sqft'] and r['sqft'] > 0 else None,
        axis=1
    )
    
    # Check if in preferred area
    df['is_preferred'] = df['city'].apply(
        lambda x: any(area.lower() in str(x).lower() for area in PREFERRED_AREAS) if pd.notna(x) else False
    )
    
    # Meets criteria
    df['meets_criteria'] = (
        (df['bedrooms'] >= MIN_BEDS) & 
        (df['current_price'] <= MAX_PRICE) &
        df['current_price'].notna()
    )
    
    return df

@st.cache_data(ttl=300)
def load_incentives():
    """Load active incentives"""
    return get_active_incentives()

def main():
    st.title("🏠 Orlando New Construction Dashboard")
    st.caption(f"Target: 4+ BR under $550k | In-law suites | Builder incentives")
    
    # Load data
    df = load_data()
    incentives = load_incentives()
    stats = get_stats()
    
    # Sidebar
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    
    st.sidebar.header("⚙️ Settings")
    dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.dark_mode = dark_mode
    plotly_template = "plotly_dark" if dark_mode else "plotly_white"
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")
    
    # Price range slider
    st.sidebar.subheader("💰 Price")
    max_filter = st.sidebar.slider(
        "Maximum Price",
        300000, 600000, MAX_PRICE,
        step=10000, format="$%d"
    )
    
    # Bedroom filter
    min_beds_filter = st.sidebar.number_input("Minimum Bedrooms", 1, 6, MIN_BEDS)
    
    # Builder filter
    if len(df) > 0:
        builders = ['All'] + sorted(df['builder'].dropna().unique().tolist())
        selected_builder = st.sidebar.selectbox("Builder", builders)
    else:
        selected_builder = 'All'
    
    # City filter
    if len(df) > 0:
        cities = ['All', '⭐ Preferred Areas'] + sorted(df['city'].dropna().unique().tolist())
        selected_city = st.sidebar.selectbox("City/Area", cities)
    else:
        selected_city = 'All'
    
    # In-law suite filter
    inlaw_only = st.sidebar.checkbox("🏠👴 In-Law Suite Only", False)
    
    # Payment calculator inputs
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Payment Calculator")
    interest_rate = st.sidebar.number_input("Interest Rate %", 4.0, 10.0, 6.5, step=0.125)
    down_payment_pct = st.sidebar.slider("Down Payment %", 3, 20, 5)
    
    # Apply filters
    if len(df) > 0:
        filtered = df.copy()
        filtered = filtered[filtered['current_price'] <= max_filter]
        filtered = filtered[filtered['bedrooms'] >= min_beds_filter]
        
        if selected_builder != 'All':
            filtered = filtered[filtered['builder'] == selected_builder]
        
        if selected_city == '⭐ Preferred Areas':
            filtered = filtered[filtered['is_preferred']]
        elif selected_city != 'All':
            filtered = filtered[filtered['city'] == selected_city]
        
        if inlaw_only:
            filtered = filtered[filtered['has_inlaw_suite'] == 1]
        
        # Calculate monthly payments
        filtered['monthly_payment'] = filtered.apply(
            lambda r: calculate_total_monthly(
                r['current_price'], 
                interest_rate,
                r['hoa_monthly'] or 0,
                down_pct=down_payment_pct/100
            ) if r['current_price'] else None,
            axis=1
        )
    else:
        filtered = df
    
    # Summary metrics
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.metric("🏘️ Communities", stats.get('communities', 0))
    
    with col2:
        st.metric("🏠 Floor Plans", len(filtered) if len(df) > 0 else 0)
    
    with col3:
        meets = len(filtered[filtered['meets_criteria']]) if len(df) > 0 else 0
        st.metric("✅ Meet Criteria", meets)
    
    with col4:
        inlaw_count = len(filtered[filtered['has_inlaw_suite'] == 1]) if len(df) > 0 else 0
        st.metric("👴 In-Law Suites", inlaw_count)
    
    # Active Incentives Section
    if incentives:
        st.header("💰 Active Builder Incentives")
        
        incentive_cols = st.columns(min(len(incentives), 3))
        for i, inc in enumerate(incentives[:6]):
            with incentive_cols[i % 3]:
                rate_info = f"**{inc['rate_buydown']}** rate" if inc.get('rate_buydown') else ""
                credit_info = f"**${inc['closing_credit']:,.0f}** credit" if inc.get('closing_credit') else ""
                expires = f"Expires: {inc['expires_at']}" if inc.get('expires_at') else ""
                
                st.markdown(f"""
                **{inc['builder']}** {f"- {inc['community_name']}" if inc.get('community_name') else '(All Communities)'}
                
                {rate_info} {credit_info}
                
                {inc.get('description', '')}
                
                *{expires}*
                """)
                st.markdown("---")
    
    if len(df) == 0:
        st.warning("No properties in database yet. Add communities and floor plans to get started!")
        st.markdown("""
        ### Getting Started
        
        1. **Add a community:**
        ```bash
        python3 scripts/db.py init  # Initialize database first
        ```
        
        2. Use the research tools to find and add communities
        3. Track builder incentives as you find them
        """)
        return
    
    # Map Section
    st.header("🗺️ Community Map")
    
    # City coordinates for Orlando area
    CITY_COORDS = {
        'Saint Cloud': (28.2489, -81.2812),
        'Haines City': (28.1142, -81.6179),
        'Eagle Lake': (27.9786, -81.7537),
        'Clermont': (28.5494, -81.7729),
        'Minneola': (28.5744, -81.7462),
        'Davenport': (28.1614, -81.6017),
        'Lake Wales': (27.9014, -81.5859),
        'Groveland': (28.5578, -81.8512),
        'Kissimmee': (28.2920, -81.4076),
        'Eustis': (28.8528, -81.6851),
        'Orlando': (28.5383, -81.3792),
        'Apopka': (28.6934, -81.5322),
        'Debary': (28.8831, -81.3239),
        'Winter Haven': (28.0222, -81.7329),
        'Lake Nona': (28.3677, -81.2319),
        'Horizon West': (28.4500, -81.6000),
        'Winter Garden': (28.5653, -81.5862),
        'Sanford': (28.8128, -81.2694),
        'Champions Gate': (28.3075, -81.6209),
        'Celebration': (28.3253, -81.5339),
        'Ocoee': (28.5692, -81.5439),
    }
    
    # Add coordinates to filtered data
    map_data = filtered.copy()
    map_data['lat'] = map_data['city'].map(lambda x: CITY_COORDS.get(x, (28.5, -81.5))[0])
    map_data['lon'] = map_data['city'].map(lambda x: CITY_COORDS.get(x, (28.5, -81.5))[1])
    
    # Add small random offset to prevent overlap
    np.random.seed(42)
    map_data['lat'] = map_data['lat'] + np.random.uniform(-0.02, 0.02, len(map_data))
    map_data['lon'] = map_data['lon'] + np.random.uniform(-0.02, 0.02, len(map_data))
    
    if len(map_data) > 0:
        # Create map with plotly
        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            color='city',
            size='current_price',
            size_max=20,
            hover_name='name',
            hover_data={
                'community_name': True,
                'builder': True,
                'current_price': ':$,.0f',
                'bedrooms': True,
                'sqft': ':,.0f',
                'lat': False,
                'lon': False,
            },
            zoom=8,
            center={'lat': 28.35, 'lon': -81.55},
            mapbox_style='carto-positron' if not dark_mode else 'carto-darkmatter',
        )
        
        fig_map.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", yanchor="top", y=-0.02, xanchor="center", x=0.5, font=dict(size=10)),
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    # Charts Section
    st.header("📈 Market Analysis")
    
    # Price vs Sqft scatter
    scatter_data = filtered[
        filtered['current_price'].notna() & 
        filtered['sqft'].notna() & 
        (filtered['sqft'] > 0)
    ].copy()
    
    if len(scatter_data) > 0:
        # Custom hover text
        scatter_data['hover_text'] = scatter_data.apply(
            lambda r: f"<b>{r['name']}</b><br>" +
                      f"📍 {r['community_name']} ({r['builder']})<br>" +
                      f"🏙️ {r['city']}<br>" +
                      f"💰 ${r['current_price']:,.0f}<br>" +
                      f"📐 {r['sqft']:,.0f} sqft (${r['price_per_sqft']:,.0f}/sqft)<br>" +
                      f"🛏️ {int(r['bedrooms'])}BR | 🛁 {r['bathrooms']}BA<br>" +
                      (f"👴 In-Law Suite<br>" if r['has_inlaw_suite'] else "") +
                      f"💳 ~${r['monthly_payment']:,.0f}/mo" if r.get('monthly_payment') else "",
            axis=1
        )
        
        fig = px.scatter(
            scatter_data,
            x='sqft',
            y='current_price',
            color='city',
            symbol='has_inlaw_suite',
            symbol_map={0: 'circle', 1: 'star'},
            custom_data=['url', 'community_name', 'city', 'monthly_payment', 'builder'],
            hover_data={
                'sqft': ':,.0f',
                'current_price': ':$,.0f',
                'city': True,
                'builder': True,
                'has_inlaw_suite': False
            },
            labels={'sqft': 'Square Feet', 'current_price': 'Price (USD)', 'city': 'Location'}
        )
        
        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
        
        # Add max price line
        fig.add_hline(y=MAX_PRICE, line_dash="dash", line_color="red", 
                      annotation_text=f"Max ${MAX_PRICE:,}")
        
        # Add trend line
        if len(scatter_data) > 2:
            z = np.polyfit(scatter_data['sqft'], scatter_data['current_price'], 1)
            x_line = np.linspace(scatter_data['sqft'].min(), scatter_data['sqft'].max(), 100)
            y_line = z[0] * x_line + z[1]
            
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode='lines', name='Trend',
                line=dict(color='gray', width=2, dash='dash'),
                hoverinfo='skip'
            ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=30, b=60),
            template=plotly_template,
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
            title="💰 Price vs Size (⭐ = In-Law Suite)"
        )
        
        scatter_data = scatter_data.reset_index(drop=True)
        selected_point = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_scatter")
        
        # Handle selection
        if selected_point and selected_point.selection and selected_point.selection.points:
            point = selected_point.selection.points[0]
            click_x = point.get('x')
            click_y = point.get('y')
            
            matching = scatter_data[
                (scatter_data['sqft'] == click_x) & 
                (scatter_data['current_price'] == click_y)
            ]
            
            if len(matching) > 0:
                clicked_row = matching.iloc[0]
                
                st.success(f"**Selected:** {clicked_row['name']} at {clicked_row['community_name']}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Price", f"${clicked_row['current_price']:,.0f}")
                with col2:
                    st.metric("Size", f"{clicked_row['sqft']:,.0f} sqft")
                with col3:
                    st.metric("$/sqft", f"${clicked_row['price_per_sqft']:,.0f}")
                with col4:
                    if clicked_row.get('monthly_payment'):
                        st.metric("Est. Monthly", f"${clicked_row['monthly_payment']:,.0f}")
                
                st.markdown(f"**Builder:** {clicked_row['builder']} | **City:** {clicked_row['city']}")
                if clicked_row.get('has_inlaw_suite'):
                    st.markdown("🏠👴 **Has In-Law Suite**")
                if clicked_row.get('url'):
                    st.markdown(f"🔗 **[View Listing]({clicked_row['url']})**")
    
    # Price by Builder comparison
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        builder_data = filtered[filtered['current_price'].notna()].copy()
        if len(builder_data) > 0:
            builder_avg = builder_data.groupby('builder').agg({
                'current_price': 'median',
                'name': 'count'
            }).reset_index()
            builder_avg.columns = ['builder', 'median_price', 'count']
            builder_avg = builder_avg.sort_values('median_price')
            
            fig = px.bar(
                builder_avg,
                x='median_price',
                y='builder',
                orientation='h',
                color='count',
                color_continuous_scale='Greens',
                labels={'median_price': 'Median Price', 'builder': '', 'count': 'Plans'}
            )
            fig.update_layout(
                height=300,
                template=plotly_template,
                margin=dict(l=10, r=10, t=30, b=10),
                title="🏗️ Price by Builder"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Monthly payment distribution
        payment_data = filtered[filtered['monthly_payment'].notna()].copy()
        if len(payment_data) > 0:
            fig = px.histogram(
                payment_data,
                x='monthly_payment',
                nbins=20,
                color='meets_criteria',
                color_discrete_map={True: '#27ae60', False: '#e74c3c'},
                labels={'monthly_payment': 'Monthly Payment', 'meets_criteria': 'Meets Criteria'}
            )
            fig.update_layout(
                height=300,
                template=plotly_template,
                margin=dict(l=10, r=10, t=30, b=10),
                title="💳 Monthly Payment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Properties Table
    st.header("🏠 Properties")
    
    search_query = st.text_input("🔍 Search", placeholder="Search by name, builder, community, city...")
    
    search_filtered = filtered.copy()
    if search_query:
        q = search_query.lower()
        search_filtered = filtered[
            filtered['name'].str.lower().str.contains(q, na=False) |
            filtered['builder'].str.lower().str.contains(q, na=False) |
            filtered['community_name'].str.lower().str.contains(q, na=False) |
            filtered['city'].str.lower().str.contains(q, na=False)
        ]
        st.caption(f"Showing {len(search_filtered)} of {len(filtered)} properties")
    
    # Prepare display
    display_cols = ['name', 'builder', 'community_name', 'city', 'current_price', 
                    'sqft', 'bedrooms', 'bathrooms', 'has_inlaw_suite', 'monthly_payment', 'url']
    display_df = search_filtered[display_cols].copy()
    
    display_df['has_inlaw_suite'] = display_df['has_inlaw_suite'].apply(lambda x: "👴" if x else "")
    
    display_df.columns = ['Floor Plan', 'Builder', 'Community', 'City', 'Price', 
                          'Sqft', 'BR', 'BA', 'In-Law', 'Monthly', 'URL']
    
    display_df = display_df.sort_values('Price')
    
    st.dataframe(
        display_df,
        column_config={
            "Price": st.column_config.NumberColumn("Price", format="$%,.0f"),
            "Sqft": st.column_config.NumberColumn("Sqft", format="%,.0f"),
            "Monthly": st.column_config.NumberColumn("Est. Monthly", format="$%,.0f"),
            "URL": st.column_config.LinkColumn("Link", display_text="View →"),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )
    
    # Top Picks Section
    st.header("⭐ Top Picks")
    st.caption("Properties meeting criteria: 4+ BR, under $550k, sorted by value")
    
    top_picks = filtered[
        filtered['meets_criteria'] & 
        filtered['price_per_sqft'].notna()
    ].copy()
    
    if len(top_picks) > 0:
        # Sort by price per sqft (best value)
        top_picks = top_picks.nlargest(10, 'sqft')  # Biggest for the money
        
        col1, col2 = st.columns(2)
        
        for i, (_, row) in enumerate(top_picks.iterrows()):
            inlaw_badge = "👴" if row['has_inlaw_suite'] else ""
            monthly = f"${row['monthly_payment']:,.0f}/mo" if row.get('monthly_payment') else ""
            
            card = f"""
**{row['name']}** {inlaw_badge}
📍 {row['community_name']} - {row['city']}
🏗️ {row['builder']}
💰 ${row['current_price']:,.0f} | 📐 {row['sqft']:,.0f} sqft | ${row['price_per_sqft']:,.0f}/sqft
🛏️ {int(row['bedrooms'])}BR | 🛁 {row['bathrooms']}BA | 💳 {monthly}
"""
            if row.get('url'):
                card += f"[View →]({row['url']})"
            
            with col1 if i % 2 == 0 else col2:
                st.markdown(card)
                st.markdown("---")
    else:
        st.info("No properties currently meet all criteria. Try adjusting filters.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Database: {stats.get('communities', 0)} communities, {stats.get('property_types', 0)} floor plans")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Run the app
if DB_AVAILABLE:
    main()
else:
    st.title("🏠 Orlando New Construction Dashboard")
    st.error("Database not available. Please check the logs.")
    st.info("The dashboard will show data once the database is properly initialized.")

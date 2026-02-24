#!/usr/bin/env python3
"""Minimal dashboard for debugging"""
import streamlit as st

st.set_page_config(page_title="🏠 Orlando Real Estate", page_icon="🏠")
st.title("🏠 Orlando Real Estate - Test")
st.write("If you see this, Streamlit is working!")

# Try imports one by one
try:
    import pandas as pd
    st.success("✓ pandas")
except Exception as e:
    st.error(f"✗ pandas: {e}")

try:
    import numpy as np
    st.success("✓ numpy")
except Exception as e:
    st.error(f"✗ numpy: {e}")

try:
    import plotly.express as px
    st.success("✓ plotly")
except Exception as e:
    st.error(f"✗ plotly: {e}")

try:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
    from db import init_db, get_stats, get_all_listings
    st.success("✓ db module imported")
    
    init_db()
    st.success("✓ db initialized")
    
    stats = get_stats()
    st.write(f"Communities: {stats.get('communities', 0)}")
    st.write(f"Properties: {stats.get('property_types', 0)}")
    
except Exception as e:
    import traceback
    st.error(f"✗ db error: {e}")
    st.code(traceback.format_exc())

st.write("---")
st.write("Startup complete!")

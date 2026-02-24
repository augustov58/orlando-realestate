#!/usr/bin/env python3
"""Minimal startup test for debugging Streamlit Cloud issues"""
import sys
print(f"Python: {sys.version}")

try:
    import streamlit as st
    print("✓ streamlit imported")
except Exception as e:
    print(f"✗ streamlit: {e}")

try:
    import pandas as pd
    print("✓ pandas imported")
except Exception as e:
    print(f"✗ pandas: {e}")

try:
    import numpy as np
    print("✓ numpy imported")
except Exception as e:
    print(f"✗ numpy: {e}")

try:
    import plotly.express as px
    print("✓ plotly imported")
except Exception as e:
    print(f"✗ plotly: {e}")

try:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
    from db import init_db, get_stats
    print("✓ db module imported")
    init_db()
    print("✓ db initialized")
    stats = get_stats()
    print(f"✓ stats: {stats}")
except Exception as e:
    import traceback
    print(f"✗ db: {e}")
    traceback.print_exc()

print("\n--- All imports successful ---")

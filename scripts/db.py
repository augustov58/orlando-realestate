#!/usr/bin/env python3
"""
SQLite database for Orlando real estate - community-based tracking.
Focus on new construction with builder incentives.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "listings.db"

def get_db():
    """Get database connection"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_db()
    conn.executescript("""
        -- Communities (builder developments)
        CREATE TABLE IF NOT EXISTS communities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            builder TEXT NOT NULL,
            city TEXT,
            zip_code TEXT,
            address TEXT,
            url TEXT,
            lat REAL,
            lng REAL,
            hoa_monthly REAL,
            amenities TEXT,
            status TEXT DEFAULT 'active',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, builder)
        );
        
        -- Property types / floor plans within communities
        CREATE TABLE IF NOT EXISTS property_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            bedrooms INTEGER,
            bathrooms REAL,
            sqft INTEGER,
            stories INTEGER DEFAULT 1,
            garage_spaces INTEGER DEFAULT 2,
            has_inlaw_suite BOOLEAN DEFAULT 0,
            base_price REAL,
            current_price REAL,
            price_updated_at TEXT,
            url TEXT,
            images TEXT,
            features TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(community_id, name),
            FOREIGN KEY (community_id) REFERENCES communities(id)
        );
        
        -- Builder incentives (change frequently)
        CREATE TABLE IF NOT EXISTS incentives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER,
            builder TEXT,
            type TEXT NOT NULL,
            description TEXT,
            rate_buydown TEXT,
            rate_after_buydown REAL,
            closing_credit REAL,
            other_value REAL,
            terms TEXT,
            lender_required TEXT,
            expires_at TEXT,
            source_url TEXT,
            verified_at TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (community_id) REFERENCES communities(id)
        );
        
        -- Price history for tracking changes
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_type_id INTEGER NOT NULL,
            price REAL NOT NULL,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_type_id) REFERENCES property_types(id)
        );
        
        -- Search/research log
        CREATE TABLE IF NOT EXISTS research_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            source TEXT,
            results_count INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Telegram notifications sent
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            reference_id INTEGER,
            group_id TEXT NOT NULL,
            topic_id TEXT,
            message_id TEXT,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_communities_builder ON communities(builder);
        CREATE INDEX IF NOT EXISTS idx_communities_city ON communities(city);
        CREATE INDEX IF NOT EXISTS idx_property_types_beds ON property_types(bedrooms);
        CREATE INDEX IF NOT EXISTS idx_property_types_price ON property_types(current_price);
        CREATE INDEX IF NOT EXISTS idx_incentives_active ON incentives(is_active);
        CREATE INDEX IF NOT EXISTS idx_incentives_expires ON incentives(expires_at);
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")

def add_community(name: str, builder: str, city: str = None, url: str = None, **kwargs) -> int:
    """Add a new community. Returns ID or -1 if duplicate."""
    conn = get_db()
    try:
        cursor = conn.execute("""
            INSERT INTO communities (name, builder, city, url, zip_code, address, lat, lng, hoa_monthly, amenities, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, builder, city, url,
            kwargs.get('zip_code'),
            kwargs.get('address'),
            kwargs.get('lat'),
            kwargs.get('lng'),
            kwargs.get('hoa_monthly'),
            json.dumps(kwargs.get('amenities', [])),
            kwargs.get('notes')
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return -1
    finally:
        conn.close()

def get_community_by_name(name: str, builder: str = None):
    """Get community by name, optionally filter by builder"""
    conn = get_db()
    if builder:
        cursor = conn.execute(
            "SELECT * FROM communities WHERE name = ? AND builder = ?",
            (name, builder)
        )
    else:
        cursor = conn.execute(
            "SELECT * FROM communities WHERE name = ?",
            (name,)
        )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_property_type(community_id: int, name: str, **kwargs) -> int:
    """Add a property type/floor plan to a community. Returns ID or -1 if duplicate."""
    conn = get_db()
    try:
        cursor = conn.execute("""
            INSERT INTO property_types (
                community_id, name, bedrooms, bathrooms, sqft, stories,
                garage_spaces, has_inlaw_suite, base_price, current_price,
                price_updated_at, url, images, features, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            community_id, name,
            kwargs.get('bedrooms'),
            kwargs.get('bathrooms'),
            kwargs.get('sqft'),
            kwargs.get('stories', 1),
            kwargs.get('garage_spaces', 2),
            kwargs.get('has_inlaw_suite', False),
            kwargs.get('base_price'),
            kwargs.get('current_price') or kwargs.get('base_price'),
            datetime.now().isoformat() if kwargs.get('current_price') else None,
            kwargs.get('url'),
            json.dumps(kwargs.get('images', [])),
            json.dumps(kwargs.get('features', [])),
            kwargs.get('notes')
        ))
        conn.commit()
        
        # Record price history
        if kwargs.get('current_price'):
            conn.execute(
                "INSERT INTO price_history (property_type_id, price) VALUES (?, ?)",
                (cursor.lastrowid, kwargs.get('current_price'))
            )
            conn.commit()
        
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return -1
    finally:
        conn.close()

def update_property_price(property_type_id: int, new_price: float):
    """Update price and record in history"""
    conn = get_db()
    conn.execute("""
        UPDATE property_types 
        SET current_price = ?, price_updated_at = ?, updated_at = ?
        WHERE id = ?
    """, (new_price, datetime.now().isoformat(), datetime.now().isoformat(), property_type_id))
    conn.execute(
        "INSERT INTO price_history (property_type_id, price) VALUES (?, ?)",
        (property_type_id, new_price)
    )
    conn.commit()
    conn.close()

def add_incentive(builder: str, community_id: int = None, **kwargs) -> int:
    """Add a new incentive"""
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO incentives (
            community_id, builder, type, description, rate_buydown,
            rate_after_buydown, closing_credit, other_value, terms,
            lender_required, expires_at, source_url, verified_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        community_id, builder,
        kwargs.get('type', 'rate_buydown'),
        kwargs.get('description'),
        kwargs.get('rate_buydown'),
        kwargs.get('rate_after_buydown'),
        kwargs.get('closing_credit'),
        kwargs.get('other_value'),
        kwargs.get('terms'),
        kwargs.get('lender_required'),
        kwargs.get('expires_at'),
        kwargs.get('source_url'),
        datetime.now().isoformat()
    ))
    conn.commit()
    incentive_id = cursor.lastrowid
    conn.close()
    return incentive_id

def get_active_incentives(builder: str = None, community_id: int = None) -> list:
    """Get active incentives, optionally filtered"""
    conn = get_db()
    query = """
        SELECT i.*, c.name as community_name 
        FROM incentives i
        LEFT JOIN communities c ON i.community_id = c.id
        WHERE i.is_active = 1
    """
    params = []
    
    if builder:
        query += " AND i.builder = ?"
        params.append(builder)
    if community_id:
        query += " AND i.community_id = ?"
        params.append(community_id)
    
    query += " ORDER BY i.expires_at ASC"
    
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_communities(builder: str = None, city: str = None, status: str = 'active') -> list:
    """Get communities with optional filters"""
    conn = get_db()
    query = "SELECT * FROM communities WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    if builder:
        query += " AND builder = ?"
        params.append(builder)
    if city:
        query += " AND city = ?"
        params.append(city)
    
    query += " ORDER BY builder, name"
    
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_property_types(
    community_id: int = None,
    min_beds: int = None,
    max_price: float = None,
    inlaw_only: bool = False
) -> list:
    """Get property types with filters"""
    conn = get_db()
    query = """
        SELECT pt.*, c.name as community_name, c.builder, c.city
        FROM property_types pt
        JOIN communities c ON pt.community_id = c.id
        WHERE 1=1
    """
    params = []
    
    if community_id:
        query += " AND pt.community_id = ?"
        params.append(community_id)
    if min_beds:
        query += " AND pt.bedrooms >= ?"
        params.append(min_beds)
    if max_price:
        query += " AND pt.current_price <= ?"
        params.append(max_price)
    if inlaw_only:
        query += " AND pt.has_inlaw_suite = 1"
    
    query += " ORDER BY pt.current_price ASC"
    
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_listings() -> list:
    """Get all property types with community info for dashboard"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT 
            pt.*,
            c.name as community_name,
            c.builder,
            c.city,
            c.zip_code,
            c.hoa_monthly,
            c.lat,
            c.lng,
            c.url as community_url
        FROM property_types pt
        JOIN communities c ON pt.community_id = c.id
        WHERE c.status = 'active'
        ORDER BY pt.current_price ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats() -> dict:
    """Get database statistics"""
    conn = get_db()
    stats = {}
    
    stats['communities'] = conn.execute("SELECT COUNT(*) FROM communities WHERE status = 'active'").fetchone()[0]
    stats['property_types'] = conn.execute("SELECT COUNT(*) FROM property_types").fetchone()[0]
    stats['active_incentives'] = conn.execute("SELECT COUNT(*) FROM incentives WHERE is_active = 1").fetchone()[0]
    
    # By builder
    cursor = conn.execute("""
        SELECT builder, COUNT(*) as count 
        FROM communities 
        WHERE status = 'active'
        GROUP BY builder 
        ORDER BY count DESC
    """)
    stats['by_builder'] = dict(cursor.fetchall())
    
    # By city
    cursor = conn.execute("""
        SELECT city, COUNT(*) as count 
        FROM communities 
        WHERE status = 'active' AND city IS NOT NULL
        GROUP BY city 
        ORDER BY count DESC
    """)
    stats['by_city'] = dict(cursor.fetchall())
    
    # Price range
    cursor = conn.execute("""
        SELECT MIN(current_price), MAX(current_price), AVG(current_price)
        FROM property_types
        WHERE current_price > 0
    """)
    price_stats = cursor.fetchone()
    if price_stats[0]:
        stats['price_min'] = price_stats[0]
        stats['price_max'] = price_stats[1]
        stats['price_avg'] = price_stats[2]
    
    # 4+ bedroom count
    stats['four_plus_beds'] = conn.execute(
        "SELECT COUNT(*) FROM property_types WHERE bedrooms >= 4"
    ).fetchone()[0]
    
    # In-law suite count
    stats['inlaw_suites'] = conn.execute(
        "SELECT COUNT(*) FROM property_types WHERE has_inlaw_suite = 1"
    ).fetchone()[0]
    
    conn.close()
    return stats

def format_property_telegram(prop: dict, include_incentive: bool = True) -> str:
    """Format a property for Telegram notification"""
    lines = []
    
    # Header
    inlaw = " 🏠👴" if prop.get('has_inlaw_suite') else ""
    lines.append(f"**{prop['name']}**{inlaw}")
    lines.append(f"📍 {prop['community_name']} ({prop['builder']})")
    lines.append(f"🏙️ {prop.get('city', 'Orlando Area')}")
    
    # Price
    if prop.get('current_price'):
        lines.append(f"💰 ${prop['current_price']:,.0f}")
    
    # Details
    details = []
    if prop.get('bedrooms'):
        details.append(f"{int(prop['bedrooms'])}BR")
    if prop.get('bathrooms'):
        details.append(f"{prop['bathrooms']}BA")
    if prop.get('sqft'):
        details.append(f"{int(prop['sqft']):,}sqft")
    if details:
        lines.append(f"🏠 {' | '.join(details)}")
    
    # HOA
    if prop.get('hoa_monthly'):
        lines.append(f"📋 HOA: ${prop['hoa_monthly']:,.0f}/mo")
    
    # URL
    if prop.get('url') or prop.get('community_url'):
        url = prop.get('url') or prop.get('community_url')
        lines.append(f"🔗 [View Details]({url})")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'init':
            init_db()
        elif cmd == 'stats':
            stats = get_stats()
            print(json.dumps(stats, indent=2))
    else:
        print("Usage: python db.py [init|stats]")

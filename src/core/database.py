import sqlite3
from langchain_community.utilities import SQLDatabase
from src.config.config import CONFIG
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def create_sample_database():
    """Create sample SQLite database with airplanes table."""
    db_path = CONFIG["database_path"]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS airplanes')
    
    # Create airplanes table
    cursor.execute('''
    CREATE TABLE airplanes (
        Airplane_id INTEGER PRIMARY KEY,
        Producer TEXT NOT NULL,
        Type TEXT NOT NULL
    )
    ''')
    
    # Insert sample data
    sample_data = [
        (1, 'Boeing', 'Commercial'),
        (2, 'Airbus', 'Commercial'),
        (3, 'Boeing', 'Military'),
        (4, 'Lockheed Martin', 'Military'),
        (5, 'Airbus', 'Commercial'),
        (6, 'Boeing', 'Commercial'),
        (7, 'Cessna', 'Private'),
        (8, 'Gulfstream', 'Private'),
    ]
    
    cursor.executemany(
        'INSERT INTO airplanes VALUES (?, ?, ?)',
        sample_data
    )
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Created sample database at {db_path}")

def initialize_database():
    """Initialize SQLDatabase for LangChain."""
    db = SQLDatabase.from_uri(CONFIG["database_uri"])
    logger.info(f"Connected to database: {CONFIG['database_path']}")
    return db
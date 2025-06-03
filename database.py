import sqlite3
from typing import List, Dict, Optional


class Database:
    """Handles database operations and connections."""
   
    def __init__(self, db_path: str = "community_pulse.db"):
        self.db_path = db_path
        self.init_database()
   
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
   
    def init_database(self):
        """Initialize database with required tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
       
        # Create tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT DEFAULT 'citizen'
            );
           
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
           
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
           
            CREATE TABLE IF NOT EXISTS report_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                image_url TEXT NOT NULL,
                FOREIGN KEY (report_id) REFERENCES reports (id)
            );
           
            CREATE TABLE IF NOT EXISTS report_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                updated_by INTEGER NOT NULL,
                comment TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES reports (id),
                FOREIGN KEY (updated_by) REFERENCES users (id)
            );
        ''')
       
        conn.commit()
        conn.close()
        self.seed_initial_data()
   
    def seed_initial_data(self):
        """Add initial data to the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
       
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
       
        # Add default users
        users_data = [
            ('admin@community.com', 'Admin', 'User', 'admin'),
            ('john.makau@email.com', 'John', 'Makau', 'citizen'),
            ('winnie.siriba@email.com', 'Winnie', 'Siriba', 'moderator'),
        ]
       
        cursor.executemany(
            "INSERT INTO users (email, first_name, last_name, role) VALUES (?, ?, ?, ?)",
            users_data
        )
       
        # Add default categories
        categories_data = [
            ('Infrastructure',),
            ('Safety',),
            ('Environment',),
            ('Community Events',),
            ('Public Services',),
        ]
       
        cursor.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            categories_data
        )
       
        # Add sample reports
        reports_data = [
            (1, 1, 'Pothole on Main Street', 'Large pothole causing traffic issues', 'Main Street & 1st Ave', 'pending'),
            (2, 2, 'Broken Streetlight', 'Streetlight has been out for a week', '5th Street Park', 'in-progress'),
            (1, 3, 'Litter in Community Park', 'Excessive litter near playground area', 'Community Park', 'resolved'),
        ]
       
        cursor.executemany(
            "INSERT INTO reports (user_id, category_id, title, description, location, status) VALUES (?, ?, ?, ?, ?, ?)",
            reports_data
        )
       
        conn.commit()
        conn.close()

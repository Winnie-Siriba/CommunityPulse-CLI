from typing import List, Optional, Tuple
from database import Database
from models import User, Category, Report, ReportUpdate


class UserService:

    def __init__(self, db: Database):
        self.db = db
   
    def get_all_users(self) -> List[User]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
       
        return [User(row['id'], row['email'], row['first_name'], row['last_name'], row['role'])
                for row in rows]
   
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
       
        if row:
            return User(row['id'], row['email'], row['first_name'], row['last_name'], row['role'])
        return None
   
    def create_user(self, email: str, first_name: str, last_name: str, role: str = 'citizen') -> User:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, first_name, last_name, role) VALUES (?, ?, ?, ?)",
            (email, first_name, last_name, role)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
       
        return User(user_id, email, first_name, last_name, role)


class CategoryService:
    """Handles category-related operations."""
   
    def __init__(self, db: Database):
        self.db = db
   
    def get_all_categories(self) -> List[Category]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
       
        return [Category(row['id'], row['name']) for row in rows]
   
    def create_category(self, name: str) -> Category:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
       
        return Category(category_id, name)


class ReportService:
    
   
    def __init__(self, db: Database):
        self.db = db
   
    def get_all_reports(self) -> List[Tuple[Report, str, str]]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.first_name, u.last_name
            FROM reports r
            JOIN categories c ON r.category_id = c.id
            JOIN users u ON r.user_id = u.id
            ORDER BY r.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
       
        results = []
        for row in rows:
            report = Report(row['id'], row['user_id'], row['category_id'],
                          row['title'], row['description'], row['location'],
                          row['status'], row['created_at'])
            results.append((report, row['category_name'], f"{row['first_name']} {row['last_name']}"))
       
        return results
   
    def get_reports_by_user(self, user_id: int) -> List[Tuple[Report, str]]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, c.name as category_name
            FROM reports r
            JOIN categories c ON r.category_id = c.id
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
       
        results = []
        for row in rows:
            report = Report(row['id'], row['user_id'], row['category_id'],
                          row['title'], row['description'], row['location'],
                          row['status'], row['created_at'])
            results.append((report, row['category_name']))
       
        return results
   
    def create_report(self, user_id: int, category_id: int, title: str,
                     description: str, location: str) -> Report:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reports (user_id, category_id, title, description, location, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        ''', (user_id, category_id, title, description, location))
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
       
        return Report(report_id, user_id, category_id, title, description, location, 'pending')
   
    def update_report_status(self, report_id: int, status: str) -> bool:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE reports SET status = ? WHERE id = ?", (status, report_id))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
   
    def search_reports(self, search_term: str) -> List[Tuple[Report, str, str]]:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.first_name, u.last_name
            FROM reports r
            JOIN categories c ON r.category_id = c.id
            JOIN users u ON r.user_id = u.id
            WHERE r.title LIKE ? OR r.description LIKE ? OR r.location LIKE ?
            ORDER BY r.created_at DESC
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        conn.close()
       
        results = []
        for row in rows:
            report = Report(row['id'], row['user_id'], row['category_id'],
                          row['title'], row['description'], row['location'],
                          row['status'], row['created_at'])
            results.append((report, row['category_name'], f"{row['first_name']} {row['last_name']}"))
       
        return results
   
    def add_report_update(self, report_id: int, updated_by: int, comment: str) -> ReportUpdate:
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO report_updates (report_id, updated_by, comment)
            VALUES (?, ?, ?)
        ''', (report_id, updated_by, comment))
        update_id = cursor.lastrowid
        conn.commit()
        conn.close()
       
        return ReportUpdate(update_id, report_id, updated_by, comment)

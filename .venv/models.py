from datetime import datetime
from typing import Optional


class User:
    
   
    def __init__(self, id: int, email: str, first_name: str, last_name: str, role: str = 'citizen'):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
   
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
   
    def is_admin(self) -> bool:
        return self.role == 'admin'
   
    def is_moderator(self) -> bool:
        return self.role in ['admin', 'moderator']


class Category:
    
   
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Report:

   
    def __init__(self, id: int, user_id: int, category_id: int, title: str,
                 description: str, location: str, status: str = 'pending',
                 created_at: str = None):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.description = description
        self.location = location
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()


class ReportUpdate:
    
   
    def __init__(self, id: int, report_id: int, updated_by: int, comment: str, created_at: str = None):
        self.id = id
        self.report_id = report_id
        self.updated_by = updated_by
        self.comment = comment
        self.created_at = created_at or datetime.now().isoformat()
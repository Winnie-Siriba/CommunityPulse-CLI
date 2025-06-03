from typing import Optional
from database import Database
from services import UserService, CategoryService, ReportService
from models import User
from utils import (
    STATUS_OPTIONS, get_status_emoji, get_role_emoji,
    print_separator, print_section_header, validate_input, get_integer_input
)


class CommunityPulseCLI:
    """Main CLI interface for the CommunityPulse application."""
   
    def __init__(self):
        self.db = Database()
        self.user_service = UserService(self.db)
        self.category_service = CategoryService(self.db)
        self.report_service = ReportService(self.db)
        self.current_user: Optional[User] = None
   
    def run(self):
        """Main application loop."""
        print("🏘️  Welcome to CommunityPulse - Community Incident Reporting System")
        print_separator()
       
        while True:
            self.show_main_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
           
            if choice == '1':
                self.handle_user_selection()
            elif choice == '2':
                self.view_all_reports()
            elif choice == '3':
                self.create_new_report()
            elif choice == '4':
                self.search_reports()
            elif choice == '5':
                self.view_my_reports()
            elif choice == '6':
                self.admin_panel()
            elif choice == '7':
                print("Thank you for using CommunityPulse! Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
           
            input("\nPress Enter to continue...")
   
    def show_main_menu(self):
        """Display the main menu."""
        print_section_header("CommunityPulse CLI")
       
        if self.current_user:
            print(f"👤 Logged in as: {self.current_user.full_name} ({self.current_user.role})")
        else:
            print("👤 Not logged in")
       
        print("\n1. Select User")
        print("2. View All Reports")
        print("3. Create New Report")
        print("4. Search Reports")
        print("5. My Reports")
        print("6. Admin Panel" + (" ✅" if self.current_user and self.current_user.is_admin() else ""))
        print("7. Exit")
   
    def handle_user_selection(self):
        """Handle user selection (simplified login)."""
        users = self.user_service.get_all_users()
       
        print("\n📋 Available Users:")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.full_name} ({user.email}) - {user.role}")
       
        choice = get_integer_input(f"\nSelect user (1-{len(users)}): ", 1, len(users))
        self.current_user = users[choice - 1]
        print(f"✅ Selected user: {self.current_user.full_name}")
   
    def view_all_reports(self):
        """Display all reports."""
        reports = self.report_service.get_all_reports()
       
        if not reports:
            print("\n📭 No reports found.")
            return
       
        print(f"\n📋 All Reports ({len(reports)} total):")
        print_separator("-", 100)
       
        for report, category_name, user_name in reports:
            self._display_report_summary(report, category_name, user_name)
            print_separator("-", 100)
   
    def create_new_report(self):
        """Create a new incident report."""
        if not self._ensure_user_logged_in():
            return
       
        print("\n🆕 Create New Report")
        print_separator("-", 30)
       
        # Get available categories
        categories = self.category_service.get_all_categories()
        print("\n📋 Available Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.name}")
       
        category_choice = get_integer_input(f"\nSelect category (1-{len(categories)}): ", 1, len(categories))
        selected_category = categories[category_choice - 1]
       
        # Get report details
        title = input("📝 Report Title: ").strip()
        if not validate_input(title, "Title"):
            return
       
        description = input("📄 Description: ").strip()
        if not validate_input(description, "Description"):
            return
       
        location = input("📍 Location: ").strip()
        if not validate_input(location, "Location"):
            return
       
        # Create the report
        try:
            report = self.report_service.create_report(
                self.current_user.id, selected_category.id, title, description, location
            )
            print(f"✅ Report created successfully! Report ID: {report.id}")
        except Exception as e:
            print(f"❌ Error creating report: {e}")
   
    def search_reports(self):
        """Search for reports."""
        search_term = input("\n🔍 Enter search term (title, description, or location): ").strip()
       
        if not validate_input(search_term, "Search term"):
            return
       
        reports = self.report_service.search_reports(search_term)
       
        if not reports:
            print("📭 No reports found matching your search.")
            return
       
        print(f"\n🔍 Search Results ({len(reports)} found):")
        print_separator("-", 100)
       
        for report, category_name, user_name in reports:
            self._display_report_summary(report, category_name, user_name)
            print_separator("-", 100)
   
    def view_my_reports(self):
        """View reports created by the current user."""
        if not self._ensure_user_logged_in():
            return
       
        reports = self.report_service.get_reports_by_user(self.current_user.id)
       
        if not reports:
            print("\n📭 You haven't created any reports yet.")
            return
       
        print(f"\n👤 Your Reports ({len(reports)} total):")
        print_separator("-", 80)
       
        for report, category_name in reports:
            self._display_user_report(report, category_name)
            print_separator("-", 80)
   
    def admin_panel(self):
        """Admin panel for managing reports and categories."""
        if not self._ensure_admin_access():
            return
       
        while True:
            print("\n🔧 Admin Panel")
            print_separator("-", 20)
            print("1. Update Report Status")
            print("2. Add Report Comment")
            print("3. Create New Category")
            print("4. View All Users")
            print("5. Back to Main Menu")
           
            choice = input("\nEnter your choice (1-5): ").strip()
           
            if choice == '1':
                self.update_report_status()
            elif choice == '2':
                self.add_report_comment()
            elif choice == '3':
                self.create_category()
            elif choice == '4':
                self.view_all_users()
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
   
    def update_report_status(self):
        """Update the status of a report."""
        report_id = get_integer_input("🆔 Enter Report ID: ")
       
        print("\n📊 Available Statuses:")
        for i, status in enumerate(STATUS_OPTIONS, 1):
            print(f"{i}. {status}")
       
        status_choice = get_integer_input(f"\nSelect new status (1-{len(STATUS_OPTIONS)}): ", 1, len(STATUS_OPTIONS))
        new_status = STATUS_OPTIONS[status_choice - 1]
       
        if self.report_service.update_report_status(report_id, new_status):
            print(f"✅ Report {report_id} status updated to '{new_status}'")
        else:
            print("❌ Report not found or update failed.")
   
    def add_report_comment(self):
        """Add a comment to a report."""
        report_id = get_integer_input("🆔 Enter Report ID: ")
        comment = input("💬 Enter comment: ").strip()
       
        if not validate_input(comment, "Comment"):
            return
       
        try:
            self.report_service.add_report_update(report_id, self.current_user.id, comment)
            print("✅ Comment added successfully!")
        except Exception as e:
            print(f"❌ Error adding comment: {e}")
   
    def create_category(self):
        """Create a new category."""
        category_name = input("🏷️  Enter new category name: ").strip()
       
        if not validate_input(category_name, "Category name"):
            return
       
        try:
            category = self.category_service.create_category(category_name)
            print(f"✅ Category '{category.name}' created successfully!")
        except Exception as e:
            print(f"❌ Error creating category: {e}")
   
    def view_all_users(self):
        """View all users in the system."""
        users = self.user_service.get_all_users()
       
        print(f"\n👥 All Users ({len(users)} total):")
        print_separator("-", 60)
       
        for user in users:
            role_emoji = get_role_emoji(user.role)
            print(f"{role_emoji} {user.full_name}")
            print(f"   📧 {user.email}")
            print(f"   🏷️  Role: {user.role}")
            print_separator("-", 60)
   
    def _display_report_summary(self, report, category_name: str, user_name: str):
        """Display a summary of a report."""
        status_emoji = get_status_emoji(report.status)
        print(f"🆔 ID: {report.id} | {status_emoji} {report.status.upper()}")
        print(f"📝 Title: {report.title}")
        print(f"🏷️  Category: {category_name}")
        print(f"👤 Reporter: {user_name}")
        print(f"📍 Location: {report.location}")
        print(f"📅 Created: {report.created_at}")
        print(f"📄 Description: {report.description}")
   
    def _display_user_report(self, report, category_name: str):
        """Display a user's own report summary."""
        status_emoji = get_status_emoji(report.status)
        print(f"🆔 ID: {report.id} | {status_emoji} {report.status.upper()}")
        print(f"📝 Title: {report.title}")
        print(f"🏷️  Category: {category_name}")
        print(f"📍 Location: {report.location}")
        print(f"📅 Created: {report.created_at}")
   
    def _ensure_user_logged_in(self) -> bool:
        """Ensure a user is logged in."""
        if not self.current_user:
            print("❌ Please select a user first.")
            return False
        return True
   
    def _ensure_admin_access(self) -> bool:
        """Ensure the current user has admin access."""
        if not self.current_user or not self.current_user.is_admin():
            print("❌ Access denied. Admin privileges required.")
            return False
        return True

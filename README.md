# CommunityPulse CLI 🏘️

A Python CLI application for community incident reporting and management.

## Author
**Winnie Moraa Siriba**

## Overview

CommunityPulse is a command-line interface application that enables citizens to report community issues (infrastructure problems, safety concerns, environmental issues) and allows administrators to manage and track these reports efficiently.

## Features

- 📝 **Report Creation**: Submit incident reports with categorization
- 🔍 **Search Functionality**: Find reports by keywords
- 📊 **Status Tracking**: Monitor report progress (pending → in-progress → resolved → closed)
- 👥 **User Role Management**: Citizens, moderators, and administrators with different permissions
- 💬 **Comment System**: Add updates and comments to reports
- 🏷️ **Category Management**: Organize reports by type (Infrastructure, Safety, Environment, etc.)
- 📋 **Report Management**: View all reports or filter by user

## Technology Stack

- **Language**: Python 3.x
- **Database**: SQLite3
- **Architecture**: Modular OOP design
- **CLI Interface**: Interactive command-line menus

## Project Structure

```
community-pulse/
├── main.py           # Application entry point
├── cli.py            # CLI interface and user interactions
├── database.py       # Database connection and schema management
├── models.py         # Data model classes (User, Report, Category)
├── services.py       # Business logic and CRUD operations
├── utils.py          # Helper functions and utilities
└── community_pulse.db # SQLite database (created automatically)
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses built-in libraries)

### Installation
1. Clone or download the project files
2. Navigate to the project directory
3. Run the application:

```bash
python main.py
```

The application will automatically create the SQLite database and populate it with sample data on first run.

## Usage

### Getting Started
1. **Launch the application**:
   ```bash
   python main.py
   ```

2. **Select a user** (simplified login):
   - Admin User (admin@community.com) - Full access
   - John Doe (john.doe@email.com) - Citizen
   - Jane Smith (jane.smith@email.com) - Moderator

3. **Navigate the menu**:
   - View all reports
   - Create new reports
   - Search existing reports
   - Access admin panel (admin only)

### Sample Workflow
1. Select a user to login
2. Choose "Create New Report"
3. Select a category (Infrastructure, Safety, etc.)
4. Fill in report details (title, description, location)
5. View your submitted report in "My Reports"
6. Admins can update report status and add comments

## Database Schema

The application uses 5 related tables:
- **users**: User accounts and roles
- **categories**: Report categories
- **reports**: Main incident reports
- **report_images**: Image attachments (structure ready)
- **report_updates**: Comments and status updates

## Key Features Demonstrated

### Technical Features
- **Modular Architecture**: Separation of concerns across multiple modules
- **Database Relationships**: Foreign keys and JOIN operations
- **Full CRUD Operations**: Create, Read, Update, Delete for all entities
- **Input Validation**: Robust error handling and data validation
- **Type Hints**: Professional code documentation

### User Experience
- **Intuitive Navigation**: Clear menu systems with numbered options
- **Visual Indicators**: Emoji icons for status and roles
- **Error Handling**: Graceful error messages and recovery
- **Role-based Access**: Different features for different user types

## Default Users & Categories

### Pre-loaded Users:
- **Admin**: admin@community.com (Full system access)
- **Citizen**: john.doe@email.com (Create and view reports)
- **Moderator**: jane.smith@email.com (Moderate reports)

### Default Categories:
- Infrastructure
- Safety
- Environment
- Community Events
- Public Services

## Admin Features

Administrators have access to additional functionality:
- Update report status
- Add comments to any report
- Create new categories
- View all system users
- Full report management

## Contributing

This project was created as part of a Phase 3 CLI project. Future enhancements could include:
- Image upload functionality
- Email notifications
- Report analytics and statistics
- Export functionality
- Web interface integration

## License

This project is created for educational purposes.

---

*Built with ❤️ for community engagement and civic participation*

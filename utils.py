from typing import Dict


# Status options for reports
STATUS_OPTIONS = ['pending', 'in-progress', 'resolved', 'closed']


def get_status_emoji(status: str) -> str:
    """Get emoji for report status."""
    emoji_map = {
        'pending': '⏳',
        'in-progress': '🔄',
        'resolved': '✅',
        'closed': '🔒'
    }
    return emoji_map.get(status, '❓')


def get_role_emoji(role: str) -> str:
    """Get emoji for user role."""
    emoji_map = {
        'admin': '👑',
        'moderator': '🛡️', 
        'citizen': '👤'
    }
    return emoji_map.get(role, '👤')


def print_separator(char: str = "=", length: int = 60):
    """Print a separator line."""
    print(char * length)


def print_section_header(title: str, char: str = "=", length: int = 60):
    """Print a formatted section header."""
    print("\n" + char * length)
    print(f"=== {title} ===")
    print(char * length)


def validate_input(value: str, field_name: str) -> bool:
    """Validate that input is not empty."""
    if not value.strip():
        print(f"❌ {field_name} cannot be empty.")
        return False
    return True


def get_integer_input(prompt: str, min_val: int = 1, max_val: int = None) -> int:
    """Get and validate integer input from user."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"❌ Please enter a number >= {min_val}")
                continue
            if max_val and value > max_val:
                print(f"❌ Please enter a number <= {max_val}")
                continue
            return value
        except ValueError:
            print("❌ Please enter a valid number.")

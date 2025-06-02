from cli import CommunityPulseCLI


def main():
    """Main function to run the application."""
    try:
        app = CommunityPulseCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Please restart the application.")


if __name__ == "__main__":
    main()
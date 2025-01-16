from typing_automation.automation import TypingAutomation

def main():
    try:
        app = TypingAutomation()
        app.main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()

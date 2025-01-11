import time
import random
import pyautogui
import os
from datetime import datetime
from typing import Optional

from typing_automation.settings import Settings
from typing_automation.utils import save_typing_stats, validate_word_count

class TypingAutomation:
    def __init__(self):
        self.settings = Settings()
        self.typing_stats = {
            'start_time': None,
            'end_time': None,
            'words_typed': 0,
            'characters_typed': 0
        }

    def configure_settings(self) -> None:
        print("\nCurrent Settings:")
        current_settings = self.settings.settings
        new_settings = {}
        
        for key, value in current_settings.items():
            print(f"{key}: {value}")
            new_value = input(f"Enter new value for {key} (press Enter to keep current): ")
            if new_value.strip():
                try:
                    new_settings[key] = float(new_value)
                except ValueError:
                    print(f"Invalid input. Keeping current value: {value}")
        
        if new_settings:
            self.settings.update(new_settings)

    def get_words_to_type(self, word_count: int) -> int:
        while True:
            user_input = input(
                "Enter the number of words to type, 'all' for entire content, "
                "or 'random' for random selection: "
            )
            if user_input.lower() == 'random':
                return random.randint(1, word_count)
            try:
                return validate_word_count(user_input, word_count)
            except ValueError as e:
                print(str(e))

    def type_text(self, words: list, num_words: int) -> None:
        i = 0
        self.typing_stats['start_time'] = datetime.now()

        while i < num_words:
            chunk_size = random.randint(
                self.settings.get('min_chunk_size'),
                self.settings.get('max_chunk_size')
            )
            
            next_pause = random.randint(
                self.settings.get('min_pause'),
                self.settings.get('max_pause')
            )
            
            for _ in range(chunk_size):
                if i >= num_words:
                    break
                
                word = words[i]
                pyautogui.typewrite(word)
                pyautogui.press('space')
                
                self.typing_stats['words_typed'] += 1
                self.typing_stats['characters_typed'] += len(word)
                
                typing_speed = random.uniform(
                    self.settings.get('min_typing_speed'),
                    self.settings.get('max_typing_speed')
                )
                time.sleep(typing_speed)
                
                i += 1
            
            print(f"\nProgress: {i}/{num_words} words ({(i/num_words)*100:.1f}%)")
            print(f"Pausing for {next_pause} seconds...\n")
            time.sleep(next_pause)

        self.typing_stats['end_time'] = datetime.now()
        stats_file = save_typing_stats(self.typing_stats)
        print("\nTyping completed!")
        print(f"Statistics have been saved to {stats_file}")

    def main(self) -> None:
        while True:
            print("\n1. Start Typing")
            print("2. Configure Settings")
            print("3. Exit")
            
            choice = input("\nSelect an option (1-3): ")
            
            if choice == '2':
                self.configure_settings()
            elif choice == '3':
                break
            elif choice == '1':
                self._run_typing_session()
            else:
                print("Invalid choice")

    def _run_typing_session(self) -> None:
        file_name = input("Enter the name of the text file (with extension): ")
        
        try:
            start_delay = int(input("Enter delay (in seconds) before starting to type: "))
        except ValueError:
            print("Please enter a valid integer for delay.")
            return

        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, file_name)
            with open(file_path, 'r') as file:
                text_content = file.read()
        except FileNotFoundError:
            print(f"File '{file_name}' not found in the project root directory.")
            return
        try:
            words = text_content.split()
            word_count = len(words)
            num_words_to_type = self.get_words_to_type(word_count)
        except Exception as e:
            print(f"Error: {e}")

        print(f"Waiting for {start_delay} seconds before starting...")
        time.sleep(start_delay)
        print("\nTyping starts now...\n")
        
       
        
        self.type_text(words, num_words_to_type)

def main():
    automation = TypingAutomation()
    automation.main()

if __name__ == "__main__":
    main()

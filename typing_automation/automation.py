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
            'characters_typed': 0,
            'errors_made': 0,
            'corrections_made': 0
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

    def simulate_typo(self, char: str) -> str:
        keyboard_layout = {
            'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'srfce', 'e': 'wrsdf',
            'f': 'drtgv', 'g': 'ftyhb', 'h': 'gyujn', 'i': 'ujko', 'j': 'huikm',
            'k': 'jiol', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
            'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awdxz', 't': 'rfgy',
            'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
            'z': 'asx'
        }
        char = char.lower()
        if char in keyboard_layout:
            return random.choice(keyboard_layout[char])
        return char

    def type_with_errors(self, word: str) -> None:
        error_rate = self.settings.get('error_rate')
        max_error_chars = self.settings.get('max_error_chars')
        correction_delay = self.settings.get('correction_delay')
        
        i = 0
        while i < len(word):
            if random.random() < error_rate:
                error_chars = []
                num_errors = random.randint(1, int(max_error_chars))
                for _ in range(num_errors):
                    wrong_char = self.simulate_typo(word[i])
                    error_chars.append(wrong_char)
                    pyautogui.typewrite(wrong_char)
                    time.sleep(random.uniform(0.1, 0.2))
                
                time.sleep(correction_delay)
                
                for _ in range(len(error_chars)):
                    pyautogui.press('backspace')
                    time.sleep(0.1)
                
                pyautogui.typewrite(word[i])
                
                self.typing_stats['errors_made'] += 1
                self.typing_stats['corrections_made'] += 1
            else:
                pyautogui.typewrite(word[i])
            
            i += 1
            time.sleep(random.uniform(
                self.settings.get('min_typing_speed'),
                self.settings.get('max_typing_speed')
            ))

    def type_text(self, words: list, num_words: int) -> None:
        i = 0
        self.typing_stats['start_time'] = datetime.now()

        while i < num_words:
            chunk_size = random.randint(
                int(self.settings.get('min_chunk_size')),
                int(self.settings.get('max_chunk_size'))
            )
            
            next_pause = random.randint(
                int(self.settings.get('min_pause')),
                int(self.settings.get('max_pause'))
            )
            
            for _ in range(chunk_size):
                if i >= num_words:
                    break
                
                word = words[i]
                self.type_with_errors(word)
                pyautogui.press('space')
                
                self.typing_stats['words_typed'] += 1
                self.typing_stats['characters_typed'] += len(word)
                
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

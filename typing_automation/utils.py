from datetime import datetime
from typing import Dict, Any

def save_typing_stats(stats: Dict[str, Any]) -> str:
    stats_file = f"typing_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    duration = (stats['end_time'] - stats['start_time']).total_seconds()
    wpm = (stats['words_typed'] / duration) * 60
    cpm = (stats['characters_typed'] / duration) * 60
    
    with open(stats_file, 'w') as f:
        f.write("Typing Session Statistics\n")
        f.write("=======================\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {duration:.2f} seconds\n")
        f.write(f"Words Typed: {stats['words_typed']}\n")
        f.write(f"Characters Typed: {stats['characters_typed']}\n")
        f.write(f"Words Per Minute: {wpm:.2f}\n")
        f.write(f"Characters Per Minute: {cpm:.2f}\n")
    
    return stats_file

def validate_word_count(user_input: str, max_words: int) -> int:
    if user_input.lower() == 'all':
        return max_words
    try:
        num_words = int(user_input)
        if 0 < num_words <= max_words:
            return num_words
        raise ValueError
    except ValueError:
        raise ValueError(f"Please enter a number between 1 and {max_words}.")
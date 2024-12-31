import unittest
from unittest.mock import patch, mock_open
from typing_automation.automation import TypingAutomation
from typing_automation.settings import Settings
from typing_automation.utils import validate_word_count

class TestTypingAutomation(unittest.TestCase):
    def setUp(self):
        self.automation = TypingAutomation()

    def test_validate_word_count(self):
        self.assertEqual(validate_word_count('all', 100), 100)
        
        self.assertEqual(validate_word_count('50', 100), 50)
        
        with self.assertRaises(ValueError):
            validate_word_count('0', 100)
        
        with self.assertRaises(ValueError):
            validate_word_count('101', 100)

class TestSettings(unittest.TestCase):
    @patch('builtins.open', mock_open(read_data='{"min_typing_speed": 0.2}'))
    def test_load_settings(self):
        settings = Settings()
        self.assertEqual(settings.get('min_typing_speed'), 0.2)

if __name__ == '__main__':
    unittest.main()

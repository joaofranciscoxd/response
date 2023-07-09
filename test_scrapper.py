import os
os.system('cls')
import unittest
from unittest.mock import patch, MagicMock
from scrapper.scrapper_bot import scrape_wikipedia, configure_logger
from scrapper.database import Fact
import datetime

class ScraperBotTests(unittest.TestCase):
    @patch('scrapper.scrapper_bot.send_get_request')
    @patch('scrapper.scrapper_bot.parse_wikipedia_page')
    @patch('scrapper.scrapper_bot.extract_facts')
    @patch('scrapper.scrapper_bot.exclude_archived_facts')
    def test_scrape_wikipedia(self, mock_exclude_archived_facts, mock_extract_facts, mock_parse_wikipedia_page, mock_send_get_request):
        # Mock the necessary dependencies and data
        mock_send_get_request.return_value = MagicMock()
        mock_parse_wikipedia_page.return_value = MagicMock()
        mock_extract_facts.return_value = [{'content': 'Test Fact 1', 'preview_links': []}, {'content': 'Test Fact 2', 'preview_links': []}]
        mock_exclude_archived_facts.return_value = [{'content': 'Test Fact 1'}, {'content': 'Test Fact 2'}]

        # Mock the store_facts_in_database function to prevent side effects
        with patch('scrapper.scrapper_bot.store_facts_in_database'):
            # Run the function to be tested
            scrape_wikipedia()

        # Assert the expected behavior
        # Add your assertions here

    def test_configure_logger(self):
        # Run the function to be tested
        configure_logger()

        # Assert the expected behavior
        # Add your assertions here

class DatabaseTests(unittest.TestCase):
    def test_fact_model(self):
        # Create a Fact instance
        fact = Fact(content='Test Fact', created_at=datetime.datetime.now())

        # Assert the attributes of the Fact instance
        self.assertEqual(fact.content, 'Test Fact')
        self.assertIsNotNone(fact.created_at)

        # Add more tests for Fact model if needed

if __name__ == '__main__':
    unittest.main()

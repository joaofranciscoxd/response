import os
os.system('cls')
import unittest
from unittest.mock import patch
from analyzer.fetcher import extract_keywords, find_related_articles, extract_metadata, check_temporal_relevance, get_date, get_fact_length
import datetime

class MockFact:
    def __init__(self, content):
        self.content = content

class FetcherTests(unittest.TestCase):

    def test_extract_keywords(self):
        # Test case for extract_keywords function
        fact = MockFact(content='This is a test sentence.')
        expected_keywords = ['sentence', 'test']

        keywords = extract_keywords(fact.content)
        self.assertEqual(sorted(keywords), sorted(expected_keywords))

    def test_find_related_articles(self):
        # Test case for find_related_articles function
        keyword = 'test'
        expected_internal_links = ['https://en.wikipedia.org/wiki/Test_Page']

        with patch('analyzer.fetcher.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'query': {
                    'search': [
                        {'title': 'Test Page'}
                    ]
                }
            }

            internal_links = find_related_articles(keyword)
            self.assertEqual(internal_links, expected_internal_links)

    def test_extract_metadata(self):
        # Test case for extract_metadata function
        fact = MockFact(content='This is a test sentence mentioning 2022-01.')
        expected_metadata = {
            'temporal_relevance': True,
            'date': datetime.datetime(2022, 1, 1).date(),
            'fact_length': 7
        }

        metadata = extract_metadata(fact)
        self.assertEqual(metadata, expected_metadata)

    
            
    def test_check_temporal_relevance(self):
        # Test case for check_temporal_relevance function
        fact = MockFact(content='This is a test sentence mentioning 2022.')
        temporal_relevance = check_temporal_relevance(fact)
        self.assertIsInstance(temporal_relevance, bool)


    def test_get_date(self):
        # Test case for get_date function
        fact = MockFact(content='This is a test sentence mentioning a date: 2022-07-01.')
        expected_date = datetime.datetime(2022, 7, 1).date()

        date = get_date(fact)
        self.assertEqual(date, expected_date)

    def test_get_fact_length(self):
        # Test case for get_fact_length function
        fact = MockFact(content='This is a test sentence.')
        expected_length = 5

        length = get_fact_length(fact)
        self.assertEqual(length, expected_length)


if __name__ == '__main__':
    unittest.main()

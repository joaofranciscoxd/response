# %%
import unittest
from unittest.mock import patch
from main import scrape_wikipedia

class TestWebScraper(unittest.TestCase):
    
    def test_scrape_wikipedia(self):
        # Prepare mock response
        mock_response = MockResponse()
        mock_response.status_code = 200
        mock_response.content = """
            <html>
                <body>
                    <div id="mp-dyk">
                        <li>Fact 1</li>
                        <li>Fact 2</li>
                    </div>
                </body>
            </html>
        """
        
        with patch('main.requests.get') as mock_get:
            mock_get.return_value = mock_response

            # Call the function to be tested
            scrape_wikipedia()

            # TODO: Add assertions to validate the functionality of your code
            # For example, you can assert that the data is stored correctly in the database,
            # or check if the expected number of facts were retrieved and processed.

class MockResponse:
    def __init__(self):
        self.status_code = None
        self.content = None

unittest.main()




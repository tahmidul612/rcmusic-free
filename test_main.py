import unittest
from unittest.mock import patch, MagicMock
from main import main

class TestMain(unittest.TestCase):

    @patch('main.requests.get')
    @patch('main.create_ics')
    def test_main_with_extra_table(self, mock_create_ics, mock_requests_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
                <table>
                    <tr><td>Some other table</td></tr>
                </table>
                <div class="rcm-responsive-table">
                    <table>
                        <tr>
                            <th>Date & Time</th>
                            <th>Location</th>
                            <th>Artist & Discipline</th>
                        </tr>
                        <tr>
                            <td>Friday, September 5 1:00pm</td>
                            <td>Mazzoleni Hall</td>
                            <td>Eric Guo, piano</td>
                        </tr>
                    </table>
                </div>
            </body>
        </html>
        """
        mock_requests_get.return_value = mock_response

        # Call the main function
        result = main()

        # Assert that the script runs successfully
        self.assertTrue(result)

        # Assert that create_ics was called
        mock_create_ics.assert_called_once()

        # Get the actual call arguments
        actual_args, _ = mock_create_ics.call_args

        # Extract the json from the arguments
        table_json = actual_args[0]

        # Assert that the parsed data is correct
        expected_json = {
            'Date & Time': 'Friday, September 5 1:00pm',
            'Location': 'Mazzoleni Hall',
            'Artist & Discipline': 'Eric Guo, piano'
        }

        # The html_to_json library returns a list of dictionaries, with one dictionary per row
        # The mock HTML has one data row, so we expect a list with one item
        self.assertEqual(len(table_json), 1)
        self.assertEqual(table_json[0], expected_json)

    @patch('main.requests.get')
    @patch('main.create_ics')
    def test_main_fallback_to_direct_tables(self, mock_create_ics, mock_requests_get):
        # Mock the response with no rcm-responsive-table divs, only direct tables
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
                <table>
                    <tr>
                        <th>Date & Time</th>
                        <th>Location</th>
                        <th>Artist & Discipline</th>
                    </tr>
                    <tr>
                        <td>Monday, December 9 3:00pm</td>
                        <td>Concert Hall</td>
                        <td>Jane Smith, violin</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        mock_requests_get.return_value = mock_response

        # Call the main function
        result = main()

        # Assert that the script runs successfully
        self.assertTrue(result)

        # Assert that create_ics was called
        mock_create_ics.assert_called_once()

        # Get the actual call arguments
        actual_args, _ = mock_create_ics.call_args
        table_json = actual_args[0]

        # Assert that the parsed data is correct
        expected_json = {
            'Date & Time': 'Monday, December 9 3:00pm',
            'Location': 'Concert Hall',
            'Artist & Discipline': 'Jane Smith, violin'
        }

        self.assertEqual(len(table_json), 1)
        self.assertEqual(table_json[0], expected_json)

if __name__ == '__main__':
    unittest.main()
from unittest.mock import patch
from accountparser.main import create_output_row


class Test_create_output_row:
    good_row = {
        'Account Name': 'lexcorp',
        'Account ID': '12345',
        'Created On': '1/12/11',
        'First Name': 'Lex'
    }

    bad_id_row = {
        'Account Name': 'lexcorp',
        'Account ID': '',
        'Created On': '1/12/11',
        'First Name': 'Lex'
    }

    no_id_row = {
        'Account Name': 'lexcorp',
        'First Name': 'Lex'
    }

    no_first_name = {
        'Account Name': 'lexcorp',
        'Account ID': '12345',
        'Created On': '1/12/11',
    }

    bad_created_on_date = {
        'Account Name': 'lexcorp',
        'Account ID': '12345',
        'Created On': '00',
        'First Name': 'Lex'
    }

    good_status = {
            "account_id": "12345",
            "status": "good",
            "created_on": "2011-01-12"
        }

    no_status = {
            "account_id": "12345",
            "created_on": "2011-01-12"
        }

    no_status_date = {
            "account_id": "12345",
            "status": "good",
        }

    @patch('accountparser.main.get_account_status')
    def test_good_row(self, mock_status):
        mock_status.return_value = self.good_status

        expected = {
            "Account ID": "12345",
            "First Name": "Lex",
            "Created On": "2011-01-12",
            "Status": "good",
            "Status Set On": "2011-01-12"
        }
        row = create_output_row(None, self.good_row)
        assert(row == expected)

    def test_bad_account_id(self):
        row = create_output_row(None, self.bad_id_row)
        assert(row is None)

    def test_no_account_id(self):
        row = create_output_row(None, self.no_id_row)
        assert(row is None)

    @patch('accountparser.main.get_account_status')
    def test_no_first_name(self, mock_status):
        mock_status.return_value = self.good_status

        expected = {
            "Account ID": "12345",
            "First Name": None,
            "Created On": "2011-01-12",
            "Status": "good",
            "Status Set On": "2011-01-12"
        }

        row = create_output_row(None, self.no_first_name)
        assert(row == expected)

    @patch('accountparser.main.get_account_status')
    def test_bad_created_on_date(self, mock_status):
        mock_status.return_value = self.good_status

        expected = {
            "Account ID": "12345",
            "First Name": "Lex",
            "Created On": None,
            "Status": "good",
            "Status Set On": "2011-01-12"
        }

        row = create_output_row(None, self.bad_created_on_date)
        assert(row == expected)

    @patch('accountparser.main.get_account_status')
    def test_no_status(self, mock_status):
        mock_status.return_value = self.no_status

        expected = {
            "Account ID": "12345",
            "First Name": "Lex",
            "Created On": "2011-01-12",
            "Status": None,
            "Status Set On": "2011-01-12"
        }

        row = create_output_row(None, self.good_row)
        assert(row == expected)

    @patch('accountparser.main.get_account_status')
    def test_no_status_date(self, mock_status):
        mock_status.return_value = self.no_status_date

        expected = {
            "Account ID": "12345",
            "First Name": "Lex",
            "Created On": "2011-01-12",
            "Status": "good",
            "Status Set On": None
        }

        row = create_output_row(None, self.good_row)
        assert(row == expected)

from unittest.mock import patch

#  call_command() will allow us to call the command in our source code
from django.core.management import call_command

# import operatinalError that django throws when db is not available
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):
    def test_wait_for_db_ready(self):
        """ Test waiting for db when db is available """

        # check if it return OperationalError
        # if error then db not available
        # else db is available

        # for changing behavior of __getitem__
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")  # calling management command
            self.assertEqual(gi.call_count, 1)  # making assertions

    # this will replace time.sleep
    # with mock function that returns True
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """ TEst waiting for db """
        # this is going to be while loop
        # it's gonna check if ConnectionHandler raise the OperationalError
        # if it does raise the OperationalError then it's going to wait
        # a sec and try again
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 6)

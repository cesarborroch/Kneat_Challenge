import unittest
from SW_stops_amount import SW_stops_amount

class TestStringMethods(unittest.TestCase):

    def test_amount_of_stops(self):
        # Creates a mock ship with previous well known values
        ship = {'name':'mock ship', 'consumables':'1 week', 'MGLT':'80'}
        App = SW_stops_amount()
        intStops = App.get_amount(1000000, ship['consumables'], ship['MGLT'])
        # We expect "74 stops" for "1000000 MGLT"
        # Change this value "74" to force a failure or break the main application
        self.assertEqual(intStops, 74)

if __name__ == '__main__':
    unittest.main()

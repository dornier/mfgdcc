import unittest
from mfgdcc import app


class MfgdccTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_bad_url(self):
        response = self.app.get('/chart', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_tabular(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_tabular_filter(self):
        response = self.app.post(
            '/',
            data=dict(
                coin='Ethereum',
                status='Enabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_mkt_cap_charting_single_coin(self):
        response = self.app.post(
            '/charts/marketcap',
            data=dict(
                coins=['IOTA'],
                status='Enabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_mkt_cap_charting_multiple_coins(self):
        response = self.app.post(
            '/charts/marketcap',
            data=dict(
                coins=['Dash', 'EOS'],
                status='Disabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_price_charting_single_coin(self):
        response = self.app.post(
            '/charts/price',
            data=dict(
                coins=['TRON'],
                status='Enabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_price_charting_multiple_coins(self):
        response = self.app.post(
            '/charts/price',
            data=dict(
                coins=['Bitcoin', 'Tether'],
                status='Disabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_supply_charting_single_coin(self):
        response = self.app.post(
            '/charts/supply',
            data=dict(
                coins=['Cardano'],
                status='Enabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_supply_charting_multiple_coins(self):
        response = self.app.post(
            '/charts/supply',
            data=dict(
                coins=['Monero', 'Ethereum Classic'],
                status='Disabled'
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

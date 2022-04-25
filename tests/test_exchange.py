from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
import server


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return server.create_app()

    async def test_wrong_authentication(self):
        headers = {'Authentication': 'wrong_token'}

        async with self.client.request("GET", "/exchange?from=2020-10-01&to=2020-10-03", headers=headers) as resp:
            self.assertEqual(401, resp.status)
            text = await resp.text()
        self.assertIn("Unauthorized", text)

    async def test_bad_params(self):
        headers = {'Authentication': 'correct_token'}

        cases = [
            # Check availabilty of parameters.
            {'to': '2020-10-01'},
            {'from': '2020-10-01'},
            # Check correctness of parameters.
            {'from': '2020-10-01', 'to': '2020-10-001'},
            {'from': '2020-10-001', 'to': '2020-10-01'},
        ]
        for params in cases:
            async with self.client.request("GET", "/exchange", params=params, headers=headers) as resp:
                self.assertEqual(400, resp.status)


    async def test_bank_link_availability(self):
        headers = {'Authentication': 'wrong_token'}
        EXCHANGE_API_URL = "http://127.0.0.1"
        async with self.client.request("GET", "/exchange?from=2020-10-01&to=2020-10-03", headers=headers) as resp:
            self.assertEqual(401, resp.status)
            text = await resp.text()
        self.assertIn("Unauthorized", text)

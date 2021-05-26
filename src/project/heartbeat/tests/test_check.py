import unittest

from project._tests.base import BaseTestCase


class TestServiceHealth(BaseTestCase):
    """Tests for service check"""

    def test_heartbeat(self):
        """Ensure heartbeat route behaves correctly."""

        with self.client:
            response = self.client.get('/heartbeat')
            data = response.json
            self.assert200(response)
            self.assertIn('status', data)


if __name__ == '__main__':
    unittest.main()

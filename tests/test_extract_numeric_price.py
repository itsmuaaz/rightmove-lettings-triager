import unittest
from utils import extract_numeric_price

class TestNumericPriceExtraction(unittest.TestCase):
    def test_extract_valid_pcm(self):
        self.assertEqual(extract_numeric_price("£2,000 pcm"), 2000)
        self.assertEqual(extract_numeric_price("£1,550 pcm"), 1550)
        self.assertEqual(extract_numeric_price("£950 pcm"), 950)

    def test_extract_valid_pw(self):
        self.assertEqual(extract_numeric_price("£450 pw"), 450)
        self.assertEqual(extract_numeric_price("£1,200 pw"), 1200)

    def test_extract_no_currency(self):
        self.assertEqual(extract_numeric_price("2000 pcm"), 2000)
        self.assertEqual(extract_numeric_price("2,000"), 2000)
        self.assertEqual(extract_numeric_price("2000"), 2000)

    def test_extract_poa_or_invalid(self):
        self.assertIsNone(extract_numeric_price("POA"))
        self.assertIsNone(extract_numeric_price("Contact Agent"))
        self.assertIsNone(extract_numeric_price(""))
        self.assertIsNone(extract_numeric_price(None))

if __name__ == '__main__':
    unittest.main()

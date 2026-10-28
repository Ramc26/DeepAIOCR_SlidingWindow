import unittest
from unittest.mock import patch

from classifier import BuildUserPayload, ParseLabel, ClassifyDocument


class ClassifierTests(unittest.TestCase):
    def test_valid_label(self):
        self.assertEqual(ParseLabel('{"label": "Invoice"}'), "Invoice")

    def test_rejects_invalid_label(self):
        with self.assertRaises(ValueError):
            ParseLabel('{"label": "Tax Form"}')

    def test_rejects_extra_response_fields(self):
        with self.assertRaises(ValueError):
            ParseLabel('{"label": "Invoice", "reason": "looks like one"}')

    def test_rejects_malformed_json(self):
        with self.assertRaises(ValueError):
            ParseLabel("Invoice")

    def test_first_and_last_page_boundaries(self):
        pages = ["first page", "second page"]
        first_payload = BuildUserPayload(pages, 0, None, "test", 1000)
        last_payload = BuildUserPayload(pages, 1, "Invoice", "test", 1000)

        self.assertIsNone(first_payload["previous_page"])
        self.assertIsNotNone(first_payload["next_page"])
        self.assertIsNotNone(last_payload["previous_page"])
        self.assertIsNone(last_payload["next_page"])

    @patch("classifier.time.sleep")
    @patch("classifier.CallOpenRouter")
    def test_failed_page_does_not_stop_document(self, mock_call, mock_sleep):
        # Page 2 fails; page 3 still runs and receives UNKNOWN as prior label.
        mock_call.side_effect = [
            "Invoice",
            ValueError("bad response"),
            ValueError("bad response"),
            ValueError("bad response"),
            "Appendix",
        ]

        results = ClassifyDocument(
            ["page one", "page two", "page three"],
            api_key="test-key",
            max_retries=2,
        )

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["label"], "Invoice")
        self.assertEqual(results[1]["status"], "failed")
        self.assertIsNone(results[1]["label"])
        self.assertEqual(results[2]["label"], "Appendix")

        third_call_payload = mock_call.call_args_list[4].args[0]
        self.assertEqual(
            third_call_payload["previous_page"]["predicted_label"],
            "UNKNOWN",
        )


if __name__ == "__main__":
    unittest.main()

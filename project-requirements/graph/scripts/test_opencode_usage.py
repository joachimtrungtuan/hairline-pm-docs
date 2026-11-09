import json
import unittest

from opencode_usage import summarise


class SummariseTest(unittest.TestCase):
    def test_sums_step_usage_and_skips_noise(self):
        lines = [
            "not json",
            json.dumps({"type": "text", "part": {"text": "hello"}}),
            json.dumps({"type": "step_finish", "part": {"cost": 0.01, "tokens": {"input": 100, "output": 20, "reasoning": 5, "cache": {"read": 50, "write": 10}}}}),
            json.dumps({"type": "step_finish", "part": {"cost": 0.02, "tokens": {"input": 200, "output": 30}}}),
        ]
        total = summarise(lines)
        self.assertEqual(total["steps"], 2)
        self.assertEqual(total["input"], 300)
        self.assertEqual(total["output"], 50)
        self.assertEqual(total["reasoning"], 5)
        self.assertEqual(total["cache_read"], 50)
        self.assertEqual(total["cache_write"], 10)
        self.assertAlmostEqual(total["cost"], 0.03)

    def test_empty_log(self):
        self.assertEqual(summarise([])["steps"], 0)


if __name__ == "__main__":
    unittest.main()

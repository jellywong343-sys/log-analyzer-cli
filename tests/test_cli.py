import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from log_analyzer_cli.cli import analyze_file, combine, normalize_message

class LogAnalyzerTests(unittest.TestCase):
    def test_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app.log"
            path.write_text(
                "2026-09-24 09:00:00 INFO request completed 200 in 12 ms\n"
                "2026-09-24 09:00:01 WARNING retry 1 returned 503\n"
                "2026-09-24 09:00:02 ERROR retry 2 returned 503\n",
                encoding="utf-8",
            )
            result = analyze_file(path)
            self.assertEqual(result.lines, 3)
            self.assertEqual(result.levels, {"ERROR": 1, "INFO": 1, "WARN": 1})
            self.assertEqual(result.status_codes, {"200": 1, "503": 2})
            self.assertEqual(combine([result])["lines"], 3)

    def test_normalization(self):
        one = normalize_message("2026-09-24 09:00:01 ERROR item 123 failed")
        two = normalize_message("2026-09-24 09:00:02 ERROR item 456 failed")
        self.assertEqual(one, two)

if __name__ == "__main__":
    unittest.main()

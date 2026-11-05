"""Регрессионные проверки точного извлечения метрик и выбора победителя."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "result_ranker", Path(__file__).parents[1] / "scripts/result_ranker.py")
ranker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ranker)


class MetricTests(unittest.TestCase):
    """Проверяет числа, имена полей и отбрасывание недостоверных значений."""

    def test_signed_and_exponential_numbers(self) -> None:
        for text, expected in [
            ("score: -2.5", -2.5), ("score: 1e-5", 0.00001),
            ("score=+2E3", 2000.0), ("score: .5", 0.5),
            ("score: 0", 0.0), ("score: -0.2e+2", -20.0),
            ("log\nscore: 2.5\nend", 2.5),
            ("'score': -3", -3.0),
        ]:
            with self.subTest(text=text):
                self.assertEqual(ranker.extract_metric(text, "score"), expected)

    def test_exact_name(self) -> None:
        for text in ["other_score: 9", "x.score: 9", "score_extra: 9", "Score: 9"]:
            with self.subTest(text=text):
                self.assertIsNone(ranker.extract_metric(text, "score"))
        self.assertEqual(ranker.extract_metric("loss.avg: -1e-3", "loss.avg"), -0.001)
        self.assertIsNone(ranker.extract_metric("lossXavg: 2", "loss.avg"))

    def test_invalid_numbers(self) -> None:
        for text in ["score: 1e", "score: 1.2.3", "score: NaN",
                     "score: Infinity", "score: 1e999", "score: 3units"]:
            with self.subTest(text=text):
                self.assertIsNone(ranker.extract_metric(text, "score"))

    def test_json(self) -> None:
        self.assertEqual(ranker.extract_metric('{"other_score":9,"score":-1e-5}', "score"), -1e-5)
        for text in ['{"score":true}', '{"score":"3"}', '{"other_score":9}',
                     '{"score":null}', '{"score":NaN}', '{"score":1e999}']:
            with self.subTest(text=text):
                self.assertIsNone(ranker.extract_metric(text, "score"))

    def test_ranking_uses_correct_values(self) -> None:
        rows = [{"agent": name, "metric_value": ranker.extract_metric(text, "score")}
                for name, text in [("a", "score: 1e-5"),
                                   ("b", "score: -2.5"),
                                   ("c", "other_score: 9")]]
        self.assertEqual([r["agent"] for r in ranker.rank_by_metric(rows)], ["b", "a", "c"])
        self.assertEqual([r["agent"] for r in ranker.rank_by_metric(rows, "higher")], ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()

import unittest

target = __import__("weather_cli")
cmd1 = target.import_dataset
cmd2 = target.analyze_dataset
cmd3 = target.export_results


class test_weather(unittest.TestCase):
    def test_import_dataset(self):
        self.assertEqual(cmd1("weather.csv"), True, "one file_name")

    def test_analyze_dataset(self):
        self.assertEqual(
            cmd2("2016-1-1 to 2017-1-1"),
            [39.76656151419559, -11, 84],
            "should be [39.76656151419559,-11,84]",
        )

    def test_export_results(self):
        self.assertEqual(
            cmd3("csv"),
            True,
            "should export results in results.csv",
        )


if __name__ == "__main__":
    unittest.main()

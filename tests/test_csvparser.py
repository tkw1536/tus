from django.test import SimpleTestCase

from tus.utils.csvparser import CSVParser


class CSVParserRegisterTests(SimpleTestCase):
    def test_register_rejects_empty_target(self):
        parser = CSVParser()

        with self.assertRaises(Exception):
            parser.register(["slug"], "", str)

    def test_register_rejects_empty_field_name(self):
        parser = CSVParser()

        with self.assertRaises(Exception):
            parser.register([""], "slug", str)

    def test_register_rejects_duplicate_field_across_groups(self):
        parser = CSVParser()
        parser.register(["slug"], "slug", str)

        with self.assertRaises(Exception):
            parser.register(["slug"], "other", str)


class CSVParserParseTests(SimpleTestCase):
    def setUp(self):
        self.parser = CSVParser()
        self.parser.register(["slug"], "slug", str)
        self.parser.register(["target"], "target", str)

    def test_parse_maps_rows_to_dicts(self):
        rows, targets = self.parser.parse(
            ["slug", "target"],
            [
                ["go", "https://example.com/"],
                ["docs", "https://example.com/docs/"],
            ],
            required=["slug", "target"],
        )

        self.assertEqual(targets, ["slug", "target"])
        self.assertEqual(
            rows,
            [
                {"slug": "go", "target": "https://example.com/"},
                {"slug": "docs", "target": "https://example.com/docs/"},
            ],
        )

    def test_parse_rejects_unknown_field(self):
        with self.assertRaises(Exception):
            self.parser.parse(["slug", "unknown"], [["go", "x"]])

    def test_parse_rejects_missing_required_target(self):
        with self.assertRaises(Exception):
            self.parser.parse(["slug"], [["go"]], required=["slug", "target"])

    def test_parse_rejects_row_with_wrong_length(self):
        with self.assertRaises(Exception):
            self.parser.parse(
                ["slug", "target"],
                [["go"]],
            )

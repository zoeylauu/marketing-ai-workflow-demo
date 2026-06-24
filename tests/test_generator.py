from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from marketing_ai_workflow.generator import (
    CampaignInput,
    generate_marketing_report,
    parse_selling_points,
    save_marketing_report,
)


class GeneratorTests(unittest.TestCase):
    def test_parse_selling_points_removes_empty_values(self):
        points = parse_selling_points("Fast setup, , Affordable, Easy reporting")

        self.assertEqual(points, ["Fast setup", "Affordable", "Easy reporting"])

    def test_generate_marketing_report_contains_required_sections(self):
        report = generate_marketing_report(
            CampaignInput(
                product_name="BrightCart",
                target_audience="independent online shop owners",
                key_selling_points=["Fast setup", "Affordable pricing", "Clear analytics"],
            )
        )

        required_sections = [
            "## Target Audience Persona",
            "## Pain Points",
            "## Emotional Triggers",
            "## Content Matrix",
            "## Instagram Captions",
            "## Hashtag Suggestions",
            "## 15-Second Short Video Scripts",
        ]

        for section in required_sections:
            self.assertIn(section, report)

    def test_save_marketing_report_writes_markdown_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = save_marketing_report("# Demo Report", output_dir=temp_dir)

            self.assertEqual(output_path.suffix, ".md")
            self.assertEqual(output_path.read_text(encoding="utf-8"), "# Demo Report")


if __name__ == "__main__":
    unittest.main()

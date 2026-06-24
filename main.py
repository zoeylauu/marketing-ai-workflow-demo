"""Command-line entry point for the marketing workflow demo."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from marketing_ai_workflow.generator import (  # noqa: E402
    CampaignInput,
    generate_marketing_report,
    parse_selling_points,
    save_marketing_report,
)


def prompt_required(label: str) -> str:
    """Ask for a required value until the user enters something."""

    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Please enter a value.")


def main() -> None:
    """Collect user input, generate a report, and save it."""

    print("AI Marketing Workflow Demo")
    print("This demo uses templates only. No paid APIs are called.\n")

    product_name = prompt_required("Product name")
    target_audience = prompt_required("Target audience")

    while True:
        raw_selling_points = prompt_required("Key selling points, separated by commas")
        key_selling_points = parse_selling_points(raw_selling_points)
        if key_selling_points:
            break
        print("Please enter at least one selling point.")

    campaign = CampaignInput(
        product_name=product_name,
        target_audience=target_audience,
        key_selling_points=key_selling_points,
    )
    report = generate_marketing_report(campaign)
    output_path = save_marketing_report(report)

    print(f"\nDone. Your report was saved to: {output_path}")


if __name__ == "__main__":
    main()

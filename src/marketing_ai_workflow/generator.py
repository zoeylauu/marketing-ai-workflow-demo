"""Marketing report generation using simple templates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import textwrap


@dataclass(frozen=True)
class CampaignInput:
    """User-provided campaign details."""

    product_name: str
    target_audience: str
    key_selling_points: list[str]


def generate_marketing_report(campaign: CampaignInput) -> str:
    """Create a structured Markdown marketing report from templates."""

    product = campaign.product_name.strip()
    audience = campaign.target_audience.strip()
    selling_points = [point.strip() for point in campaign.key_selling_points if point.strip()]

    if not product:
        raise ValueError("Product name is required.")
    if not audience:
        raise ValueError("Target audience is required.")
    if not selling_points:
        raise ValueError("At least one key selling point is required.")

    primary_point = selling_points[0]
    selling_points_md = "\n".join(f"- {point}" for point in selling_points)
    pain_points_md = "\n".join(
        f"- They want {point.lower()}, but may not know which product to trust."
        for point in selling_points[:4]
    )
    emotional_triggers_md = "\n".join(
        [
            f"- Confidence: {product} helps them feel ready to make a smart choice.",
            f"- Relief: It reduces friction around {primary_point.lower()}.",
            "- Belonging: The message should make the audience feel understood.",
            "- Momentum: The campaign should make taking the next step feel simple.",
        ]
    )
    content_matrix_md = _build_content_matrix(product, audience, selling_points)
    captions_md = _build_instagram_captions(product, audience, selling_points)
    hashtags_md = _build_hashtags(product, audience, selling_points)
    videos_md = _build_video_scripts(product, audience, selling_points)

    return textwrap.dedent(
        f"""\
        # Marketing Workflow Report: {product}

        ## Campaign Input

        **Product name:** {product}

        **Target audience:** {audience}

        **Key selling points:**
        {selling_points_md}

        ## Target Audience Persona

        **Persona name:** The Practical Optimizer

        **Profile:** A member of {audience} who wants a product that feels useful, credible, and easy to choose.

        **Buying mindset:** They compare options quickly, look for proof, and respond well to clear benefits.

        **What they need to hear:** "{product} helps you get {primary_point.lower()} without adding extra complexity."

        ## Pain Points

        {pain_points_md}
        - They see too many similar offers and need a clear reason to care.
        - They may delay buying if the value is not obvious in the first few seconds.

        ## Emotional Triggers

        {emotional_triggers_md}

        ## Content Matrix

        {content_matrix_md}

        ## Instagram Captions

        {captions_md}

        ## Hashtag Suggestions

        {hashtags_md}

        ## 15-Second Short Video Scripts

        {videos_md}
        """
    )


def save_marketing_report(report: str, output_dir: Path | str = "outputs") -> Path:
    """Save a Markdown report and return its file path."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = directory / f"marketing-report-{timestamp}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def parse_selling_points(raw_value: str) -> list[str]:
    """Parse comma-separated selling points from terminal input."""

    return [point.strip() for point in raw_value.split(",") if point.strip()]


def _build_content_matrix(product: str, audience: str, selling_points: list[str]) -> str:
    rows = [
        (
            "Awareness",
            "Instagram Reel",
            f"Show a common problem for {audience} and introduce {product}.",
            f"Lead with {selling_points[0].lower()}.",
        ),
        (
            "Consideration",
            "Carousel Post",
            f"Break down 3 reasons {product} is a smart choice.",
            "Make each slide focus on one benefit.",
        ),
        (
            "Trust",
            "Story Poll",
            "Ask the audience what challenge matters most to them.",
            "Use answers to guide follow-up content.",
        ),
        (
            "Conversion",
            "Short Video Ad",
            f"Show the before-and-after feeling of choosing {product}.",
            "End with a clear next step.",
        ),
    ]
    table = [
        "| Funnel Stage | Content Type | Message Idea | Execution Tip |",
        "| --- | --- | --- | --- |",
    ]
    table.extend(f"| {stage} | {kind} | {idea} | {tip} |" for stage, kind, idea, tip in rows)
    return "\n".join(table)


def _build_instagram_captions(product: str, audience: str, selling_points: list[str]) -> str:
    templates = [
        f"Meet {product}: built for {audience} who want {selling_points[0].lower()} without the guesswork.",
        f"If you have been waiting for a simpler way to get {selling_points[-1].lower()}, {product} is worth a look.",
        f"Small decision, big difference. {product} helps {audience} move from unsure to ready.",
    ]
    return "\n".join(f"{index}. {caption}" for index, caption in enumerate(templates, start=1))


def _build_hashtags(product: str, audience: str, selling_points: list[str]) -> str:
    source_terms = [product, audience, *selling_points, "marketing", "small business", "digital marketing"]
    hashtags = []
    for term in source_terms:
        normalized = re.sub(r"[^a-zA-Z0-9]+", "", term.title())
        if normalized:
            hashtags.append(f"#{normalized}")
    unique_hashtags = list(dict.fromkeys(hashtags))
    return " ".join(unique_hashtags[:12])


def _build_video_scripts(product: str, audience: str, selling_points: list[str]) -> str:
    primary_point = selling_points[0]
    secondary_point = selling_points[-1]
    scripts = [
        (
            "Problem to Solution",
            [
                f"0-3s: Show a frustrating moment for {audience}.",
                f"4-8s: Introduce {product} as the simpler option.",
                f"9-12s: Highlight {primary_point.lower()}.",
                "13-15s: End with: Try it today and make the next step easier.",
            ],
        ),
        (
            "Benefit Stack",
            [
                f"0-3s: Text on screen: What if {secondary_point.lower()} felt easy?",
                f"4-10s: Show 2-3 quick product benefit shots for {product}.",
                f"11-13s: Reinforce that it is made for {audience}.",
                "14-15s: End with a clean call to action.",
            ],
        ),
    ]
    formatted_scripts = []
    for title, beats in scripts:
        beat_text = "\n".join(f"   - {beat}" for beat in beats)
        formatted_scripts.append(f"### {title}\n\n{beat_text}")
    return "\n\n".join(formatted_scripts)

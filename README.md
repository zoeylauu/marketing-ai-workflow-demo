# Zoey Liu Portfolio Website

A clean, responsive portfolio website for Zoey Liu, a Digital Media Management student focused on AI-driven digital marketing, marketing analytics, consumer insights, and digital content workflow.

The site is built with plain HTML, CSS, and JavaScript. It does not use React or any other front-end framework.

## Pages and Sections

- Home
- About
- Featured projects
- Skills
- Contact

## Featured Projects

- AI Content Workflow for Social Media Campaigns
- Duolingo Short-Form Video Marketing Analysis
- Green Shipping Sustainability Campaign
- TailBliss Digital Brand Strategy

## How to Run the Website

Open `index.html` in a web browser.

You can also use a local static server if you prefer:

```bash
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Public Metadata Workflow

The Duolingo case study includes a semi-automated data collection script that uses `yt-dlp` to collect publicly visible YouTube metadata for recent Duolingo short-form videos. It does not download videos.

Install `yt-dlp`:

```bash
python -m pip install yt-dlp
```

Run the script:

```powershell
python scripts/fetch_duolingo_youtube_metadata.py
```

You can also pass specific YouTube or Shorts URLs:

```bash
python scripts/fetch_duolingo_youtube_metadata.py "https://www.youtube.com/@duolingo/shorts"
```

The script writes:

```text
data/duolingo_youtube_shorts.csv
```

The CSV includes public video metadata, duration, rule-based content pillar labels, rule-based hook type labels, and an engagement proxy calculated as `(likes + comments) / views`. If view count is missing or zero, the engagement proxy is left blank.

This workflow uses publicly visible YouTube metadata only. It does not use private analytics, sales data, ad performance data, or internal Duolingo data.

## Project Structure

```text
.
|-- index.html
|-- css/
|   `-- style.css
|-- js/
|   `-- main.js
|-- projects/
|   |-- ai-content-workflow.html
|   |-- social-media-analytics.html
|   |-- green-shipping-campaign.html
|   `-- tailbliss-brand-strategy.html
|-- scripts/
|   `-- fetch_duolingo_youtube_metadata.py
|-- data/
|   `-- duolingo_youtube_shorts.csv
`-- README.md
```

## Customization Notes

- Update the contact section with a real email address or portfolio link before publishing.
- Replace or expand project descriptions as more portfolio work becomes available.
- Add screenshots, case study links, or downloadable resume links when ready.

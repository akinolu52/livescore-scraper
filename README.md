# LiveScore Team Game Crawler

A Python-based web crawler to fetch and download the last N games for any football team from LiveScore, with a simple Streamlit UI and CSV export functionality.

## Features

- 🔍 **Automated Build ID Extraction** - Automatically extracts LiveScore's Next.js build ID, no manual updates needed
- ⚽ **Fetch Team Games** - Get recent games for any team on LiveScore
- 📊 **Interactive Display** - View games in a clean, sortable table
- 📥 **CSV Export** - Download game data as CSV for further analysis
- 🎨 **Modern UI** - Built with Streamlit for a clean, responsive interface

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

### 2. Clone and Setup

```bash
cd /Users/mac/Desktop/web/backend/crawl-games
uv sync
```

This will automatically:
- Install Python 3.12 (if needed)
- Create a virtual environment
- Install all dependencies (streamlit, requests, pandas, beautifulsoup4)

## Usage

### Run the Streamlit App

```bash
uv run streamlit run src/app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Using the App

1. **Enter Team Information** in the sidebar:
   - **Team Name**: URL-friendly team name (e.g., `west-ham-united`)
   - **Team ID**: Numeric ID from LiveScore URL (e.g., `252`)
   - **Number of Games**: How many recent games to fetch (1-50)

2. **Click "Fetch Games"** to retrieve the data

3. **View Results** in the interactive table

4. **Download CSV** using the download button

### Finding Team Information

1. Visit [livescore.com](https://www.livescore.com)
2. Search for your team
3. Look at the URL: `/team/west-ham-united/252/overview`
   - Team Name: `west-ham-united`
   - Team ID: `252`

### Example Teams

| Team | Team Name | Team ID |
|------|-----------|---------|
| West Ham United | `west-ham-united` | `252` |
| Arsenal | `arsenal` | `675` |
| Liverpool | `liverpool` | `24` |
| Real Madrid | `real-madrid` | `418` |
| Barcelona | `barcelona` | `421` |
| Juventus | `juventus` | `506` |

## Project Structure

```
crawl-games/
├── src/
│   ├── scraper.py      # Core scraping logic
│   └── app.py          # Streamlit web interface
├── pyproject.toml      # Project dependencies
├── .python-version     # Python version (3.12)
├── .gitignore
└── README.md
```

## How It Works

1. **Build ID Extraction**: The scraper automatically fetches LiveScore's homepage and extracts the Next.js build ID from the HTML source
2. **API Request**: Uses the build ID to construct the API endpoint URL
3. **Data Parsing**: Parses the JSON response to extract game details (date, teams, scores, competition, status)
4. **Display**: Shows the data in an interactive Streamlit dataframe
5. **Export**: Converts to CSV for download

## Data Fields

The CSV export includes the following fields:

- **Date**: Match date and time
- **Home Team**: Home team name
- **Away Team**: Away team name
- **Score**: Match score (or "vs" for upcoming games)
- **Competition**: Competition name (e.g., "Premier League")
- **Stage**: Competition stage (e.g., "Premier League", "Round 3")
- **Status**: Match status (e.g., "FT", "Upcoming")

## Troubleshooting

### Build ID Issues

If you encounter errors about the build ID, the scraper will automatically try to extract a new one. If this fails:
- LiveScore may have changed their website structure
- Check your internet connection
- Try again in a few moments

### Invalid Team ID/Name

- Verify the team ID and name from the LiveScore URL
- Team names should be lowercase and hyphenated (e.g., `west-ham-united`)
- Team IDs are numeric (e.g., `252`)

## Dependencies

- **streamlit** - Web UI framework
- **requests** - HTTP library for API calls
- **pandas** - Data manipulation and CSV export
- **beautifulsoup4** - HTML parsing for build ID extraction

## License

MIT
# livescore-scraper

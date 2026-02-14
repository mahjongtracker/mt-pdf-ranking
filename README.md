# Tournament Ranking PDF Generator

Generate a printable PDF ranking table from [mahjongtracker.com](https://mahjongtracker.com) tournament data.

## Usage

Run the script with a tournament ID:

```bash
uv run ranking_pdf.py <tournament_id>
```

### Example

```bash
uv run ranking_pdf.py 699036bea3ee3d000a4c8e0d
```

This will:
1. Fetch the tournament name and ranking data from the API
2. Generate `ranking.pdf` in the current directory with a table containing:
   - Place (ranking position)
   - Player Name
   - Total Points

## Requirements

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

Dependencies are managed automatically by uv:
- `requests` - API calls
- `fpdf2` - PDF generation

## Finding Tournament IDs

Tournament IDs can be found in the URL when viewing a tournament on mahjongtracker.com:
```
https://mahjongtracker.com/tournaments/{tournament_id}
```

#!/usr/bin/env python3
"""Generate PDF ranking from mahjongtracker.com tournament data."""

import sys
import requests
from fpdf import FPDF


def fetch_tournament_details(tournament_id):
    """Fetch tournament details from mahjongtracker.com API."""
    url = f"https://mahjongtracker.com/api/v1/tournaments/{tournament_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_ranking(tournament_id):
    """Fetch ranking data from mahjongtracker.com API."""
    url = f"https://mahjongtracker.com/api/v1/tournaments/{tournament_id}/ranking"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def generate_pdf(ranking_data, tournament_name, output_path="ranking.pdf"):
    """Generate PDF table with ranking data."""
    pdf = FPDF()
    pdf.add_page()

    # Use DejaVu Sans for Unicode support (bundled with fpdf2)
    pdf.add_font("DejaVu", "", fname="DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", fname="DejaVuSans-Bold.ttf")

    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, tournament_name, align="C", ln=True)
    pdf.ln(5)

    # Table header
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(20, 10, "Place", border=1, align="C")
    pdf.cell(120, 10, "Player Name", border=1, align="C")
    pdf.cell(40, 10, "Total Points", border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("DejaVu", "", 12)
    for idx, entry in enumerate(ranking_data, start=1):
        player_name = entry["player"]["name"]
        total_points = entry["total_points"]

        pdf.cell(20, 10, str(idx), border=1, align="C")
        pdf.cell(120, 10, player_name, border=1)
        pdf.cell(40, 10, str(total_points), border=1, align="R")
        pdf.ln()

    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: ranking_pdf.py <tournament_id>")
        sys.exit(1)

    tournament_id = sys.argv[1]

    print(f"Fetching tournament details...")
    tournament_details = fetch_tournament_details(tournament_id)
    tournament_name = tournament_details.get("name", "Tournament Ranking")

    print(f"Fetching ranking for {tournament_name}...")
    ranking_data = fetch_ranking(tournament_id)

    generate_pdf(ranking_data, tournament_name)


if __name__ == "__main__":
    main()

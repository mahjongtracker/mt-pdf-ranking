#!/usr/bin/env python3
"""Generate PDF ranking from mahjongtracker.com tournament data."""

import sys
from datetime import datetime
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

    class PDFWithFooter(FPDF):
        def footer(self):
            # Text at 10mm from bottom
            self.set_y(-10)
            self.set_font("DejaVu", "", 6)
            self.cell(0, 2, "Powered by Mahjong Tracker - mahjongtracker.com", align="C")

    pdf = PDFWithFooter()

    # Use DejaVu Sans for Unicode support
    pdf.add_font("DejaVu", "", fname="DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", fname="DejaVuSans-Bold.ttf")

    pdf.add_page()
    pdf.set_margins(10, 10, 10)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 6, tournament_name, align="C", ln=True)

    # Timestamp subtitle
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.set_font("DejaVu", "", 8)
    pdf.cell(0, 4, f"(generated at {timestamp})", align="C", ln=True)
    pdf.ln(10)

    # Table header
    pdf.set_font("DejaVu", "B", 9)
    pdf.cell(15, 5, "Place", border=1, align="C")
    pdf.cell(140, 5, "Player Name", border=1, align="C")
    pdf.cell(35, 5, "Total Points", border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("DejaVu", "", 9)
    for idx, entry in enumerate(ranking_data, start=1):
        player_name = entry["player"]["name"]
        total_points = entry["total_points"]

        pdf.cell(15, 5, str(idx), border=1, align="C")
        pdf.cell(140, 5, player_name, border=1)
        pdf.cell(35, 5, str(total_points), border=1, align="R")
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

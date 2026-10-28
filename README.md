# Crime Pattern Analysis & Community Safety Awareness

A college-project Flask website with:
- Dashboard and charts
- Interactive Leaflet/OpenStreetMap crime hotspot map
- Geo-tagged analysis
- Crime information and safety tips
- Community survey link
- Survey results section
- Findings
- Python-based Low/Medium/High risk analysis
- Safety concern reporting form
- Emergency numbers
- Methodology, dataset, about and references

## Run
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Open Terminal.
4. Run:
   `pip install -r requirements.txt`
5. Run:
   `python app.py`
6. Open:
   `http://127.0.0.1:5000`

The app creates a sample `crime.db` automatically on first run.

## Customize
Edit the student/college/guide details in `templates/about.html`.
Replace the Google Form URL in `templates/survey.html`.
Replace sample dataset values with your actual college-project data.

The map uses Leaflet + OpenStreetMap tiles and opens from the **Crime Hotspot Map** page.

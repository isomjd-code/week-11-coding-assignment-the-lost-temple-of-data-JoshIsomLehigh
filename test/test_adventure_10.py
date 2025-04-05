import pytest
import pandas as pd
from pathlib import Path
import adventure as ap # Import student's code, aliased as 'ap'

# --- Fixtures to create temporary sample files ---

@pytest.fixture
def sample_excel_file(tmp_path):
    """Creates a temporary sample artifacts.xlsx file."""
    file_path = tmp_path / "artifacts.xlsx"
    # Create a Pandas Excel writer using openpyxl as the engine.
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Write irrelevant data to the first sheet
        df_sheet1 = pd.DataFrame({'Ignore': [1, 2]})
        df_sheet1.to_excel(writer, sheet_name='Sheet1', index=False)

        # Write relevant data to the 'Main Chamber' sheet with header rows
        df_main = pd.DataFrame({
            'ArtifactName': ['Golden Idol', 'Jade Monkey', 'Obsidian Dagger'],
            'EstimatedValue': [5000, 1500, 800],
            'RoomFound': ['Altar Room', 'Treasury', 'Sacrificial Chamber']
        })
        # Simulate header rows by writing empty frames first
        pd.DataFrame(['Temple of Azmar - Artifact Inventory']).to_excel(writer, sheet_name='Main Chamber', index=False, header=False, startrow=0)
        pd.DataFrame(['Report Date: 2024-10-30']).to_excel(writer, sheet_name='Main Chamber', index=False, header=False, startrow=1)
        # Actual data starts after row 3 (index 3), headers on row 4 (index 3 after skipping)
        df_main.to_excel(writer, sheet_name='Main Chamber', index=False, startrow=3)
    return file_path

@pytest.fixture
def sample_tsv_file(tmp_path):
    """Creates a temporary sample locations.tsv file."""
    file_path = tmp_path / "locations.tsv"
    content = "LocationID\tDescription\tDangerLevel\n" \
              "LOC01\tEntrance Hall\tLow\n" \
              "LOC02\tAltar Room\tMedium\n" \
              "LOC03\tTreasury\tHigh"
    file_path.write_text(content, encoding='utf-8')
    return file_path

@pytest.fixture
def sample_journal_text():
    """Provides sample journal text content."""
    return """
    Dr. Evelyn Reed - Azmar Expedition Journal

    Entry: 10/25/2024
    Made it inside the main entrance (LOC01). Air is stale. Found strange markings. Code AZMAR-999 seems off.

    Entry: 10/26/2024
    Reached the Altar Room (LOC02). Discovered the Golden Idol! It matches code AZMAR-101. Incredible find.

    Entry: 10/27/2024
    Navigated to the Treasury (LOC03). Found the Jade Monkey. Security code AZMAR-256 seems relevant here. Need to log this by 11/01/2024.

    Entry: 10/28/2024
    Found the Sacrificial Chamber (LOC04). Very unsettling. Recovered the Obsidian Dagger. This corresponds to AZMAR-007 in the old texts.

    Entry: 10/29/2024
    Explored the Flooded Passage (LOC05). Difficult terrain. No major artifacts, but found map fragment AZMAR-314. Planning extraction for 11/05/2024. Invalid date 99/99/9999.
    """

@pytest.fixture
def empty_journal_text():
    """Provides journal text with no matching patterns."""
    return "Journal Entry: No relevant codes or standard dates found here. Maybe next time. AZMAR-ABC is not a code."

# --- Test Functions ---



def test_extract_no_matches(empty_journal_text):
    """Tests that regex functions return empty lists when no patterns match."""
    dates = ap.extract_journal_dates(empty_journal_text)
    codes = ap.extract_secret_codes(empty_journal_text)
    assert dates == [], "Expected empty list for dates when no matches found"
    assert codes == [], "Expected empty list for codes when no matches found"

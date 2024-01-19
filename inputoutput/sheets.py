import pandas as pd

from inputoutput.readwrite import seed_sentences_location, legos_location, write_seed_sentences, write_legos

SHEET_ID = r'1hPVfuP9wQun4OWg7_mYM1qPg3VuYamUecne0wEZjCl4'


def _remove_whitespace(string) -> str:
    return string.replace(" ", "%20")


def write_source_json_from_sheets(overwrite_existing: bool) -> None:
    both_files_exist = seed_sentences_location.exists() and legos_location.exists()

    if both_files_exist and not overwrite_existing:
        return None

    seeds_url = (fr'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet='
                 fr'{_remove_whitespace('Translations Of Seeds')}')
    legos_url = (fr'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet='
                 fr'{_remove_whitespace('Seeds to Words (Items)')}')

    seeds_df = pd.read_csv(seeds_url)[["English", "Chinese"]].dropna()
    legos_df = pd.read_csv(legos_url)[["English Legos", "Chinese Legos"]].dropna()

    write_seed_sentences(seeds_df)
    write_legos(legos_df)

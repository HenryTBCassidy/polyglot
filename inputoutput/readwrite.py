import json
from pathlib import Path
from typing import Union

import pandas as pd

OUTPUT = Path(r"C:\Users\Henry\PycharmProjects\pythonProject\output")
INPUT = Path(r"C:\Users\Henry\PycharmProjects\pythonProject\input")
seed_sentences_location = INPUT / 'seedsentences.json'
legos_location = INPUT / 'legos.json'
seeds_and_legos_location = OUTPUT / 'seedsandlegos.json'


def read_seed_sentences() -> pd.DataFrame:
    return pd.read_json(seed_sentences_location)


def read_legos() -> pd.DataFrame:
    return pd.read_json(legos_location)


def read_assembled_seeds() -> dict[dict[str, Union[str, list[dict]]]]:
    with open(seeds_and_legos_location) as json_file:
        return json.load(json_file)


def write_seed_sentences(seeds_df: pd.DataFrame) -> None:
    seeds_df.to_json(seed_sentences_location)


def write_legos(legos_df: pd.DataFrame) -> None:
    legos_df.to_json(legos_location)


def write_assembled_seed_sentences(results: dict) -> None:
    json_object = json.dumps(results)

    with open(seeds_and_legos_location, "w") as outfile:
        outfile.write(json_object)

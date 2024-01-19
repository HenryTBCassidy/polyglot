import json

import pandas as pd

from inputoutput.readwrite import write_assembled_seed_sentences, read_seed_sentences, read_legos
from library.phrases import SeedSentenceBuilder
from library.trees import LegoNode
from library.wrappers import LegoValueId, LegoId, SeedSentenceValueId, SeedSentenceId


def _get_legos_for_seed(seed_value_id: SeedSentenceValueId, legos: pd.DataFrame) -> list[list[LegoNode]]:
    # ALGORITHM
    # 1. When you find legos that fit in the seed sentence, store them ordered by the index of their first character
    #    in the seed sentence
    # 2. To check if legos can make seed sentence, try and build a tree using legos to take you from start of seed
    #    sentence to end
    # 3. Return empty list if we are unsuccessful

    seed_sentence_builder = SeedSentenceBuilder(target_seed_sentence=seed_value_id)
    current_lego_index = 0

    while current_lego_index < len(legos):
        current_lego_value = legos.loc[current_lego_index].lower()
        current_lego_value_id = LegoValueId(lego_id=LegoId(current_lego_index), string_value=current_lego_value)
        seed_sentence_builder.check_lego_potentially_needed_for_seed(current_lego_value_id)
        current_lego_index += 1

    if seed_sentence_builder.check_seed_sentence_can_be_made_from_potential_legos():
        return seed_sentence_builder.definite_lego_paths
    else:
        return []


def choose_smallest_lego_list(data: list[dict]) -> dict:
    if len(data) == 0:
        return {}
    take = data[0]
    for d in data[0:]:
        if len(d) < len(take):
            take = d
    return take


def find_legos_for_seed_sentences():
    seed_sentences = read_seed_sentences()
    legos = read_legos()["English Legos"]
    seed_index = 0

    results = {}
    for i in range(len(seed_sentences)):
        seed_sentence = seed_sentences.loc[seed_index, 'English']
        current_seed_value_id = SeedSentenceValueId(seed_sentence_id=SeedSentenceId(seed_index),
                                                    string_value=seed_sentence)
        legos_for_seed = _get_legos_for_seed(current_seed_value_id, legos)
        assemblies_list = []
        for item in legos_for_seed:
            inner_d = {}
            for ln in item:
                inner_d.update({ln.value_id.lego_id: ln.value_id.string_value})
            assemblies_list.append(inner_d)
        phrase_result = dict()
        phrase_result["value"] = current_seed_value_id.string_value
        phrase_result["assemblies"] = assemblies_list
        phrase_result["best_assembly"] = choose_smallest_lego_list(assemblies_list)
        results[current_seed_value_id.seed_sentence_id] = phrase_result

        seed_index += 1

    write_assembled_seed_sentences(results)

    decoded = {k: v for k, v in results.items() if len(v["assemblies"]) != 0}
    multiple_paths = {k: v for k, v in results.items() if len(v["assemblies"]) > 1}
    print(fr"Seed sentences decoded: {len(decoded)} out of {len(results)} i.e {100 * len(decoded) / len(results)} %")
    print(fr"Seed sentences with multiple constructions: {len(multiple_paths)} out of {len(decoded)} " +
          fr"i.e {100 * len(multiple_paths) / len(decoded)} %")

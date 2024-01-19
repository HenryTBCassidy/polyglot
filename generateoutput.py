# ALGORITHM
# 1. Introduce lego 1 and store as learned lego
# 2. Introduce lego 2 with some combination of lego 1 and store
# 3. Keep going until all legos are learned for a phrase, store phrase as learned phrases
# 4. Keep going with next phrase and next legos, but randomly select legos from learned list to build new sentences
from inputoutput.readwrite import read_assembled_seeds
from library.wrappers import LegoId, SeedSentenceId
from typing import Union

learned_legos: list[LegoId] = []
learned_phrases: list[SeedSentenceId] = []


def make_output():
    assembled_phrases: dict[dict[str, Union[str, list[dict]]]] = read_assembled_seeds()
    phrases_to_learn = {i: d for i, d in assembled_phrases.items() if len(d["assemblies"]) > 0}

    for id, data in assembled_phrases.items():
        # ALGORITHM
        # learned_legos += the_one_learnt
        # check the legos that exist and see which combinations make a phrase
        # store that one as learnt
        # keep going until all phrases done
        break

    pass

from generateoutput import make_output
from inputoutput.sheets import write_source_json_from_sheets
from phraseassembly import find_legos_for_seed_sentences

if __name__ == '__main__':
    # 1. Read inputs
    # 2. Find all (not much slower) possible ways of making phrases from legos and writes this out
    #    (Later this will be: for each phrase, generate the legos)
    # 3. Builds output phrases from legos, randomly choosing learned legos to test understanding
    write_source_json_from_sheets(overwrite_existing=False)
    find_legos_for_seed_sentences()
    make_output()

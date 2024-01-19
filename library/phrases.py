from .trees import LegoNode
from .wrappers import LegoValueId, SeedSentenceValueId
from utils import contains_words


class SeedSentenceBuilder(object):
    def __init__(self, target_seed_sentence: SeedSentenceValueId):
        self.original_target_seed_sentence = target_seed_sentence
        self.formatted_target_seed_sentence = self._remove_punctuation(target_seed_sentence.string_value).lower()
        self.target_seed_sentence_words: list[str] = self.formatted_target_seed_sentence.split(" ")
        self.sorted_potential_legos: dict[int, list[LegoValueId]] = {}
        self.definite_lego_paths: list[list[LegoNode]] = []

    @staticmethod
    def _remove_punctuation(string: str):
        return (
            string.replace("?", "").replace(".", "")
            .replace("!", "").replace(",", "")
        )

    def check_lego_potentially_needed_for_seed(self, lego_value_id: LegoValueId) -> bool:
        if contains_words(words=lego_value_id.string_value, sentence=self.formatted_target_seed_sentence):
            self._ordered_insert_of_potential_lego(lego_value_id)
            return True
        return False

    def _ordered_insert_of_potential_lego(self, lego_value_id: LegoValueId) -> None:
        insertion_index = self.formatted_target_seed_sentence.index(lego_value_id.string_value)
        if insertion_index in self.sorted_potential_legos:
            self.sorted_potential_legos[insertion_index].append(lego_value_id)
            sorted(self.sorted_potential_legos[insertion_index], key=lambda lvid: lvid.string_value)
        else:
            self.sorted_potential_legos[insertion_index] = [lego_value_id]
        self.sorted_potential_legos = dict(sorted(self.sorted_potential_legos.items()))

    def check_seed_sentence_can_be_made_from_potential_legos(self) -> bool:
        if 0 in self.sorted_potential_legos:  # Cannot make sentence if we don't start at beginning
            roots = LegoNode.create_nodes_from_list(insertion_index=0, items=self.sorted_potential_legos[0])

            for node in roots:
                node.add_children(self.sorted_potential_legos, self.formatted_target_seed_sentence)

            routes_to_end = [path for root in roots for path in root.routes_to_end()]
            if len(routes_to_end) > 0:
                self.definite_lego_paths = routes_to_end
                return True
        else:
            return False

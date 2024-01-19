from .wrappers import LegoValueId


# ALGORITHM: As you discover legos that fit in the sentence, build a tree
# 1. Start with ordered dictionary of index of first string and list of lego ids with this string eg
#    {
#     0: [(0,"i"), (100,"i don't know")],
#     13: [(36,"how"), (91, "how to say")],
#     24: [(97,"enough"), (103,"enough different words")],
#     31: [(101,"different"), (102,"different words")],
#     41: [(93, "words")],
#     47: [(104,"yet")]
# }
# 2. Try and build a tree starting at the first value e.g (0,"i") which is at position 0 in the target sentence
# 3. A node's children are defined by the values in the sorted dictionary at
#    next_index = current_index +len(current_string) + 1
# 4. Recursively add children for each node

class LegoNode(object):
    def __init__(self, lego_value_id: LegoValueId, insertion_index: int):
        self.value_id = lego_value_id
        self.index = insertion_index
        self.children: list[LegoNode] = []
        self.is_end = False

    @classmethod
    def create_nodes_from_list(cls, insertion_index: int, items: list[LegoValueId]) -> list['LegoNode']:
        return [LegoNode(lego_value_id=item, insertion_index=insertion_index) for item in items]

    def add_children(self, sorted_potential_legos: dict[int, list[LegoValueId]], target_seed_sentence: str) -> None:
        end = len(target_seed_sentence)
        new_key = self.reach + 1
        if new_key == end + 1:
            self.is_end = True
            return None
        if new_key in sorted_potential_legos:
            self.children = self.create_nodes_from_list(new_key, sorted_potential_legos[new_key])
            for child in self.children:
                child.add_children(sorted_potential_legos, target_seed_sentence)
        else:
            return None

    def tree(self, level=0) -> str:
        ret = "\t" * level + repr(self.value_id) + "\n"
        for child in self.children:
            ret += child.tree(level + 1)
        return ret

    def __repr__(self):
        return fr"{self.value_id}"

    def routes_to_end(self) -> list[list['LegoNode']]:
        if self.is_end:
            yield [self]
        for child in self.children:
            for path in child.routes_to_end():
                yield [self] + path

    @property
    def reach(self):
        return self.index + len(self.value_id.string_value)

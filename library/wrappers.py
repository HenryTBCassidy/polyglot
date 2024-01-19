# Wrappers around int to make sure legos and phrases do not get confused
# NB: Both of these are immutable
class LegoId(int):
    def __init__(self, val: int):
        self.val = val

    def __int__(self):
        return self.val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return repr(self.val)


class LegoValueId(object):
    def __init__(self, lego_id: LegoId, string_value: str):
        self.lego_id = lego_id
        self.string_value = string_value

    def __repr__(self):
        return fr"{self.lego_id}:{self.string_value}"


class SeedSentenceId(int):
    def __init__(self, val: int):
        self.val = val

    def __int__(self):
        return self.val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return repr(self.val)


class SeedSentenceValueId(object):
    def __init__(self, seed_sentence_id: SeedSentenceId, string_value: str):
        self.seed_sentence_id = seed_sentence_id
        self.string_value = string_value

    def __repr__(self):
        return fr"{self.seed_sentence_id}:{self.string_value}"

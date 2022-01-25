from typing import Union

import markovify
import jieba
from markovify import Text


class MarkovifyInterface:
    def __init__(self):
        self.models = []
        self.texts = []
        self.text_cnt = 0
        self.combined_model: Union[None, Text] = None

    def add_text(self, texts, split_by="\n"):
        for t in texts.split(split_by):
            if len(t) > 0:
                self.texts.append(t)

    def gen_model(self):
        self.combined_model = markovify.combine(models=self.models)

    def convent_text_2_model(self):
        while len(self.texts) > 0:
            text = self.texts.pop()
            self.models.append(markovify.Text(text))

    def make_sentence(self, max_times_invocation=10):
        self.convent_text_2_model()
        self.gen_model()
        sentence = None
        index = 0
        while sentence is None and index < max_times_invocation:
            sentence = self.combined_model.make_sentence()
            index += 1
        return sentence

    def to_json(self):
        self.convent_text_2_model()
        self.gen_model()
        return self.combined_model.to_json()

    def load_json(self, json_str):
        self.combined_model = markovify.Text.from_json(json_str)

# unit test
inter = MarkovifyInterface()

#
inter.add_text("你好嗎\n我很好", split_by="\n")
inter.make_sentence()

#
json_str = inter.to_json()
inter.load_json(json_str)
assert json_str == inter.to_json()
from app.utils.text_utils import clamp, sentence_count, words


class ClarityScorer:
    def score(self, text: str, **kwargs) -> float:
        tokens = words(text)
        avg_sentence = len(tokens) / sentence_count(text)
        length_score = 100 - abs(avg_sentence - 16) * 2.8
        jargon_penalty = sum(token in {"synergy", "leverage", "disruptive", "paradigm"} for token in tokens) * 5
        return clamp(length_score - jargon_penalty)

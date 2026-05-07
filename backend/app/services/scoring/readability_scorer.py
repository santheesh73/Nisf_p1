from app.utils.text_utils import clamp, sentence_count, words


class ReadabilityScorer:
    def score(self, text: str, **kwargs) -> float:
        tokens = words(text)
        if not tokens:
            return 0
        avg_word = sum(len(token) for token in tokens) / len(tokens)
        avg_sentence = len(tokens) / sentence_count(text)
        return clamp(110 - avg_word * 8 - max(0, avg_sentence - 18) * 2)

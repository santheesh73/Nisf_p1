class ContentModeration:
    unsafe_terms = {"hate", "violence", "kill", "scam", "fraud", "exploit"}

    def check(self, text: str) -> dict:
        lowered = text.lower()
        hits = sorted(term for term in self.unsafe_terms if term in lowered)
        return {"safe": not hits, "flags": hits}

from app.pipelines.base_pipeline import BasePipeline


class VideoPipeline(BasePipeline):
    def validate_input(self, payload): raise NotImplementedError("Video pipeline is planned")
    def generate(self, payload): raise NotImplementedError("Video pipeline is planned")
    def simulate(self, payload): raise NotImplementedError("Video pipeline is planned")
    def score(self, payload): raise NotImplementedError("Video pipeline is planned")
    def critique(self, payload): raise NotImplementedError("Video pipeline is planned")
    def optimize(self, payload): raise NotImplementedError("Video pipeline is planned")
    def build_output(self, payload): raise NotImplementedError("Video pipeline is planned")

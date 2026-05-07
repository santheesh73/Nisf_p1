from app.pipelines.base_pipeline import BasePipeline


class ImagePipeline(BasePipeline):
    def validate_input(self, payload): raise NotImplementedError("Image pipeline is planned")
    def generate(self, payload): raise NotImplementedError("Image pipeline is planned")
    def simulate(self, payload): raise NotImplementedError("Image pipeline is planned")
    def score(self, payload): raise NotImplementedError("Image pipeline is planned")
    def critique(self, payload): raise NotImplementedError("Image pipeline is planned")
    def optimize(self, payload): raise NotImplementedError("Image pipeline is planned")
    def build_output(self, payload): raise NotImplementedError("Image pipeline is planned")

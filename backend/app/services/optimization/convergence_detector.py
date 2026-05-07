class ConvergenceDetector:
    def has_converged(self, improvement: float, threshold: float) -> bool:
        return improvement < threshold

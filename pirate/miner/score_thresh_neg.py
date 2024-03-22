class ScoreThresholdMiner:
    def __init__(
        self, 
        thresh=0.5,
    ):
        self.thresh = thresh

    def mine(self, score):
        return score < self.thresh
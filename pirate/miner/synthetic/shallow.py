import dspy

from pirate.miner.synthetic.signatures import NegativeDocumentGenerator


class ShallowNegativeGenerator(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generator = dspy.Predict(NegativeDocumentGenerator)

    def forward(self, query: str, positive_document: str) -> str:
        return self.generator(
            query=query, 
            positive_document=positive_document
        ).negative_document

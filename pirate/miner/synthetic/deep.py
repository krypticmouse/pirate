import dspy

from pirate.miner.synthetic.signatures import (
    NegativeTraitGenerator,
    NegativeValidator,
    NegativeRegenerator,
    TraitBasedNegativeDocumentGenerator,
)


class DeepNegativeGenerator(dspy.Module):
    def __init__(self):
        super().__init__()

        self.trait_generator = dspy.Predict(NegativeTraitGenerator)
        self.document_generator = dspy.Predict(TraitBasedNegativeDocumentGenerator)
        self.validator = dspy.TypedPredictor(NegativeValidator)
        self.regenerator = dspy.Predict(NegativeRegenerator)


    def forward(self, query: str, positive_document: str) -> str:
        negative_traits = self.trait_generator(
            query=query, 
            positive_document=positive_document
        ).negative_traits

        negative_document = self.document_generator(
            query=query, 
            positive_document=positive_document, 
            negative_traits=negative_traits
        ).negative_document

        validation = self.validator(
            query=query,
            positive_document=positive_document,
            negative_traits=negative_traits,
            negative_document=negative_document
        ).feedback

        match validation:
            case True:
                return negative_document
            case False:
                return self.regenerator(
                    query=query,
                    negative_traits=negative_traits,
                    negative_document=negative_document
                ).regenerated_document
            case _:
                raise ValueError("Failed to generate a negative document.")

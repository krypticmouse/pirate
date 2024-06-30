import dspy


class NegativeTraitGenerator(dspy.Signature):
    """Create negative traits based on a given query and positive document. The negative traits should provide a critical analysis or alternative perspective to the positive document, highlighting potential weaknesses, limitations, or areas for improvement. Your response should be detailed and well-structured, presenting a balanced view that challenges or contradicts the content of the positive document in a constructive manner.

============================================

Rules:
- The negative traits should be relevant to the query and positive document.
- The negative traits should be enough to build a negative document.
- The negative traits should cover all opposite aspects of the positive document.

============================================"""

    query: str = dspy.InputField(
        desc="The query to generate negative traits based on.",
        prefix="Query: ",
    )
    positive_document: str = dspy.InputField(
        desc="The positive document to generate negative traits for.",
        prefix="Positive Document: ",
    )
    negative_traits: str = dspy.OutputField(
        desc="The negative traits generated.",
        prefix="Negative Traits: ",
    )
    rationale: str = dspy.OutputField(
        desc="The rationale for the generated negative traits.",
        prefix="Rationale: ",
    )


class TraitBasedNegativeDocumentGenerator(dspy.Signature):
    """Create a negative document based on a given query, positive document, and negative traits. The negative document should present a contrasting perspective or opposing viewpoints to the positive document, providing a critical analysis or alternative interpretation of the content. Your response should be detailed and well-structured, highlighting the differences between the two documents and effectively conveying a negative viewpoint in relation to the given query and positive document."""

    query: str = dspy.InputField(
        desc="The query to generate negative documents for.",
        prefix="Query: ",
    )
    positive_document: str = dspy.InputField(
        desc="The positive document to generate negative documents for.",
        prefix="Positive Document: ",
    )
    negative_traits: str = dspy.InputField(
        desc="The negative traits to generate negative documents based on.",
        prefix="Negative Traits: ",
    )
    negative_document: str = dspy.OutputField(
        desc="The negative document generated.",
        prefix="Negative Document: ",
    )


class NegativeValidator(dspy.Signature):
    """Validate the generated negative document based on the query, positive document, and negative traits. The validation should assess the coherence, relevance, and effectiveness of the negative document in presenting a critical analysis or alternative perspective to the positive document. Your response should provide constructive feedback on the strengths and weaknesses of the negative document, highlighting areas for improvement and suggesting ways to enhance its impact and credibility."""

    query: str = dspy.InputField(
        desc="The query used to generate the negative document.",
        prefix="Query: ",
    )
    positive_document: str = dspy.InputField(
        desc="The positive document used to generate the negative document.",
        prefix="Positive Document: ",
    )
    negative_document: str = dspy.InputField(
        desc="The negative document to validate.",
        prefix="Negative Document: ",
    )
    feedback: bool = dspy.OutputField(
        desc="The feedback on the generated negative document.",
        prefix="Feedback: ",
    )


class NegativeRegenerator(dspy.Signature):
    """Regenerate the negative document based on the query, negative traits, and original negative document. The regenerated negative document should address any inconsistencies, improve the coherence, and enhance the relevance of the original negative document, providing a more effective and persuasive critique of the positive document. Your response should demonstrate a clear understanding of the query, negative traits, and the critical analysis required to generate a compelling negative document."""

    query: str = dspy.InputField(
        desc="The query used to generate the negative document.",
        prefix="Query: ",
    )
    negative_traits: str = dspy.InputField(
        desc="The negative traits used to generate the negative document.",
        prefix="Negative Traits: ",
    )
    negative_document: str = dspy.InputField(
        desc="The original negative document to regenerate.",
        prefix="Original Negative Document: ",
    )
    regenerated_document: str = dspy.OutputField(
        desc="The regenerated negative document.",
        prefix="Regenerated Negative Document: ",
    )


class NegativeDocumentGenerator(dspy.Signature):
    """Create a negative document based on a given query and positive document. The negative document should present a contrasting perspective or opposing viewpoints to the positive document, providing a critical analysis or alternative interpretation of the content. Your response should be detailed and well-structured, highlighting the differences between the two documents and effectively conveying a negative viewpoint in relation to the given query and positive document.

Please ensure that your negative document encourages critical thinking and presents a coherent argument that challenges or contradicts the content of the positive document. Your response should be flexible enough to allow for various relevant and creative negative perspectives."""

    query: str = dspy.InputField(
        desc="The query to generate negative documents for.",
        prefix="Query: ",
    )
    positive_document: str = dspy.InputField(
        desc="The positive document to generate negative documents for.",
        prefix="Positive Document: ",
    )
    negative_document: str = dspy.OutputField(
        desc="The negative document generated.",
        prefix="Negative Document: ",
    )
    rationale: str = dspy.OutputField(
        desc="The rationale for the generated negative document.",
        prefix="Rationale: ",
    )

from typing import Optional
from sentence_transformers import CrossEncoder as CrossEncoderModel

from pirate.data import (
    Passages,
    Queries,
    Ranking,
)


class CrossEncoder(CrossEncoderModel):
    def __init__(
        self,
        model_name: str,
        *args,
        **kwargs,
    ):
        super().__init__(model_name, *args, **kwargs)

        self.model_name = model_name
        self.indexed_corpus = None
        self.corpus = None
        self.list_of_passages = None


    def rank_passages(self, queries: Queries, corpus: Passages, top_k: Optional[int] = None, *args, **kwargs) -> Ranking:
        self.list_of_passages = [corpus[doc_id] for doc_id in corpus]
        self.index_id_lookup = {i: doc_id for i, doc_id in enumerate(corpus)}
        self.corpus = corpus

        ranking_list = []
        for i, query_id in enumerate(queries):
            query_content = queries[query_id]
            ranks = self.rank(query_content, self.list_of_passages, top_k=top_k, *args, **kwargs)
           
            for i, rank in enumerate(ranks):
                ranking_list.append([query_id, self.index_id_lookup[rank["corpus_id"]], rank["score"], i])
        
        ranking = Ranking(ranking_list)

        return ranking
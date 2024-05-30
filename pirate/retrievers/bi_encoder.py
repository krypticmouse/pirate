from loguru import logger
from typing import Optional
from sentence_transformers import SentenceTransformer

from pirate.data import (
    Passages,
    Queries,
    Ranking,
)


class BiEncoder(SentenceTransformer):
    def __init__(
        self,
        model_name: str,
        *args,
        **kwargs,
    ):
        super().__init__(model_name, *args, **kwargs)

        self.indexed_corpus = None
        self.corpus = None
        self.list_of_passages = None


    def index(self, corpus: Passages, *args, **kwargs):
        if not isinstance(corpus, Passages):
            raise ValueError("Invalid corpus type, must be Passages or Queries.")
        
        self.list_of_passages = [corpus[doc_id] for doc_id in corpus]
        self.index_id_lookup = {i: doc_id for i, doc_id in enumerate(corpus)}

        logger.info(f"Indexing corpus on {self.model_name}...")
        self.indexed_corpus = self.encode(self.list_of_passages, *args, **kwargs)
        self.corpus = corpus

        logger.info("Finished indexing corpus.")


    def rank_passages(self, queries: Queries, top_k: Optional[int] = None, *args, **kwargs) -> Ranking:
        if self.indexed_corpus is None or self.corpus is None:
            raise ValueError("Index not built. Please call the index method first.")

        ranking_list = []
        for i, query_id in enumerate(queries):
            query_embedding = self.encode(queries[query_id], *args, **kwargs)
           
            scores = self.similarity(query_embedding, self.indexed_corpus)
            score_array = scores.cpu().numpy().flatten()

            if top_k is not None:
                top_k_indices = score_array.argsort()[-top_k:][::-1]
                top_k_scores = score_array[top_k_indices]
                top_k_doc_ids = [self.index_id_lookup[i] for i in top_k_indices]

                for j, doc_id in enumerate(top_k_doc_ids):
                    ranking_list.append([query_id, doc_id, top_k_scores[j], j])
            
            else:
                sorted_indices = score_array.argsort()[::-1]

                for j, doc_id in enumerate(sorted_indices):
                    ranking_list.append([query_id, self.index_id_lookup[doc_id], score_array[doc_id], j])
        
        ranking = Ranking(ranking_list)

        return ranking

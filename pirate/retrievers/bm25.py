import numpy as np

from rank_bm25 import (
    BM25Okapi,
    BM25L,
    BM25Plus
)
from loguru import logger
from typing import Any, Optional, Callable

from pirate.data.ranking import Ranking

from .base import BaseRetriever
from pirate.models.types import Encoder
from pirate.data import (
    Passages,
    Queries,
)

class BM25Retriever(BaseRetriever):
    def __init__(self, model: Encoder, tokenizer: Optional[Callable] = None):
        self.model_name = model
        self.model = self._get_model(model)
        self.tokenizer = tokenizer or (lambda x: x.split(" "))

        self.indexed_corpus = None
        self.corpus = None

    def _get_model(self, model: Encoder) -> Any:
        match model:
            case Encoder.BM25:
                return BM25Okapi
            case Encoder.BM25L:
                return BM25L
            case Encoder.BM25PLUS:
                return BM25Plus
            case _:
                raise ValueError("Invalid BM25 model. Must be BM25, BM25L, or BM25PLUS.")

    def index(self, corpus: Passages):
        if not isinstance(corpus, Passages):
            raise ValueError("Invalid corpus type, must be Passages or Queries.")
        
        tokenized_corpus = [self.tokenizer(corpus[doc_id]) for doc_id in corpus]
        self.index_id_lookup = {i: doc_id for i, doc_id in enumerate(corpus)}

        logger.info(f"Indexing corpus on {self.model_name}...")
        self.indexed_corpus = self.model(tokenized_corpus)
        self.corpus = corpus

        logger.info("Finished indexing corpus.")

    def rank(self, queries: Queries, top_k: Optional[int] = None) -> Ranking:
        if self.indexed_corpus is None or self.corpus is None:
            raise ValueError("Index not built. Please call the index method first.")

        tokenized_queries = [self.tokenizer(queries[query_id]) for query_id in queries]

        ranking_list = []
        for i, query_id in enumerate(queries):
            scores = self.indexed_corpus.get_scores(tokenized_queries[i])
            score_array = np.array(scores)

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

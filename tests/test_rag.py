import unittest
from unittest.mock import patch

from langchain_core.documents import Document

from helper_functions import rag
from helper_functions.rag import fuse_ranked_documents, tokenize


class HybridRetrievalTests(unittest.TestCase):
    def test_tokenize_removes_markdown_and_html_markup(self):
        self.assertEqual(
            tokenize("**<mark>GROUNDS FOR DIVORCE</mark>**"),
            ["grounds", "for", "divorce"],
        )

    def test_reciprocal_rank_fusion_promotes_shared_chunks_once(self):
        vector_shared = Document(
            page_content="shared vector chunk",
            metadata={"source": "guide.md", "chunk_index": 1},
        )
        keyword_shared = Document(
            page_content="shared keyword chunk",
            metadata={"source": "guide.md", "chunk_index": 1},
        )
        vector_only = Document(
            page_content="vector only",
            metadata={"source": "guide.md", "chunk_index": 2},
        )
        keyword_only = Document(
            page_content="keyword only",
            metadata={"source": "guide.md", "chunk_index": 3},
        )

        results = fuse_ranked_documents(
            [[vector_shared, vector_only], [keyword_shared, keyword_only]],
            k=3,
        )

        self.assertEqual(results[0][0].metadata["chunk_index"], 1)
        self.assertAlmostEqual(results[0][1], 2 / 61)
        self.assertEqual(len(results), 3)
        self.assertEqual(
            len({(doc.metadata["source"], doc.metadata["chunk_index"]) for doc, _ in results}),
            len(results),
        )

    def test_candidate_limits_come_from_config(self):
        self.assertEqual(rag.VECTOR_CANDIDATES, 10)
        self.assertEqual(rag.KEYWORD_CANDIDATES, 10)
        self.assertFalse(hasattr(rag, "MIN_RELEVANCE_SCORE"))

    def test_vector_candidates_are_not_filtered_by_relevance(self):
        document = Document(
            page_content="low-scoring vector result",
            metadata={"source": "guide.md", "chunk_index": 1},
        )

        class FakeVectorStore:
            def similarity_search_with_score(self, question, k):
                self.k = k
                return [(document, 99.0)]

            def _select_relevance_score_fn(self):
                return lambda distance: -1.0

        fake_store = FakeVectorStore()
        with (
            patch.object(rag, "build_index", return_value=(fake_store, [], None)),
            patch.object(rag, "fuse_ranked_documents", return_value=[(document, 1 / 61)]),
        ):
            results = rag.retrieve("query", k=1)

        self.assertEqual(fake_store.k, 10)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["vector_score"], -1.0)


if __name__ == "__main__":
    unittest.main()
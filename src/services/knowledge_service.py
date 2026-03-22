"""Knowledge base retrieval service using FAISS."""

import os
import pickle
from pathlib import Path
from typing import List, Optional
from loguru import logger
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.core.config import Settings


class KnowledgeService:
    """Service for RAG-based knowledge base operations using FAISS."""

    def __init__(self, settings: Settings):
        """
        Initialize knowledge service with FAISS and embeddings.

        Args:
            settings: Application settings with OpenAI API key
        """
        self.settings = settings
        self.vectorstore = None
        self.embeddings = None
        self.faiss_index_path = "./data_or_knowledge_graph/faiss_index"
        self._init_embeddings()
        self._load_or_create_vectorstore()

    def _init_embeddings(self) -> None:
        """Initialize OpenAI embeddings."""
        try:
            logger.info("Initializing OpenAI embeddings")
            self.embeddings = OpenAIEmbeddings(
                api_key=self.settings.openai_api_key,
                model="text-embedding-3-small",
            )
            logger.info("OpenAI embeddings initialized")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            self.embeddings = None

    def _load_or_create_vectorstore(self) -> None:
        """Load existing FAISS index or create empty one."""
        try:
            if os.path.exists(self.faiss_index_path) and self.embeddings:
                logger.info(f"Loading existing FAISS index from {self.faiss_index_path}")
                self.vectorstore = FAISS.load_local(
                    self.faiss_index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.info("FAISS index loaded successfully")
            else:
                logger.info("No existing FAISS index found, will create on first load")

        except Exception as e:
            logger.warning(f"Failed to load FAISS index: {e}. Will create new index.")
            self.vectorstore = None

    async def load_knowledge_base(self, path: str = None) -> None:
        """
        Load knowledge base documents into FAISS.

        Loads .txt documents from the specified path, chunks them, embeds them,
        and stores them in FAISS vector store.

        Args:
            path: Path to knowledge base documents directory.
                  Defaults to settings.knowledge_base_path
        """
        if not self.embeddings:
            logger.error("Embeddings not initialized, cannot load knowledge base")
            return

        try:
            if path is None:
                path = self.settings.knowledge_base_path

            logger.info(f"Loading knowledge base from {path}")

            # Check if path exists
            kb_path = Path(path)
            if not kb_path.exists():
                logger.warning(f"Knowledge base path does not exist: {path}")
                return

            # Load all .txt files
            documents = []
            txt_files = list(kb_path.glob("**/*.txt"))

            if not txt_files:
                logger.warning(f"No .txt files found in {path}")
                return

            logger.info(f"Found {len(txt_files)} document files")

            for txt_file in txt_files:
                try:
                    loader = TextLoader(str(txt_file))
                    docs = loader.load()
                    documents.extend(docs)
                    logger.debug(f"Loaded {txt_file.name}")
                except Exception as e:
                    logger.error(f"Failed to load {txt_file.name}: {e}")

            if not documents:
                logger.warning("No documents loaded")
                return

            logger.info(f"Loaded {len(documents)} documents total")

            # Split documents into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,  # Smaller chunks for better retrieval
                chunk_overlap=50,
                separators=["\n\n", "\n", ".", " ", ""],
            )
            chunks = splitter.split_documents(documents)

            logger.info(f"Split into {len(chunks)} chunks")

            # Create or update FAISS index
            if self.vectorstore is None:
                logger.info("Creating new FAISS index")
                self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            else:
                logger.info("Adding documents to existing FAISS index")
                self.vectorstore.add_documents(chunks)

            # Save index to disk
            self._save_vectorstore()

            logger.info(
                f"Knowledge base loaded successfully. "
                f"Total chunks: {len(chunks)}"
            )

        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")

    def _save_vectorstore(self) -> None:
        """Save FAISS index to disk."""
        try:
            if self.vectorstore:
                os.makedirs(self.faiss_index_path, exist_ok=True)
                self.vectorstore.save_local(self.faiss_index_path)
                logger.info(f"FAISS index saved to {self.faiss_index_path}")
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}")

    async def retrieve_relevant_docs(
        self, query: str, top_k: int = 5
    ) -> List[str]:
        """
        Retrieve relevant documents from the FAISS knowledge base.

        Uses similarity search to find the most relevant documents
        for the given query.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of relevant document content strings
        """
        if not self.vectorstore:
            logger.warning(
                "FAISS vectorstore not initialized. "
                "Load knowledge base first."
            )
            return []

        try:
            logger.debug(f"Searching FAISS for: {query[:100]}...")

            # Perform similarity search with score threshold
            results = self.vectorstore.similarity_search_with_score(query, k=top_k)

            # Extract page content and filter by relevance score
            doc_contents = []
            for doc, score in results:
                # FAISS returns distance, lower is better
                # Only include results with reasonable similarity
                if score < 1.5:  # Distance threshold
                    doc_contents.append(doc.page_content)
                    logger.debug(f"Retrieved chunk (distance={score:.2f}): {doc.page_content[:100]}...")

            if not doc_contents:
                logger.debug("No highly relevant documents found")
                # Return top result anyway even if less relevant
                if results:
                    doc_contents = [results[0][0].page_content]

            logger.info(f"Found {len(doc_contents)} relevant documents for query")

            return doc_contents

        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            return []

    def get_vectorstore_stats(self) -> dict:
        """Get statistics about the FAISS vectorstore."""
        if self.vectorstore:
            return {
                "initialized": True,
                "total_vectors": self.vectorstore.index.ntotal if hasattr(self.vectorstore, 'index') else 0,
                "index_path": self.faiss_index_path,
            }
        return {
            "initialized": False,
            "total_vectors": 0,
            "index_path": self.faiss_index_path,
        }

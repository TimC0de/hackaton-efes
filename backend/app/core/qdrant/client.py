import asyncio
import json
import logging
import uuid
from typing import Optional, List

import config

from qdrant_client import AsyncQdrantClient, QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

from langchain import hub
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.embeddings.base import Embeddings

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


from langchain_community.tools.vectorstore.tool import VectorStoreQATool

from langchain_core.documents import Document

from langchain_qdrant import QdrantVectorStore

from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings


logger = logging.getLogger(__name__)

qdrant_client: Optional[QdrantClient] = None
qdrant_vector_stores: dict[str, QdrantVectorStore] = {}

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

languages = [
    "RU",
    "RO",
    "EN-US"
]


async def setup():
    global qdrant_client, qdrant_vector_stores

    if not qdrant_client:
        qdrant_client = QdrantClient(config.env_param('QDRANT_URL'))
        for language in languages:
            if not qdrant_client.collection_exists(f'{config.env_param('QDRANT_COLLECTION')}_{language}'):
                qdrant_client.create_collection(
                    collection_name=f'{config.env_param('QDRANT_COLLECTION')}_{language}',
                    vectors_config=VectorParams(
                        size=1024,  # Dimension of the vectors (e.g., 384 for embeddings)
                        distance="Cosine"  # Distance metric: "Cosine", "Euclid", or "Dot"
                    )
                )

        mistral_api_key = "xaUiT1ULmKqgJmO5XtcE7hSowfATiToA"
        mistral_embeddings_model = MistralAIEmbeddings(
            model="mistral-embed",
            api_key=mistral_api_key
        )

        for language in languages:
            qdrant_vector_stores[language] = QdrantVectorStore(
                client=qdrant_client,
                collection_name=f'{config.env_param('QDRANT_COLLECTION')}_{language}',
                embedding=mistral_embeddings_model,
            )
            await asyncio.sleep(1.5)


async def insert(vector_representation: str, data: dict) -> uuid.UUID:
    # logger.info(vector_representation)
    # vector = model.encode(vector_representation).tolist()
    #
    # # Insert the CV into Qdrant
    # id = uuid.uuid4()
    # point = PointStruct(
    #     id=str(id),  # Let Qdrant auto-generate an ID for this point
    #     vector=vector,
    #     payload={
    #         'page_content': json.dumps(data),
    #     }  # Add the CV data as a payload
    # )
    #
    # await qdrant_async_client.upsert(
    #     collection_name=config.env_param('QDRANT_COLLECTION'),
    #     points=[point]
    # )

    document = Document(
        page_content=vector_representation,
        metadata=data
    )
    qdrant_vector_stores[data['lang']].add_documents(documents=[document], ids=[data['id']])
    await asyncio.sleep(1.5)


async def search(language: str, query: str):
    response = qdrant_vector_stores[language].similarity_search_with_score(query)
    return response
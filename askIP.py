from langchain.embeddings import SentenceTransformerEmbeddings

emb_func = SentenceTransformerEmbeddings(model_name="embaas/sentence-transformers-multilingual-e5-base")

from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

model_id = "sdaia/allam-1-13b-instruct"

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 200
}

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials

credentials = Credentials(
                   url = "https://eu-de.ml.cloud.ibm.com",
                   api_key = 'Qp_xZRfMnSnXNEd51OywtfFNxiZaVvjtIpvUbE8FGLRY'
                  )

client = APIClient(credentials)

from ibm_watsonx_ai.foundation_models import Model
project_id="f5266780-6418-4e00-9410-950393001fe6"
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

esuser = '3206420058'
espassword = ''
eshost = "https://my-elasticsearch-project-bbf7a2.es.us-east-1.aws.elastic.cloud.es.io"
esport = '443'
esapi = 'RTNwVkI1TUJkUmNYWGszLVdtS3Q6RkVUR25naGlUV3EtN1JWRk9KUGJfUQ=='

from elasticsearch import Elasticsearch

# Client initialization
elastic_client = Elasticsearch(
    cloud_id="63854a0340804f9a91dd5683744082a7:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQxNGRiN2U3Y2QyYzU0NjllYmQwN2Q0M2M4ZGQ5ZjI3MCQ2NjljMDFiNGE3YzU0N2UwODRlODQzNGJhODUxMjZiZg==",
    api_key="RTNwVkI1TUJkUmNYWGszLVdtS3Q6RkVUR25naGlUV3EtN1JWRk9KUGJfUQ=="
)

elastic_client

index_name = "ip_index"
# Refresh the Elasticsearch index to ensure updated data is available
elastic_client.indices.refresh(index=index_name)

# User enters a question
user_question = input("Please enter your question related to intellectual property law in Saudi Arabia:\n")

# Embed the user's question and perform the search in Elasticsearch
embedded_question = emb_func.embed_query(user_question)
relevant_context = elastic_client.search(
    index=index_name,
    knn={
        "field": "embedding",
        "query_vector": embedded_question,
        "k": 4,
        "num_candidates": 50,
    },
    _source=["text"],
    size=5
)

# Extract relevant text sections from the search results
hits = [hit for hit in relevant_context["hits"]["hits"]]
context = "\n\n\n".join(
    [sub_text if isinstance(sub_text, str) else " ".join(sub_text) 
     for rel_ctx in hits for sub_text in ([rel_ctx["_source"]['text']] 
     if isinstance(rel_ctx["_source"]['text'], str) else rel_ctx["_source"]['text'])]
)

# Create a prompt based on the relevant context and user question
def make_prompt(context, question_text):
    return (f"Act as an excellent Intellectual Property Specialist lawyer in Saudi Arabia and answer the following based on the context:\n"
          + f"{context}:\n\n"
          + f"{question_text}")

prompt_text = make_prompt(context, user_question)

# Generate the answer using the model
generated_answer = model.generate_text(prompt_text)

# Print the response to the user
print("\nAnswer:")
print(generated_answer)

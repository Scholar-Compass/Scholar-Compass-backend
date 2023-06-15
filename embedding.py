import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION')

# calculate embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request


def embed(text, store_path):
    embeddings = []
    for batch_start in range(0, len(text), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = text[batch_start:batch_end]
        response = openai.Embedding.create(model = EMBEDDING_MODEL, input = list(batch.values))
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({"text": text, "embedding": embeddings})
    df.to_csv(store_path, index=False)


if __name__ == "__main__":
    for f in os.listdir("csv_to_embed"):
        text = pd.read_csv("csv_to_embed/" + f).apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
        embed(text, "embedding/" + f)

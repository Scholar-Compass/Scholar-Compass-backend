import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

data = pd.read_csv("北科.csv")
# merge title, heading, content
data_strings = data["title"] + " " + data["heading"] + " " + data["content"]
data_strings = data_strings.tolist()

# calculate embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

embeddings = []
for batch_start in range(0, len(data_strings), BATCH_SIZE):
    batch_end = batch_start + BATCH_SIZE
    batch = data_strings[batch_start:batch_end]
    print(f"Batch {batch_start} to {batch_end - 1}")
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
    for i, be in enumerate(response["data"]):
        assert i == be["index"]  # double check embeddings are in same order as input
    batch_embeddings = [e["embedding"] for e in response["data"]]
    embeddings.extend(batch_embeddings)

df = pd.DataFrame({"text": data_strings, "embedding": embeddings})

# save document chunks and embeddings
SAVE_PATH = "data/北科.csv"
df.to_csv(SAVE_PATH, index=False)

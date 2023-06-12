import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv('OPENAI_ORGANIZATION')

# calculate embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

files = os.listdir("csv")

for csv_file in files:
    print(csv_file)
    df = pd.read_csv("csv/" + csv_file)
    merged_content = df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    embeddings = []
    for batch_start in range(0, len(merged_content), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = merged_content[batch_start:batch_end]
        # print(list(batch.values))

        # print(f"Batch {batch_start} to {batch_end - 1}")
        response = openai.Embedding.create(model = EMBEDDING_MODEL, input = list(batch.values))
        # print(response)
        # for i, be in enumerate(response["data"]):
        #     assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    df = pd.DataFrame({"text": merged_content, "embedding": embeddings})

    df.to_csv("embedding/" + csv_file, encoding='utf-8', index=False)

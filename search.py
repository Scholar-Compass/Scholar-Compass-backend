# imports
import ast  # for converting embeddings saved as strings back to arrays
import os
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION')

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

all_df = []
for csv in os.listdir("embedding"):
    all_df.append(pd.read_csv("embedding/" + csv))
df = pd.concat(all_df)

# convert embeddings from CSV str type back to list type
df['embedding'] = df['embedding'].apply(ast.literal_eval)

links_df = pd.read_csv("csv_other/links.csv")

# search function
def strings_ranked_by_relatedness(
        query: str,
        df: pd.DataFrame,
        relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
        top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
        query: str,
        df: pd.DataFrame,
        model: str,
        token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    paragraph, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = "根据以下提供的“大学信息”作为资料进行回答。如果你不知道答案，就说“我不知道”，不要擅自进行回答。问题在最后。"
    question = f"\n\n问题: {query}"
    message = introduction
    for para in paragraph:
        next_article = f'\n\n大学信息:\n"""\n{para}\n"""'
        if num_tokens(message + next_article + question, model=model) > token_budget:
            break
        else:
            message += next_article
    return message + question


def ask(
        query: str,
        df: pd.DataFrame = df,
        model: str = GPT_MODEL,
        token_budget: int = 4096 - 500,
        print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "回答关于大学校园或专业的问题。"},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message


def add_link(paragraph):
    all_links = []
    for i, row in links_df.iterrows():
        if row["university"] in paragraph:
            all_links.append((row["university"], row["link"]))
    if 0 < len(all_links) and len(all_links) < 5:
        paragraph += "\n\n相关文档："
        for uni, link in all_links:
            paragraph += f"\n{uni}: {link}"
    return paragraph


if __name__ == "__main__":
    q = "北理工学习氛围怎么样"
    res = ask(q)
    # print(res)
    res = add_link(res)
    print(res)

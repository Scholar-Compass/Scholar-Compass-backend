import re
import pandas as pd
import os

def insert(df, row): 
    if row[4].replace(" ", "") != "":
        row[4] = re.sub(" +", " ", row[4])
        df = pd.concat([df, pd.DataFrame([row], columns=df.columns)], ignore_index=True)
        row[4] = ""
    return df

def process_md(file_path, store_path, links = None, uni_md = True):
    # print(file_path)
    f = open(file_path, "r", encoding="utf-8")
    row = [""] * 5
    df = pd.DataFrame(columns=["H1", "H2", "H3", "H4", "paragraph"])

    while True:
        line = f.readline()
        if line == "":
            df = insert(df, row)
            break
        line = re.sub(" +", " ", line.replace("\n", " "))
        # print(line)
        line_split = line.split(" ")
        if line_split[0] == "#":
            df = insert(df, row)
            row[0] = line_split[1]
        elif line_split[0] == "##":
            df = insert(df, row)
            row[1] = line_split[1]
        elif line_split[0] == "###":
            df = insert(df, row)
            row[2] = line_split[1]
        elif line_split[0] == "####":
            df = insert(df, row)
            row[3] = line_split[1]
        else:
            row[4] += line

    if uni_md and "https" in df.loc[0]["paragraph"]:
        uni = file_path.split("/")[-1].split(".")[0]
        links[uni] = df.loc[0]["paragraph"]
        df = df.drop([0])
    df.to_csv(store_path, index=False)


if __name__ == "__main__":
    links = {}
    for f in os.listdir("md_uni"):
        process_md("md_uni/" + f, "csv_to_embed/" + f.replace(".md", ".csv"), links)

    links_df = pd.Series(links).reset_index()
    links_df.columns = ["university", "links"]
    links_df.to_csv("csv_other/links.csv", index=False)
    
    for f in os.listdir("md_other"):
        process_md("md_other/" + f, "csv_to_embed/" + f.replace(".md", ".csv"), uni_md=False)

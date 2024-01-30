import re
import pandas as pd
import os


def insert(df, row):
    if row[4].replace(" ", "") != "":
        row[4] = re.sub(" +", " ", row[4])
        df = pd.concat([df, pd.DataFrame([row], columns=df.columns)], ignore_index=True)
        row[4] = ""
    return df


def process_md(file_path, store_path, links=None, uni_md=True):
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
            row = [""] * 5
            row[0] = " ".join(line_split[1:])
        elif line_split[0] == "##":
            df = insert(df, row)
            row[1] = " ".join(line_split[1:])
            row[2], row[3], row[4] = "", "", ""
        elif line_split[0] == "###":
            df = insert(df, row)
            row[2] = " ".join(line_split[1:])
            row[3], row[4] = "", ""
        elif line_split[0] == "####":
            df = insert(df, row)
            row[3] = " ".join(line_split[1:])
            row[4] = ""
        else:
            row[4] += line

    if uni_md and "https" in df.loc[0]["paragraph"]:
        link = df.loc[0]["paragraph"].replace(" ", "")
        uni_alias = df.loc[1]["H1"].replace(" ", "").split("/")
        for nickname in uni_alias:
            links[nickname] = link
        df = df.drop([0])
    df.to_csv(store_path, index=False)


if __name__ == "__main__":
    links = {}
    for f in os.listdir("md_uni"):
        process_md("md_uni/" + f, "csv_to_embed/" + f.replace(".md", ".csv"), links)

    links_df = pd.Series(links).reset_index()
    links_df.columns = ["university", "link"]
    links_df.to_csv("csv_other/links.csv", index=False)

    for f in os.listdir("md_other"):
        process_md(
            "md_other/" + f, "csv_to_embed/" + f.replace(".md", ".csv"), uni_md=False
        )

import re
import pandas as pd
from os import listdir

def insert(df, row): 
    if row[4].replace(" ", "") != "":
        row[4] = re.sub(" +", " ", row[4])
        df = pd.concat([df, pd.DataFrame([row], columns=df.columns)], ignore_index=True)
        row[4] = ""
    return df


files = listdir("md")

for md_file in files:
    f = open("md/" + md_file, "r", encoding="utf-8")
    row = [""] * 5
    para = ""
    df = pd.DataFrame(columns=["H1", "H2", "H3", "H4", "paragraph"])

    while True:
        line = f.readline().replace("\n", " ")
        line = re.sub(" +", " ", line)
        if line == "":
            break
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
    
    # print(df)
    csv_file = md_file.replace(".md", ".csv")
    df.to_csv("csv/" + csv_file, encoding='utf-8', index=False)

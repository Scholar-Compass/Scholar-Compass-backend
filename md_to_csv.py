import re
import pandas as pd

def insert(df, row):
    
    if row[4].replace(" ", "") != "":
        df = pd.concat([df, pd.DataFrame([row], columns=df.columns)], ignore_index=True)
        row[4] = ""
    return df

s = "北京大学.md              上海财经大学.md          中央财经大学.md          北京科技大学.md          北京外国语大学.md 上海交通大学.md          中国传媒大学.md          北京师范大学.md          中国科学院大学.md        北京大学医学部.md"
s = re.sub(" +", " ", s)
files = s.split(" ")

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

import os

import pandas as pd

all_df = []
for csv in os.listdir("embedding"):
    all_df.append(pd.read_csv("embedding/" + csv))
df = pd.concat(all_df)
print(df)

for i in df["text"]:
    print(i[:50])

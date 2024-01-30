# Scholar Compass' Backend

## 流程

### 准备数据

```mermaid
flowchart TB
飞书[飞书<br>各校文档] -->|导出| Word -->|转换| md_uni/*.md
飞书 -->|开头加链接| md_uni/*.md
人工 --> md_other/常见问题汇总.md
Markdown ==>|<code>md_to_csv.py</code><br>转换格式| CSV

md_uni/*.md -.-> csv_to_embed/*.csv
md_other/常见问题汇总.md -.-> csv_to_embed/*.csv
md_uni/*.md -.-> csv_other/links.csv

subgraph Markdown
    direction TB
    md_uni/*.md
    md_other/常见问题汇总.md
end

subgraph CSV
    direction TB
    csv_other/links.csv[csv_other/links.csv<br>各校文档的链接]
    csv_to_embed/*.csv[csv_to_embed/*.csv<br>每一节对应的各级标题和学校]
end

csv_to_embed/*.csv ==>|<code>embedding.py</code><br>via OpenAI API| embedding/*.csv[embedding/*.csv<br>text + embedding]

csv_other/links.csv  --> 后续
embedding/*.csv  --> 后续([后续使用])
```

另外，用`read_csv.py`可检视生成的`embedding/*.csv`。

### 后端

```mermaid
flowchart LR
前端 -->|"POST <code>/query</code><br><code>{ question: string }</code>"| api.py[<code>api.py</code><br>Flask]
api.py -->|"<code>{ answer: string }</code>"| 前端
api.py <-->|<code>search.py</code>| OpenAI[OpenAI API]
```

`search.py`从 OpenAI 生成答案步骤如下。

1. `ask()`

   > [!WARNING]
   >
   > `ask()`的`history`参数似乎实际未使用。

   1. `query_message()`
      1. `strings_ranked_by_relatedness()`根据输入的问题，利用`openai.Embedding`选出相关学校。
      2. 在问题之前补充“大学信息”等提示。

   2. 向`openai.ChatCompletion`提问并返回答案。

   > [!WARNING]
   >
   > [`983d474`](https://github.com/Scholar-Compass/Scholar-Compass-backend/commit/983d4747810aa3e0b64295499f6c9df4622b494b)给每次提问强行加了“MUST ANSWER IN ENGLISH”，恐怕需要回退。

2. `add_link()`

   用`csv_other/links.csv`匹配校名，添加相应链接。

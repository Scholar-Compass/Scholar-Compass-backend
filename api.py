import json
import search
from flask import Flask, request, jsonify, Response
import ast

app = Flask(__name__)

# app.config['JSON_AS_ASCII'] = False

@app.route('/query', methods = ['POST'])
def query():
    data = ast.literal_eval(request.data.decode("utf-8"))
    question = data["question"]
    # question = request.form["question"]
    ans = search.ask(question)
    data = {"answer" : ans}
    json_string = json.dumps(data, ensure_ascii = False)
    # print(json_string)
    # creating a Response object to set the content type and the encoding
    response = Response(json_string, content_type="application/json; charset=utf-8")
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response, response.data)
    return response
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug = True)

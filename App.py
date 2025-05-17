# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Selamın aleyküm ve rahmetullah.<br>Ve aleyna aleyküm es selam."

if __name__ == '__main__':
    app.run(debug=True)





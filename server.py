from flask import Flask, request, json

app = Flask(__name__)


@app.route('/hello')
def say_hello():
    html = "<html><body>Hello</body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True)

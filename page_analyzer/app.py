from flask import Flask, render_template
from page_analyzer.config import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World! This Flask app is running inside a Docker container."


if __name__ == "__main__":
    # 0.0.0.0 makes the app reachable from outside the container,
    # so the -p 5000:5000 port binding works.
    app.run(host="0.0.0.0", port=5000)

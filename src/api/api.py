
from flask import Flask
from functools import partial
import os

# https://gist.github.com/Peppermint777/c8465f9ce8b579a8ca3e78845309b832

app = Flask(__name__)
port = int(os.environ.get("PORT", 3000))


@app.route('/')
def hello():
    return "Hello World !"


partial_run = partial(app.run, host="0.0.0.0", port=port, debug=False, use_reloader=False)

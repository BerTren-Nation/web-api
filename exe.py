import string
import random
from flask import Flask, jsonify, request
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = Flask(__name__)
client = FaunaClient(secret="fnAECDM_y6ACB0IddJ-dSMwtXAEuZP7AaaQrs8nz")


def generate_identifier(n=6):
    identifier = ""
    for i in range(n):
        identifier += random.choice(string.ascii_letters)
    return identifier


@app.route("/")
def home():
    return "Hello World!"


@app.route("/generate/<path:address>/")
def generate(address):
    identifier = generate_identifier()
    client.query(q.create(q.collection("urls"), {
        "data": {
            "identifier": identifier,
            "url": address
        }
    }))

    shortened_url = request.host_url + identifier
    return jsonify({"identifier": identifier, "shortened_url": shortened_url})

@app.route("/<string:identifier>/")
def fetch_original(identifier):
    try:
        url = client.query(q.get(q.match(q.index("Neko"), identifier)))
    except:
        abort(404)

    return redirect(url_for(url["data"]["url"]))

if __name__ == "__main__":
    app.run(debug=True)

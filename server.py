from algorithm.report import Report
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from urllib.parse import urlparse

import redis
import json
import pickle
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
url = urlparse(os.environ.get('REDISTOGO_URL', 'localhost'))
db = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)

@app.route('/load/<token>', methods = ['POST'])
@cross_origin()
def load_csv(token):
    init = request.get_json()
    r = Report(init['csv'], init['boy'])
    db.set(token, pickle.dumps(r))
    r = pickle.loads(db.get(token))

    return json.dumps({ "stocks": r.stocks() });


@app.route('/txin/<token>', methods = ['POST'])
@cross_origin()
def load_txin(token):
    r = pickle.loads(db.get(token))
    txns = request.get_json()['txin']
    r.reset()
    to_reval = r.run(txns)
    db.set(token, pickle.dumps(r))

    return json.dumps({ "to_reval": to_reval })


@app.route('/reval/<token>', methods = ['POST'])
@cross_origin()
def reval(token):
    r = pickle.loads(db.get(token))
    data = request.get_json()['reval']
    result = r.reval(data)

    return json.dumps({ "result": result })



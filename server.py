from algorithm.report import Report
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import redis
import json
import pickle
import os

app = Flask(__name__)
print(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = redis.Redis(os.environ['REDISTOGO_URL'])

@app.route('/load/<token>', methods = ['POST'])
@cross_origin()
def load_csv(token):
    init = request.get_json()
    print(init)
    r = Report(init['csv'], init['boy'])
    db.set(token, pickle.dumps(r))
    r = pickle.loads(db.get(token))
    print(dir(r))

    return json.dumps({ "stocks": r.stocks() });


@app.route('/txin/<token>', methods = ['POST'])
@cross_origin()
def load_txin(token):
    r = pickle.loads(db.get(token))
    print(dir(r))
    txns = request.get_json()['txin']
    print(txns)
    r.reset()
    to_reval = r.run(txns)

    db.set(token, pickle.dumps(r))

    return json.dumps({ "to_reval": to_reval })


@app.route('/reval/<token>', methods = ['POST'])
@cross_origin()
def reval(token):
    r = pickle.loads(db.get(token))
    print(request.get_json())
    data = request.get_json()['reval']
    result = r.reval(data)

    return json.dumps({ "result": result })



from algorithm.report import Report
from flask import Flask
from flask import request

import redis
import json
import pickle

app = Flask(__name__)
db = redis.Redis('localhost')

@app.route('/load/<token>', methods = ['POST'])
def load_csv(token):
    data = json.dumps(request.form)
    db.getset(token, data)

    return db.get(token)


@app.route('/txin/<token>', methods = ['POST'])
def load_txin(token):
    init = json.loads(db.get(token))
    txns = request.get_json()['txin']

    r = Report(init['csv'], init['boy'])
    to_reval = r.run(txns)

    db.set(token, pickle.dumps(r))

    return json.dumps({"to_reval": to_reval})


@app.route('/reval/<token>', methods = ['POST'])
def reval(token):
    r = pickle.loads(db.get(token))
    data = request.get_json()['reval']
    result = r.reval(data)

    return json.dumps({"result": result})



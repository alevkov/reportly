from algorithm.report import Report
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import redis
import json
import pickle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = redis.Redis('localhost')

@app.route('/load/<token>', methods = ['POST'])
@cross_origin()
def load_csv(token):
    init = request.get_json()
    r = Report(init['csv'], init['boy'])
    
    db.set(token, pickle.dumps(r))

    return json.dumps({ "stocks": r.stocks() });


@app.route('/txin/<token>', methods = ['POST'])
@cross_origin()
def load_txin(token):
    r = pickle.loads(db.get(token))
    txns = request.get_json()['txin']
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



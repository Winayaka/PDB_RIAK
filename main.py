from flask import Flask, render_template, session, request, jsonify
from datetime import datetime
import riak

client = riak.RiakClient(protocol='http', http_port=8098)
client = riak.RiakClient(nodes=[
    {'host':'172.20.0.2','http_port':8098},
    {'host':'172.20.0.3','http_port':8098},
    {'host':'172.20.0.4','http_port':8098},
    {'host':'172.20.0.5','http_port':8098},
    {'host':'172.20.0.6','http_port':8098}
    ])
client = riak.RiakClient(protocol='http', nodes=[riak.RiakNode()])

user_bucket = client.bucket('user')

app = Flask(__name__)
'''
 1. buat session bucker
 2. buat htmlnya
'''

@app.route('/')
def index():
    session['last_visit'] = datetime.now()
    return render_template('login.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/api/login/', methods=['POST'])
def loginAPI():
    if request.method == 'POST':
        user = user_bucket.get(request.json['username'])
        if user.data['password'] == request.json['password']:
                flask.session['uid'] = uuid.uuid4()
                result = {'status': 'success'}
        else:
            result = {'status': 'fail'}
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    return render_template('register.html')

@app.route('/api/register/', methods=['GET','POST'])
def registerAPI():
    if request.method == 'POST':
        new_user = user_bucket.new(request.json['username'], data={
            'name': request.json['name'],
            'password': request.json['password'],
            'order': [],
        })        
        new_user.store()
        result = {'status': 'success'}
        return jsonify(result)


@app.route('/sale')
def sale():
    return render_template('sale.html')

#get untuk ambil barang, post untuk borong barang
@app.route('/api/sale', methods=['POST'])
def saleAPI():
    if request.mehtod == 'GET':
        pass
    elif request.meth == 'POST':
        user = user_bucket.get(request.json['username'])
        user.data['order'].push(request.json['order'])



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='127.1.0.0', port='7000') # runs on machine ip address to make it visible on netowrk


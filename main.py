from flask import Flask, render_template, session, request, jsonify
from datetime import datetime
import json
import riak

client = riak.RiakClient(protocol='http', http_port=8098)
client = riak.RiakClient(nodes=[
    {'host': '172.20.0.2', 'http_port': 8098},
    {'host': '172.20.0.3', 'http_port': 8098},
    {'host': '172.20.0.4', 'http_port': 8098},
    {'host': '172.20.0.5', 'http_port': 8098},
    {'host': '172.20.0.6', 'http_port': 8098}
])
client = riak.RiakClient(protocol='http', nodes=[riak.RiakNode()])

user_bucket = client.bucket('user')
session_bucket = client.bucket('session')
item_bucket = client.bucket('item')
order_bucket = client.bucket('oreder')

app = Flask(__name__)

'''
 1. buat session bucker
 2. buat barang bucket
 3. buat htmlnya
'''


@app.route('/home')
def index():
    session['last_visit'] = datetime.now()
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/api/login/', methods=['POST'])
def loginAPI():
    if request.method == 'POST':
        user = user_bucket.get(request.json['username'])
        if user.data['password'] == request.json['password']:
            result = {'status': 'success'}
            session['key'] = 'value'
            data_session = json.dumps({
                'username': request.json['username'],
                'session_id': session.get('key'),
                'last_login': datetime.now(),
                'last_order': ''
            }, indent=4, sort_keys=True, default=str)
            new_session = session_bucket.new(
                request.json['username'], data=data_session
            )
            new_session.store()
            print(session.get('key'))
        else:
            result = {'status': 'fail'}
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    return render_template('register.html')


@app.route('/api/register/', methods=['GET', 'POST'])
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
    if request.method == 'GET':
        return jsonify(item_bucket.get('kipas_angin').data)

# get untuk ambil barang, post untuk borong barang
@app.route('/api/sale', methods=['GET', 'POST'])
def saleAPI():
    if request.method == 'GET':
        print(item_bucket.data)
        return jsonify(item_bucket.data)
    elif request.meth == 'POST':
        user = user_bucket.get(request.json['username'])
        user.data['order'].push(request.json['order'])


@app.route('/api/user/<username>', methods=['POST'])
def userAPI(username):
    if request.method == 'GET':
        return jsonify(user_bucket.get(request.json['username']))


@app.route('/api/session/<username>', methods=['GET'])
def sessionAPI(username):
    if request.method == 'GET':
        return jsonify(session_bucket.get(username).data)


# @api.route('/api/item', methods=['GET'])
# def itemAPI():
#     if request.method == 'GET':
#         return jsonify(item_bucket.get('kipas_angin').data)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    # runs on machine ip address to make it visible on netowrk
    item = item_bucket.new('kipas_angin', data={
        'item_name': 'Kipas Angin',
        'brand': 'Cosmos Wadesdes',
        'quantity': 15000,
        'price': '$80'
    })
    item.store()
    app.run(host='127.1.0.0', port='7001')

import os
import requests
import sqlalchemy
from werkzeug.datastructures import Authorization
import models
import jwt
import bcrypt



from flask_cors import CORS

from dotenv import load_dotenv
from flask import Flask, request,jsonify


app = Flask(__name__)
CORS(app)

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL').replace('postgres','postgresql')
models.db.init_app(app)

crypto_api = "https://api.coinranking.com/v2/coins?limit=100"
api_key = os.environ.get("crypto_api")



@app.route('/', methods=["GET"])
def root():
    return {"message":'helllo world'}

@app.route('/user/login', methods=["POST"])
def login():
    user = models.User.query.filter_by(email = request.json['email']).first()
    
    if user.password == request.json['password']:
        return{"user":user.to_json()}
        
    else:
        return{'message':'login failed'},401



@app.route('/user/signup',methods=["POST"])
def sign_up():
    try:
        user = models.User(
            name=request.json['name'],
            email = request.json['email'],
            password = request.json['password']
            
        )
        models.db.session.add(user)
        models.db.session.commit()
        return{"message":'welcome new user', "user": user.to_json()}
    
    except sqlalchemy.exc.IntegrityError as e:
        print (e)
        return{"message":'can not signup'},401




@app.route('/user/verify',methods=["GET"])
def verify():
        user = models.User.query.filter_by(id=request.headers["Authorization"]).first()
        print(request.headers)
        if user:
            return{"user":user.to_json()}
        else:
            return{"message":'user not found'},404
    
@app.route('/user',methods=["GET", 'POST', 'DELETE'])
def user_info():
        
    if request.method == 'GET':
        try:
            user = models.User.query.filter_by(id=request.headers["Authorization"]).first()
            print(request.headers)
            if user:
                return {"user":user.to_json()}
        except sqlalchemy.exc.IntegrityError:
            return{'message':'can not find user'},404
        
    elif request.method == 'POST':
        try:
            user= models.User.query.filter_by(id=request.headers["Authorization"]).first()
            if user:
                user.name = request.json['name']
                user.email = request.json['email']
                user.password = request.json['password']
                models.db.session.commit()
                return {"user":user.to_json()}
        except sqlalchemy.exc.IntegrityError:
            return{'message':'can not update user'},404


@app.route('/stocks',methods=["GET"])

def stocks():
    try:
        response = requests.get(f'https://api.coinranking.com/v2/coins?limit=100').json()
        if response:
            return{"message": response}
    except sqlalchemy.exc.IntegrityError:
        return{'message':'can not find crypto'}
        


@app.route('/stock',methods=["GET"])
def stock():
    try:
        query = request.args.get('query')

        response = requests.get(f'https://api.coinranking.com/v2/search-suggestions?query={query}').json()   

        if response:
            return{'message':"one stock", "result":response["data"]["coins"]}
        else:
            return{"message": 'can not find data'},400
        
    except sqlalchemy.exc.IntegrityError:
        return{"message":'can not find coin'}



@app.route('/stock/info/',methods=["POST"])
def stock_info():
    try:
        query = request.args.get('query')
        print(query)

        response = requests.get(f'https://api.coinranking.com/v2/coin/{query}').json()   

        if response:
            return{'message':"one stock", "result":response}
        else:
            return{"message": 'can not find data'},400
        
    except sqlalchemy.exc.IntegrityError:
        return{"message":'can not find info'}


        





@app.route('/stock/history',methods=["GET"])
def stock_history():
    try:
        time = request.args.get('time')
        query = request.args.get('query')
        response = requests.get(f'https://api.coinranking.com/v2/coin/{query}/history?timePeriod={time}').json()   

        if response:
            return{'message':"one stock", "result":response}
        else:
            return{"message": 'can not find data'},400
        
    except sqlalchemy.exc.IntegrityError:
        return{"message":'can not find con'}


@app.route('/stock/save', methods=['POST'])
def stock_save():
    try:
        user =  models.User.query.filter_by(email= request.json['email']).first()
        watchlist = models.Watchlist(
             user_id = user.id,
             crypto_id = request.json['uuid'],
             name = request.json['name']
        )
        models.db.session.add(watchlist)
        models.db.session.commit()
        return{"message":'watchlist has been added', "watchlist": watchlist.to_json()}
    except sqlalchemy.exc.IntegrityError:
        return{"message":'can not save'}

@app.route("/stock/watchlist", methods=['GET'])
def watch_list():
    try:
        print(request.headers["Authorization"])
        watchlist=models.Watchlist.query.filter_by(user_id=request.headers["Authorization"]).all()
        print(watchlist)
        return{"message":'watchlist has been added', "watchlist": [w.to_json() for w in watchlist] }
    except sqlalchemy.exc.IntegrityError:
        return{"message":'can not get to watchlist'}





@app.after_request
def set_cors_headers(response):
    response.headers.add("Access-Control-Allow-Headers", 'Content-Type, Authorization')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", 'POST,GET,PUT,DELETE,OPTIONS')
    
    return response
# cors alternative 




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
import os
import requests
import sqlalchemy
import models
import jwt
import bcrypt

from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request,jsonify

from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt= Bcrypt(app)


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
    try:
        user = models.User.query.filter_by(email = request.json['email']).first()
        if bcrypt.check_password_hash(user.password,request.json['password']):
            encrypted_id = jwt.encode({'user_id':user.id},os.environ.get('JWT_SECRET'),algorithm="HS256")
            return{"user":user.to_json(),'user_id':encrypted_id}

    except:
        print('login failed')
        return{'message':'Unable to find Username/Email'},401

    finally:
        print('user loging route is active')
            
    


@app.route('/user/signup',methods=["POST"])
def sign_up():
    try:
        pw_hash = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        user = models.User(
            name=request.json['name'],
            email = request.json['email'],
            password = pw_hash
        )
        models.db.session.add(user)
        models.db.session.commit()

        encrypted_id = jwt.encode({'user_id':user.id},os.environ.get('JWT_SECRET'),algorithm='HS256')
        print('user has been created')
        return{"message":'welcome new user', "user": user.to_json(),"user_id":encrypted_id}
    
    except:
        print ('signup failed')
        return{"message":'This email has already been used.'},401
    
    finally:
        print('user signup route is active')
            
    

@app.route('/user/verify',methods=["GET"])
def verify():
        try:
            decrypted_id = jwt.decode(request.headers["Authorization"],os.environ.get("JWT_SECRET"),algorithms=['HS256'])["user_id"]
            user = models.User.query.filter_by(id=decrypted_id).first()
            print(request.headers)
            if user:
                return{"message":"user has been verified","user": user.to_json()}
        except:
            print('verification failed')
            return{"message":'user not found'},404
        finally:
            print("user verify route is active" )

    
@app.route('/user',methods=["GET", 'POST'])
def user_info():
        
    if request.method == 'GET':
        try:
            user = models.User.query.filter_by(id=request.headers["Authorization"]).first()
            print(request.headers)
            if user:
                print('here is a list of users')
                return {"user":user.to_json()}
        except sqlalchemy.exc.IntegrityError:
            print('can not find any user')
            return{'message':'can not find user'},404
        finally:
            print('user "get" route is active')
        
    elif request.method == 'POST':
        try:
            user= models.User.query.filter_by(id=request.headers["Authorization"]).first()
            if user:
                user.name = request.json['name']
                user.email = request.json['email']
                user.password = request.json['password']
                models.db.session.commit()
                print('user information has been updated')
                return {"user":user.to_json()}
            
        except sqlalchemy.exc.IntegrityError:
            print('can not update existing user')
            return{'message':'can not update user'},404
        
        finally:
            print('user post route is active')
        
        
                    
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
            print('single crypto history has been located')
            return{'message':"one stock", "result":response}
        else:
            print("unable to locate crypto's history")
            return{"message": 'can not find data'},400
        
    except sqlalchemy.exc.IntegrityError:
        print("crypto's uuid is not a match")
        return{"message":'can not find data'},400
    finally:
        print('locating crypto history is working')


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
        print('crypto has been added')
        return{"message":'watchlist has been added', "watchlist": watchlist.to_json()}
    except sqlalchemy.exc.IntegrityError:
        print('unable to add crypto')
        return{"message":'can not save'}
    finally:
        print('stock save route is active')


@app.route("/stock/watchlist", methods=['GET'])
def watch_list():
    try:
        # print(request.headers["Authorization"])
        watchlist=models.Watchlist.query.filter_by(user_id=request.headers["Authorization"]).all()
        # print(watchlist)
        print('user watchlist has been found')
        return{"message":'watchlist has been added', "watchlist": [w.to_json() for w in watchlist] }
    except sqlalchemy.exc.IntegrityError:
        print("unable to find user watchlist")
        return{"message":'can not get to watchlist'}
    finally:
        print('user watch list route is active')





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
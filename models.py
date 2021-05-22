from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'balance':self.balance
        }


class Crypto(db.Model):
    __tablename__ ='crypto'

    id = db.Column(db.Integer,primary_key=True)
    crypto_code = db.Column(db.String)

    def to_json(self):
        return{
            'id': self.id,
            "crypto_code" :self.crypto_code
        }


class User_crypto(db.Model):
    __tablename__ = 'user_crypto'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    

    def to_json(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'user_id':self.user_id,
            'amount':self.amount
        }
   

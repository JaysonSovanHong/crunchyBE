from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)


    cryptos = db.relationship('Crypto', secondary='watchlist', backref='users')
 

    def to_json(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email
            
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

    # users = db.relationship('User', secondary='watchlist', backref='crypto')


class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    crypto_id = db.Column(db.String, db.ForeignKey('crypto.id'))
    name = db.Column(db.String)
   
    

    def to_json(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'crypto_id':self.crypto_id,
            'name':self.name
        }
   

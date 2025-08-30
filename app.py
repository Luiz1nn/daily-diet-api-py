from flask import Flask
from database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@127.0.0.1:3306/daily-diet-db'

db.init_app(app)

if __name__ == '__main__':
  app.run(debug=True)
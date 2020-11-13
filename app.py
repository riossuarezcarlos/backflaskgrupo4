from flask import Flask
from flask_restful import Api

from base_datos import db

from models.label import LabelModel

from controllers.label import LabelController,LabelsController


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/tiendavirtual';

api = Api(app=app)

@app.before_first_request
def iniciador():
    db.init_app(app)
    # db.drop_all()
    db.create_all(app=app)
    

@app.route('/')
def inicio():
    return 'Api Tienda Virtual - 200', 200


#Creacion de rutas

api.add_resource(LabelsController, '/label')
api.add_resource(LabelController, '/label/<int:labelId>')

if __name__ == '__main__':
    app.run(debug=True)


import firebase_admin
from firebase_admin import credentials, db, storage

credenciales = credentials.Certificate("credenciales.json")

firebase_admin.initialize_app(credenciales, 
{
    "databaseURL":"https://backend-flask-a80c4-default-rtdb.firebaseio.com/",
    "storageBucket" : "backend-flask-a80c4.appspot.com"
}
)

firebaseAlmacenamiento = storage.bucket()
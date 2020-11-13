from base_datos import db

class MarkModel(db.Model):
    __tablename__ = 't_mark'

    markId = db.Column(db.Integer, primary_key=True)
    markDesc = db.Column(db.String(20))
    state = db.Column(db.Boolen, default=True)

    products = db.relationship('ProductModel', backref='product')

    def __init__(self, description):
        self.markDesc = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id' : self.markId,
            'descripcion' : self.markDesc,
            'estado' : self.state
        }
    

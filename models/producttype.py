from base_datos import db

class ProductTypeModel(db.Model):
    __tablename__ = 't_producttype'
    producttypeId = db.Column(db.Integer, primary_key=True)
    producttypeDesc = db.Column(db.String(20))
    state = db.Column(db.Boolean, default=True)

    subcategoryId = db.Column(db.Integer, db.ForeignKey('t_subcategory.subcategoryId'), nullable=False)

    products = db.relationship('ProductModel', backref='producttype')

    def __init__(self, description, subcategoryId):
        self.producttypeDesc = description
        self.subcategoryId = subcategoryId

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.producttypeId,
            'descripcion': self.producttypeDesc,
            'estado': self.state,
            'subcategoria': self.subcategoryId
        }

    def __str__(self):
        return '%s, %s, %s, %s'%(self.producttypeId, self.producttypeDesc, self.state, self.subcategoryId)
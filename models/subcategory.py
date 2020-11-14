from base_datos import db

class SubCategoryModel(db.Model):
    __tablename__ = 't_subcategory'
    subcategoryId = db.Column(db.Integer, primary_key=True)
    subcategoryDesc = db.Column(db.String(20))
    state = db.Column(db.Boolean, default=True)

    categoryId = db.Column(db.Integer, db.ForeignKey('t_category.categoryId'), nullable=False)

    types = db.relationship('ProductTypeModel', backref='subcategory')

    def __init__(self, description, categoryId):
        self.subcategoryDesc = description
        self.categoryId = categoryId

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.subcategoryId,
            'descripcion': self.subcategoryDesc,
            'estado': self.state,
            'categoria': self.categoryId
        }

    def __str__(self):
        return '%s, %s, %s, %s'%(self.subcategoryId, self.subcategoryDesc, self.state, self.categoryId)
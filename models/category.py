from base_datos import db

class CategoryModel(db.Model):
    __tablename__ = 't_category'
    categoryId = db.Column(db.Integer, primary_key=True)
    categoryDesc = db.Column(db.String(20))
    state = db.Column(db.Boolean, default=True)

    subcategories = db.relationship('SubCategoryModel', backref='category')

    def __init__(self, description):
        self.categoryDesc = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.categoryId,
            'descripcion': self.categoryDesc,
            'estado': self.state
        }

    def __str__(self):
        return '%s, %s, %s'%(self.categoryId, self.categoryDesc, self.state)
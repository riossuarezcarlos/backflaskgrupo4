from base_datos import db

class LabelModel(db.Model):
    __tablename__ = 't_label'
    labelId = db.Column(db.Integer, primary_key=True)
    labelDesc = db.Column(db.String(20))
    state = db.Column(db.Boolean, default=True)

    products = db.relationship('ProductModel', backref='label')


    def __init__(self, description):
        self.labelDesc = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.labelId,
            'descripcion': self.labelDesc,
            'estado': self.state
        }

    def __str__(self):
        return '%s, %s, %s'%(self.labelId, self.labelDesc, self.state)
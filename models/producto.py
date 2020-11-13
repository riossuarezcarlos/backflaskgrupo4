from base_datos import db
class ProductModel(db.Model):
    __tablename__ = "t_product"
    productId = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(200))
    productDesc = db.Column(db.String(500))
    productImg = db.Column(db.String(500))
    productPrice = db.Column(db.Float())
    productStock = db.Column(db.Integer)
    state = db.Column(db.Boolean, default=True)
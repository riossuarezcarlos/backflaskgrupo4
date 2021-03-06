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

    producttypeId = db.Column(db.Integer, db.ForeignKey('t_producttype.producttypeId'), nullable=False)
    markId = db.Column(db.Integer, db.ForeignKey('t_mark.markId'), nullable=False)
    labelId = db.Column(db.Integer, db.ForeignKey('t_label.labelId'), nullable=False)

    def __init__(self, name, description, img, price, stock, producttypeId, markId, labelId):
        self.productName = name
        self.productDesc = description
        self.productImg = img
        self.productPrice = price
        self.productStock = stock
        self.producttypeId = producttypeId
        self.markId = markId
        self.labelId = labelId

    def save(self):
        db.session.add(self)
        db.session.commit()

    def show(self):
        return{
            'id' : self.productId,
            'nombre' : self.productName,
            'descripcion' : self.productDesc,
            'img' : self.productImg,
            'precio' : self.productPrice,
            'stock' : self.productStock,
            'estado' : self.state,
            'tipoproducto' : self.producttypeId,
            'marca' : self.markId,
            'etiqueta' : self.labelId
        }

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(self.productId,self.productName,self.productDesc,self.productImg,self.productPrice,self.productStock,self.state,self.producttypeId,self.markId, self.labelId)

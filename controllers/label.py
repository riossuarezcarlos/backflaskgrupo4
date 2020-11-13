from flask_restful import Resource, reqparse
from models.label import LabelModel

class LabelsController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "labelDesc",
        type=str,
        required=True,
        help="labelDesc es obligatorio"
    )

    def get(self):
        labels = LabelModel.query.all()
        listado = []
        for label in labels:
            listado.append(label.show())
        
        return{
            'ok': True,
            'message': None,
            'content': listado
        }

    def post(self):
        data = self.parser.parse_args()
        label = LabelModel(data['labelDesc'])
        try:
            label.save()
            return{
                'ok': True,
                'message': 'Label registrado correctamente',
                'content': label.show()
            }
        except Exception as e:
            return{
                'ok': False,
                'message': 'Ocurrio un error: ' + str(e),
                'content': None
            }, 500

class LabelController(Resource):
    def get(self, labelId):
        label = LabelModel.query.filter_by(labelId = labelId).first()
        if label:
            return{
                'ok': True,
                'message': '',
                'content': label.show()
            }
        else:
            return{
                'ok': False,
                'message': 'No existe label con id: ' + str(labelId),
                'content': None
            }, 404
    def put(self, labelId):
        label = LabelModel.query.filter_by(labelId = labelId).first()
        if label:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "labelDesc",
                type=str,
                required=True,
                help="labelDesc es obligatorio"
            )

            data = parser.parse_args()
            label.labelDesc = data['labelDesc']
            label.save()

            return{
                'ok': True,
                'message': 'Label actualizado correctamente',
                'content': label.show()
            }
        else:
            return{
                'ok': False,
                'message': 'No existe label con id: ' + str(labelId),
                'content': None
            }, 404
    
    def delete(self, labelId):
        label = LabelModel.query.filter_by(labelId = labelId).first()
        if label:
            if label.state:
                label.state = False
                label.save()
                return{
                    'ok': True,
                    'message': 'Label deshabilitado correctamente',
                    'content': label.show()
                }
            else:
                return{
                    'ok': False,
                    'message': 'Label ya se encuentra deshabilitado',
                    'content': None
                }
        else:
            return{
                'ok': False,
                'message': 'No existe label con id: ' + str(labelId),
                'content': None
            }, 404

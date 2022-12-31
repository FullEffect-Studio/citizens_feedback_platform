from flask_restful import Resource
from pydantic import BaseModel, ValidationError
from flask import jsonify, request


class AddTwoNumbersDto(BaseModel):
    x: int
    y: int


class Add(Resource):

    def post(self):

        try:
            data = AddTwoNumbersDto(**request.get_json())
        except ValidationError:
            results = {
                'message': 'Invalid operands',
                'status_code': 304
            }
            return jsonify(results)

        results = {
            'message': data.x + data.y,
            'status_code': 200
        }

        return jsonify(results)
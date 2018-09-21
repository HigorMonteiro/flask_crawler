from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/database'

mongo = PyMongo(app)


class Property(Resource):

    def get(self):
        collection = mongo.db.properties
        properties = []
        for immobile in collection.find():
            properties.append({
                'category': immobile.get('category', ''),
                'value': immobile.get('value', ''),
                'title': immobile.get('title', ''),
                'address': immobile.get('address', ''),
                'characteristics': immobile.get('characteristics', '')
            })
        return jsonify({'result': properties})


api.add_resource(Property, '/properties')

if __name__ == '__main__':
    app.run(debug=True)

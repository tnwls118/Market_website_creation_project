import os
from flask import Flask, request, render_template, redirect
from flask.json import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)


@app.route('/detail')
def detail():
    product_db = mongo.db.product
    product = product_db.find_one({"title": request.args.get('title')})

    # API에서 가격, 위치, 이미지도 반환하도록 변경
    return jsonify({
        'title': product.get('title'),
        'content': product.get('content'),
        'price': product.get('price'),
        'location': product.get('location'),
        'image': product.get('image')
    })


@app.route('/writepage')
def writepage():
    return render_template('write.html')


@app.route('/write', methods=['POST'])
def write():
    fileinfo = request.files['image']
    filepath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(filepath, 'static')

    fileinfo.save(os.path.join(filepath, fileinfo.filename))

    product_db = mongo.db.product

    product_db.insert_one({
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'price': request.form.get('price'),
        'location': request.form.get('location'),
        'image': fileinfo.filename
    })

    return redirect('/')


@app.route('/')
def main():
    product_db = mongo.db.product
    products = product_db.find()
    return render_template('list.html', products=products)


if __name__ == '__main__':
    app.run()

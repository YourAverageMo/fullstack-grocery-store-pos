from flask import Flask, request, jsonify, render_template
from db import products_dao
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getproducts', methods=['GET'])
def get():
    conn, cursor = products_dao.connect_to_db()
    products = products_dao.get_all_products(cursor)

    response = jsonify(products)
    conn.close()
    return response


@app.route('/deleteproduct', methods=['POST'])
def delete():

    data = request.json
    print(data)
    product_ids = data.get('product_ids', [])
    print(product_ids)

    # conn, cursor = products_dao.connect_to_db()
    # response = products_dao.delete_products(cursor, product_ids, True)

    # conn.close()
    return response


if __name__ == '__main__':
    print("starting flask server for grocery store pos")
    app.run(debug=True, port=5000)

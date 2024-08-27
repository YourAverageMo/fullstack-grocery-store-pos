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
    product_id = data.get('product_ids', [])[0]
    product_id = int(product_id)

    conn, cursor = products_dao.connect_to_db()
    products_dao.delete_products(cursor, [(product_id, product_id)], True)

    conn.commit()
    conn.close()
    return jsonify({
        "status": "success",
        "message": "Products deleted successfully."
    }), 200


if __name__ == '__main__':
    print("starting flask server for grocery store pos")
    app.run(debug=True, port=5000)

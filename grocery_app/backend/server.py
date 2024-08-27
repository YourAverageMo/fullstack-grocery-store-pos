from flask import Flask, request, jsonify
import products_dao
import sqlite3

app = Flask(__name__)


@app.route('/getproducts',methods=['GET'])
def get():
    conn, cursor = products_dao.connect_to_db()
    products = products_dao.get_all_products(cursor)

    response = jsonify(products)
    conn.close()
    return response


if __name__ == '__main__':
    print("starting flask server for grocery store pos")
    app.run(debug=True, port=5000)

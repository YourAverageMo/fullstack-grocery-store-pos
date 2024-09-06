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
    
@app.route('/insertproduct', methods=['POST'])
def insert_product():
    data = request.json
    product_name = data.get('name')
    product_units = int(data.get('units'))
    product_price = int(data.get('price'))

    if product_name and isinstance(product_units, int) and isinstance(product_price, (int, float)):
        conn, cursor = products_dao.connect_to_db()
        products_dao.insert_new_products(cursor, [(product_name, product_units, product_price)])
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid product data'})
    
@app.route('/editproduct/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    data = request.json
    new_name = data.get('name')
    new_units = int(data.get('units'))
    new_price = int(data.get('price'))
    
    conn, cursor = products_dao.connect_to_db()
    products_dao.edit_product(cursor,new_name,new_units,new_price,product_id)
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})




if __name__ == '__main__':
    print("starting flask server for grocery store pos")
    app.run(debug=True, port=5000)

import datetime, pymysql, httplib2, json, sys
from app import app, db
from flask import request, jsonify, make_response

#Root API
@app.route("/")
def root():
    return "Micro IMS 2 - Distributed System"

#API PRODUK - PRODUK DI GUDANG (Info Semua Product) dan API POST PRODUK DI GUDANG (Update Stok)
@app.route("/api/products", methods=['GET', 'POST'])
def products():
    #API PRODUK - PRODUK DI GUDANG (Info Semua Product)
    if request.method == 'GET':
        connection = None
        cursor = None
        try:
            connection = db.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            products = cursor.execute("SELECT product_id, product_name, product_quantity FROM product")
            products = cursor.fetchall()
            return make_response(jsonify(products)), 200
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    # API POST PRODUK DI GUDANG (Update Stok)
    elif request.method == 'POST':
        if not request.json:
            return make_response(jsonify(['Empty Request Body'])), 400
        product_id = request.json.get('product_id', None)
        product_quantity = request.json.get('product_quantity', None)
        connection = None
        cursor = None
        try:
            if product_id and product_quantity:
                connection = db.connect()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                product = cursor.execute("UPDATE product SET product_quantity = %s WHERE product_id = %s", (product_quantity, product_id))
                connection.commit()
                return make_response(jsonify(['Successfully update product.'])), 200
            return make_response(jsonify(['Wrong Request Body'])), 400
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

#API GET PRODUK DI GUDANG (Info Stok)
@app.route("/api/products/<int:product_id>", methods=['GET'])
def product(product_id):
    connection = None
    cursor = None
    try:
        connection = db.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        product = cursor.execute("SELECT product_id, product_name, product_quantity FROM product WHERE product_id='" + str(product_id) + "'")
        product = cursor.fetchone()
        return make_response(jsonify(product)), 200
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

#API PRODUCTS DARI GUDANG LAIN
# @app.route("/api/inventories/<int:product_id>", methods=['GET', 'POST'])
# def inventories(product_id):
    # try:
        # address = 'http://localhost:2020/api/products/'
        # url = address + product_id
        # h = httplib2.Http()
        # resp, result = h.request(url, 'GET')
        # obj_json = json.loads(result)
        # return make_response(jsonify(obj_json)), 200
        # if resp['status'] != '200':
            # raise Exception('Received an unsuccessful status code of %s' % resp['status'])
        
    # except Exception as err:
        # print ("FAILED: Could not make GET Request to web server")
        # print (err.args)
        # sys.exit()
    # else:
        # print ("PASS: Successfully Made GET Request to /api/products")

#API PRODUCTS DARI VENDOR KE GUDANG
@app.route("/api/vendor/<int:product_id>", methods=['POST', 'GET'])
def vendor():
    return
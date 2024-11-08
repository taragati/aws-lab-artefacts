import json
import uuid
# import psycopg2

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def orders():
    return 'Hello ECS Service'
    # return getAllOrders()


# @app.route('/orders/<id>', methods=['GET'])
# def orderById(id):
#     return getOrderById(request.view_args['id'])
#
# @app.route('/orders/<id>', methods=['GET'])
# def orderById(id):
#     return getOrderById(request.view_args['id'])
#
# def getAllOrders():
#     try:
#         print('Before connection establish')
#         connection = psycopg2.connect(user="postgres",
#                                       password="R3mlsfHgPfaVyYSHgOmL",
#                                       host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
#                                       port="5432",
#                                       database="ecsdemo")
#
#         cursor = connection.cursor()
#         records = []
#         postgreSQL_select_Query = "SELECT JSON_AGG(r) FROM (select * from orders) r"
#         cursor.execute(postgreSQL_select_Query)
#         print("Selecting rows from orders table using cursor.fetchall")
#         orders = cursor.fetchall()
#         for row in orders:
#             records.append(row)
#         print(orders)
#     except (Exception, psycopg2.Error) as error:
#         print("Error while fetching data from PostgreSQL", error)
#
#     finally:
#         # closing database connection.
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#         return orders
#
# def getOrderById(id):
#     try:
#         connection = psycopg2.connect(user="postgres",
#                                       password="R3mlsfHgPfaVyYSHgOmL",
#                                       host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
#                                       port="5432",
#                                       database="ecsdemo")
#
#         cursor = connection.cursor()
#         records = []
#         k="orderid"
#         v=id
#         postgreSQL_select_Query = "select * from orders where orderid="+v
#         cursor.execute(postgreSQL_select_Query)
#         print("Selecting rows from orders table using cursor.fetchall")
#         orders = cursor.fetchall()
#         for row in orders:
#             records.append(row)
#         print(orders)
#     except (Exception, psycopg2.Error) as error:
#         print("Error while fetching data from PostgreSQL", error)
#
#     finally:
#         # closing database connection.
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#         return orders
#
# def insertOrder(pid,pname,price):
#     try:
#         connection = psycopg2.connect(user="postgres",
#                                       password="R3mlsfHgPfaVyYSHgOmL",
#                                       host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
#                                       port="5432",
#                                       database="ecsdemo")
#         cursor = connection.cursor()
#
#         postgres_insert_query = """ INSERT INTO orders(productid,productname,productprice) VALUES (%s,%s,%s)"""
#         record_to_insert = [(pid,pname,price)]
#         for i in record_to_insert:
#             cursor.execute(postgres_insert_query, i)
#             connection.commit()
#             count = cursor.rowcount
#         print(count, "Record inserted successfully into publisher table")
#
#     except (Exception, psycopg2.Error) as error:
#         print("Failed to insert record into publisher table", error)
#
#     finally:
#         # closing database connection.
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
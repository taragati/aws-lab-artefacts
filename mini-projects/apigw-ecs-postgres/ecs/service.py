import json
import uuid
import psycopg2

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def getOrders():
    response = {
        "data": 'getAllOrders()',
        "message": "success"
    }
    return response

def getAllOrders():
    try:
        print('Before connection establish')
        connection = psycopg2.connect(user="postgres",
                                      password="R3mlsfHgPfaVyYSHgOmL",
                                      host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
                                      port="5432",
                                      database="ecsdemo")

        cursor = connection.cursor()
        records = []
        postgreSQL_select_Query = "SELECT JSON_AGG(r) FROM (select * from orders) r"
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from orders table using cursor.fetchall")
        orders = cursor.fetchall()
        for row in orders:
            records.append(row)
        print(orders)
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def getOrderById(args):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="R3mlsfHgPfaVyYSHgOmL",
                                      host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
                                      port="5432",
                                      database="ecsdemo")

        cursor = connection.cursor()
        records = []
        k="orderid"
        v=args[2]
        postgreSQL_select_Query = "select * from orders where orderid="+v
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from orders table using cursor.fetchall")
        orders = cursor.fetchall()
        for row in orders:
            records.append(row)
        print(orders)
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def insertOrder(args):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="R3mlsfHgPfaVyYSHgOmL",
                                      host="ecsdemo-pydb.cz2aky0mczp9.ap-south-1.rds.amazonaws.com",
                                      port="5432",
                                      database="ecsdemo")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO orders(productid,productname,productprice) 
        VALUES (%s,%s,%s)"""
        pid=args[2]
        pname=args[3]
        price=args[4]
        record_to_insert = [(pid,pname,price)]
        for i in record_to_insert:
            cursor.execute(postgres_insert_query, i)

            connection.commit()
            count = cursor.rowcount
        print(count, "Record inserted successfully \
        into publisher table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into publisher table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
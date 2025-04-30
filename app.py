from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
import maskpass

pwd = maskpass.askpass(prompt="Password:", mask="#")

app = Flask(__name__)
CORS(app)

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=pwd,  # Replace with your MySQL password
        database="fleet"
    )

# Execute SQL query function
def execute_query(query, params=None):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

# Fetch data function
def fetch_data(query, params=None):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'GET':
        vehicles = fetch_data("SELECT * FROM vehicles")
        return jsonify(vehicles)
    elif request.method == 'POST':
        data = request.json
        query = """
            INSERT INTO vehicles (vehicle_id, vehicle_type, vehicle_model, vehicle_capacity, assigned_driver)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (data['id'], data['type'], data['model'], data['capacity'], None)
        if execute_query(query, params):
            return jsonify({"message": "Vehicle added successfully"}), 201
        else:
            return jsonify({"message": "Failed to add vehicle"}), 400

@app.route('/vehicles/<vehicle_id>', methods=['DELETE', 'PUT'])
def vehicle_operations(vehicle_id):
    if request.method == 'DELETE':
        query = "DELETE FROM vehicles WHERE vehicle_id = %s"
        if execute_query(query, (vehicle_id,)):
            return jsonify({"message": "Vehicle deleted successfully"}), 200
        else:
            return jsonify({"message": "Failed to delete vehicle"}), 400
    elif request.method == 'PUT':
        data = request.json
        query = """
            UPDATE vehicles
            SET vehicle_type = %s, vehicle_model = %s, vehicle_capacity = %s
            WHERE vehicle_id = %s
        """
        params = (data['type'], data['model'], data['capacity'], vehicle_id)
        if execute_query(query, params):
            return jsonify({"message": "Vehicle updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update vehicle"}), 400

@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
    if request.method == 'GET':
        drivers = fetch_data("SELECT * FROM drivers")
        return jsonify(drivers)
    elif request.method == 'POST':
        data = request.json
        query = """
            INSERT INTO drivers (driver_name, driver_license, assigned_vehicle)
            VALUES (%s, %s, %s)
        """
        params = (data['name'], data['license'], None)
        if execute_query(query, params):
            return jsonify({"message": "Driver added successfully"}), 201
        else:
            return jsonify({"message": "Failed to add driver"}), 400

@app.route('/drivers/<driver_name>', methods=['DELETE', 'PUT'])
def driver_operations(driver_name):
    if request.method == 'DELETE':
        query = "DELETE FROM drivers WHERE driver_name = %s"
        if execute_query(query, (driver_name,)):
            return jsonify({"message": "Driver deleted successfully"}), 200
        else:
            return jsonify({"message": "Failed to delete driver"}), 400
    elif request.method == 'PUT':
        data = request.json
        query = """
            UPDATE drivers
            SET driver_license = %s
            WHERE driver_name = %s
        """
        params = (data['license'], driver_name)
        if execute_query(query, params):
            return jsonify({"message": "Driver updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update driver"}), 400

@app.route('/assign', methods=['POST'])
def assign_driver():
    data = request.json
    driver_name = data['driverName']
    vehicle_id = data['vehicleId']
    
    # Update driver
    driver_query = """
        UPDATE drivers
        SET assigned_vehicle = %s
        WHERE driver_name = %s
    """
    # Update vehicle
    vehicle_query = """
        UPDATE vehicles
        SET assigned_driver = %s
        WHERE vehicle_id = %s
    """
    
    if execute_query(driver_query, (vehicle_id, driver_name)) and execute_query(vehicle_query, (driver_name, vehicle_id)):
        return jsonify({"message": f"{driver_name} has been assigned to vehicle {vehicle_id}"}), 200
    else:
        return jsonify({"message": "Failed to assign driver to vehicle"}), 400

if __name__ == '__main__':
    app.run(debug=True)

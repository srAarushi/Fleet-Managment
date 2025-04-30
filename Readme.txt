# Fleet Management System

A web-based Fleet Management System that allows users to manage vehicles and drivers, including adding, updating, viewing, and deleting records. This application is built with an HTML/CSS/JavaScript frontend and a Flask backend with MySQL database support.

---

## Features

- **Vehicle Management**: Add, view, update, and delete vehicle details.
- **Driver Management**: Add, view, update, and delete driver information.
- **Driver Assignment**: Assign a driver to a specific vehicle.
- **MySQL Database**: All records are stored in a MySQL database.

---

## Prerequisites

1. **Python** 
2. **MySQL Database**

---

## Installation


### 1. Backend Setup (Flask & MySQL)

1. Install necessary Python packages:

    ```bash
    pip install Flask flask-mysql-connector
    ```

2. Create a MySQL Database:

    - Log into your MySQL database and create a new database:
    
      ```sql
      CREATE DATABASE fleet_management;
      USE fleet_management;
      ```

    - Create the required tables:

      ```sql
      CREATE TABLE vehicles (
          vehicle_id VARCHAR(255) PRIMARY KEY,
          vehicle_type VARCHAR(255),
          vehicle_model VARCHAR(255),
          vehicle_capacity INT,
          assigned_driver VARCHAR(255)
      );

      CREATE TABLE drivers (
          driver_name VARCHAR(255) PRIMARY KEY,
          driver_license VARCHAR(255),
          assigned_vehicle VARCHAR(255)
      );
      ```

3. Configure the Flask Application

    - Open `app.py` in the root directory.
    - Update the `db_connection` function with your MySQL credentials:
      ```python
      connection = mysql.connector.connect(
          host="localhost",
          user="your_username",
          password="your_password",
          database="fleet_management"
      )
      ```

4. Run the Flask Server:

    ```bash
    python app.py
    ```

   The server will start at `http://localhost:5000`.

### 3. Frontend Setup

The frontend is built with HTML, CSS, and JavaScript. Simply open `index.html` in your preferred web browser or serve it using a local server such as [http-server]
```

This will start a server at `http://localhost:8080` by default.

---

## API Endpoints

### Vehicles

- **GET /vehicles**: Fetch all vehicles
- **POST /vehicles**: Add a new vehicle
- **PUT /vehicles/<vehicle_id>**: Update vehicle details
- **DELETE /vehicles/<vehicle_id>**: Delete a vehicle

### Drivers

- **GET /drivers**: Fetch all drivers
- **POST /drivers**: Add a new driver
- **PUT /drivers/<driver_name>**: Update driver details
- **DELETE /drivers/<driver_name>**: Delete a driver

### Assignments

- **POST /assign**: Assign a driver to a vehicle

---

## Usage

1. Open the frontend (`index.html`) in your browser.
2. Use the navigation menu to access different sections of the app:
   - **Home**: Landing page with options to manage vehicles and drivers.
   - **Vehicles**: Manage your fleet's vehicles.
   - **Drivers**: Manage driver information and assignments.

3. All operations (add, view, update, delete) for vehicles and drivers can be performed directly from the frontend interface.




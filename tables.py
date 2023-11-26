#!/usr/bin/env python3
import random
import string
import uuid
from faker import Faker
import mysql.connector

import tables
'''
This code establishes a connection to a MySQL database using the mysql.connector library.
Parameters:
- host: The hostname or IP address of the MySQL container.
- port: The port number to connect to the MySQL container (default is 3306).
- user: The username for authenticating with the MySQL container.
- password: The password associated with the provided username.
- database: The name of the MySQL database to connect to.
'''
connection = mysql.connector.connect(
	host="localhost",
	port="3306",
	user="root",
	password="root_password",
	database="mysql_db"
)
cursor = connection.cursor()


'''
Before creation of data we must first create our tables and all of there attributes
'''

def gen_tables():
	
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS members (
		id INT AUTO_INCREMENT PRIMARY KEY,
		first_name VARCHAR(99),
		last_name VARCHAR(99),
		phone VARCHAR(99),
		email VARCHAR(99),
		dob DATE,
		join_date DATE,
		address TEXT,
		member_uuid VARCHAR(99)
	)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS employees (
			employee_id INT AUTO_INCREMENT PRIMARY KEY,
			fn VARCHAR(99),
			ln VARCHAR(99),
			phone VARCHAR(99),
			email VARCHAR(99),
			hire_date DATETIME
		)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS courses (
			course_id INT AUTO_INCREMENT PRIMARY KEY,
			course_name VARCHAR(99)
		)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS equipment (
			id INT AUTO_INCREMENT PRIMARY KEY,
			name VARCHAR(99),
			manufacturer VARCHAR(99),
			purchase_date DATE,
			sn VARCHAR(99)
		)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS transactions (
			id INT AUTO_INCREMENT PRIMARY KEY,
			member_id INT,
			card_type VARCHAR(99),
			card_holder VARCHAR(99),
			card_number VARCHAR(99),
			expiry_date VARCHAR(99),
			cvc VARCHAR(99),
			FOREIGN KEY (member_id) REFERENCES members(id)
		)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS classes (
			class_id INT AUTO_INCREMENT PRIMARY KEY,
			instructor VARCHAR(99),
			schedule VARCHAR(99),
			capacity INT,
			duration_seconds INT,
			employee_id INT,
			course_id INT,
			FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
			FOREIGN KEY (course_id) REFERENCES courses(course_id)
		)
	""")
	connection.commit()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS attendance (
			attendance_id INT AUTO_INCREMENT PRIMARY KEY,
			attendance_date DATETIME,
			status VARCHAR(25),
			member_id INT,
			class_id INT,
			FOREIGN KEY (member_id) REFERENCES members(id),
			FOREIGN KEY (class_id) REFERENCES classes(class_id)
		)
	""")
	connection.commit()

def drop_table(table_name):

		drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
		cursor.execute(drop_table_query)
		cursor.fetchall()
		connection.commit()
		
def drop_all():
	# Drop the entire database
	drop_database_query = "DROP DATABASE IF EXISTS mysql_db"
	cursor.execute(drop_database_query)
	cursor.fetchall()
	connection.commit()
	
	# Recreate the database
	create_database_query = "CREATE DATABASE mysql_db"
	cursor.execute(create_database_query)
	cursor.fetchall()
	connection.commit()
	
	# Call the function to generate tables
	gen_tables()
	
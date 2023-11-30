import mysql.connector
from flask import Flask, render_template, request, jsonify
import ss

#FLASK FLASK FLASK FLASK FLASK
app = Flask(__name__)

connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root_password",
    database="mysql_db"
)

cursor = connection.cursor()

def get_members():
    try:
        cursor.execute("SELECT * FROM Members")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_employees():
    try:
        cursor.execute("SELECT * FROM Employees")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
def get_employee_salary_statistics():
    try:
        cursor.execute("SELECT * FROM EmployeeSalaryStatistics")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_product_inventory():
    try:
        cursor.execute("SELECT * FROM ProductInventory")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_equipment_inventory():
    try:
        cursor.execute("SELECT * FROM EquipmentInventory")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_transactions():
    try:
        cursor.execute("SELECT * FROM Transaction")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_lost_and_found_items():
    try:
        cursor.execute("SELECT * FROM LostAndFound")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_visitors_log():
    try:
        cursor.execute("SELECT * FROM VisitorsLog")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_classes():
    try:
        cursor.execute("SELECT * FROM Classes")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error: {e}")
        return []
    
# Define the route to handle the AJAX request
@app.route('/call_function', methods=['POST'])
def call_function():
    try:
        data = request.get_json()  # Get the JSON data from the AJAX request
        function_name = data.get('function')
        parameter = 10

        # Call the corresponding Python function based on the function_name
        if function_name == 'gen_x_members':
            ss.gen_x_members(parameter)
        elif function_name == 'gen_x_employees':
            ss.gen_x_employees(parameter)
        elif function_name == 'gen_x_products':
            ss.gen_x_products(parameter)
        elif function_name == 'gen_x_equipment':
            ss.gen_x_equipment(parameter)
        elif function_name == 'gen_x_transactions':
            ss.gen_x_transactions(parameter)
        elif function_name == 'gen_x_lost_and_found_items':
            ss.gen_x_lost_and_found_items(parameter)
        elif function_name == 'gen_x_visitors_log_entries':
            ss.gen_x_visitors_log_entries(parameter)
        elif function_name == 'gen_x_classes':
            ss.gen_x_classes(parameter)
        else:
            return jsonify({'message': 'Invalid function name'}), 400

        return jsonify({'message': 'Function executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/members')
def display_members():
    records = get_members()
    return render_template('members.html', records=records)

@app.route('/employees')
def display_employees():
    records = get_employees()
    return render_template('employees.html', records=records)

@app.route('/salary_stats')
def display_employee_salary_statistics():
    records = get_employee_salary_statistics()
    return render_template('salary_stats.html', records=records)

@app.route('/product_inventory')
def display_product_inventory():
    records = get_product_inventory()
    return render_template('product_inventory.html', records=records)

@app.route('/equipment_inventory')
def display_equipment_inventory():
    records = get_equipment_inventory()
    return render_template('equipment_inventory.html', records=records)

@app.route('/transactions')
def display_transactions():
    records = get_transactions()
    return render_template('transactions.html', records=records)

@app.route('/lost_and_found')
def display_lost_and_found_items():
    records = get_lost_and_found_items()
    return render_template('lost_and_found.html', records=records)

@app.route('/visitors_log')
def display_visitors_log():
    records = get_visitors_log()
    return render_template('visitors_log.html', records=records)

@app.route('/classes')
def display_classes():
    records = get_classes()
    return render_template('classes.html', records=records)

#Requirement 1
@app.route('/req1')
def report():
    report_data = ss.report_employee_classes()
    return render_template('req1.html', report_data=report_data)

#Requirement 2
@app.route('/req2')
def req2():
    data = ss.get_employees_with_above_average_salary()
    return render_template('req2.html', data=data) 

#Requiremnent 3
#this is 3 and 4
@app.route('/req3-4')
def view():
    try:
        ss.create_employee_classes_view()
        print("View 'EmployeeClassesView' created successfully.")
    except mysql.connector.ProgrammingError:
        print("View 'EmployeeClassesView' already exists, moving on")

    view_report = ss.view_employee_classes_view()
    return render_template('req3-4.html', view_report=view_report)

@app.route('/')
def home():

    # Execute the queries and fetch the counts
    cursor.execute("SELECT COUNT(*) FROM Members")
    total_rec_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Employees")
    total_rec_employees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ProductInventory")
    total_rec_product_inventory = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM EquipmentInventory")
    total_rec_equipment_inventory = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Transaction")
    total_rec_transaction = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM LostAndFound")
    total_rec_lost = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM VisitorsLog")
    total_rec_visitors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Classes")
    total_rec_classes = cursor.fetchone()[0]

    total_rec_all = total_rec_members + total_rec_employees + total_rec_product_inventory + total_rec_equipment_inventory + total_rec_transaction + total_rec_lost + total_rec_visitors + total_rec_classes



    # Pass the counts to the template
    return render_template('index.html', 
                           total_rec_members=total_rec_members, 
                           total_rec_employees=total_rec_employees, 
                           total_rec_product_inventory=total_rec_product_inventory, 
                           total_rec_equipment_inventory=total_rec_equipment_inventory, 
                           total_rec_transaction=total_rec_transaction, 
                           total_rec_lost=total_rec_lost, 
                           total_rec_visitors=total_rec_visitors, 
                           total_rec_classes=total_rec_classes, 
                           total_rec_all=total_rec_all)

if __name__ == '__main__':
    app.run(debug=True)


import random
import string
import uuid
from faker import Faker
import mysql.connector

fake = Faker()

#Establish connection to docker mysql db
connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root_password",
    database="mysql_db"
)
cursor = connection.cursor()

equipment = ['Dumbbells', 'Barbells', 'Weight Plates', 'Kettle Bells', 'Medicine Balls', 'Weighted Balls', 'Resistance Bands', 'Sandbags', 'Jump Rope', 'Stretch Bars' ]

machines = ['Treadmill', 'Elliptical', 'Stationary Bike', 'Rowing Machine', 'Stair Climber', 'Chest Press Machine', 'Lat Pulldown Machine', 'Cable Machine', 'Leg Press Machine']

fitness_manufacturers = ["IronFlex Tech", "PowerPulse Dynamics", "GymGear Innovations", "EpicFit Systems", "Titanic Fitness Solutions", "Zenith Muscle Machines", "Quantum Liftware", "AeroFlex Athletics", "HyperDrive Fitness", "XtremeForge Equipment"]

courses = ["Cardio Blast", "Strength Training", "Yoga Basics", "Pilates Pro", "Zumba Dance", "Kickboxing", "Spin Class", "Aerobics", "CrossFit", "HIIT Interval"]

cursor = connection.cursor()

"""
This function, create_tables, is responsible for setting up the database schema for a gym management system. 

It creates the following tables:

1. members: This table stores information about gym members, including their name, phone number, email, date of birth, join date, address, and a unique member UUID.

2. employees: This table stores information about gym employees, including their name, phone number, email, and hire date.

3. courses: This table stores information about the courses offered at the gym, including a unique course ID and the course name.

4. equipment: This table stores information about the gym's equipment, including a unique ID, the name of the equipment, the manufacturer, the purchase date, and a serial number.

5. transactions: This table stores information about transactions made by gym members. It includes a unique ID, the member's ID, card type, card holder's name, card number, expiry date, and cvc. It also includes a foreign key reference to the members table.

6. classes: This table stores information about the classes offered at the gym. It includes a unique class ID, the instructor's name, the schedule, capacity, duration in seconds, the employee ID of the instructor, and the course ID. It also includes foreign key references to the employees and courses tables.

7. attendance: This table stores information about the attendance of members at classes. It includes a unique attendance ID, the date of attendance, the status of the attendance, the member's ID, and the class ID. It also includes foreign key references to the members and classes tables.

After each table is created, a commit is made to the database to save the changes, and a message is printed to the console indicating the successful creation of the table.
"""
def create_tables():
    
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
    print('members table created successfully')
    
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
    print('employees table created successfully')
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(99)
        )
    """)
    connection.commit()
    print('courses table created successfully')
    
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
    print('equipment table created successfully')
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            transactions_amount INT,
            card_type VARCHAR(99),
            card_holder VARCHAR(99),
            card_number VARCHAR(99),
            expiry_date VARCHAR(99),
            cvc VARCHAR(99),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)
    connection.commit()
    print('transactions table created successfully')
    
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
    print('classes table created successfully')
    
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
    print('attendance table created successfully')

def gen_x_members(x):
    
    for new_member in range(x):
        fn = fake.first_name()
        ln = fake.last_name()
        phone = fake.phone_number()
        email = fake.email()
        dob = fake.date_of_birth()
        join_date = fake.date()
        address=fake.address().replace('\n',', ')
        member_uuid = str(uuid.uuid4())
        
        insert_member_query = "INSERT INTO members (first_name, last_name, phone, email, dob, join_date, address, member_uuid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (fn, ln, phone, email, dob, join_date, address, member_uuid)
        cursor.execute(insert_member_query, data)
    
    connection.commit()
    print("insert new_member success")
    
def gen_x_transaction(x):
    
    for new_transaction in range(x):
        cc_transaction = fake.credit_card_full()
        transactions_amount = random.randint(1, 500)
        card_type, card_holder, card_number, expiry_date, cvc = cc_transaction.split('\n')
        card_type = card_type.strip()
        card_holder = card_holder.strip()
        card_number = card_number.strip()
        expiry_date = expiry_date.strip()
        cvc = cvc.strip()
        
        # Get a random member ID
        random_member_id = get_random_member_id()
    
        insert_transaction_query = "INSERT INTO transactions (member_id, transactions_amount, card_type, card_holder, card_number, expiry_date, cvc) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (random_member_id, transactions_amount, card_type, card_holder, card_number, expiry_date, cvc)
        cursor.execute(insert_transaction_query, data)
    
    connection.commit()
    print("insert new_transaction success")
    
def gen_x_equipment(x):
    
    characters = string.ascii_letters + string.digits
    
    for new_equipment in range(x):
        equipment_name = random.choice(equipment)
        manufacturer = random.choice(fitness_manufacturers)
        purchase_date = fake.date()
        sn = ''.join(random.choice(characters) for _ in range(28))
        
        
        # Fix the SQL query here
        insert_equipment_query = "INSERT INTO equipment (name, manufacturer, purchase_date, sn) VALUES (%s, %s, %s, %s)"
        
        # Update the data tuple to match the placeholders
        data = (equipment_name, manufacturer, purchase_date, sn)
        cursor.execute(insert_equipment_query, data)
        cursor.execute(insert_equipment_query, data)
        
    connection.commit()
    print("insert new_equipment success")
    
def gen_x_attendance(x):
    for new_attendance in range(x):
        attendance_date = fake.date_time_this_decade()
        status = random.choice(['Present', 'Absent'])
        
        random_member_id = get_random_member_id()
        
        random_class_id = get_random_class_id()
        
        if random_member_id is not None and random_class_id is not None:
            # Insert the attendance record with member_id and class_id
            insert_attendance_query = "INSERT INTO attendance (attendance_date, status, member_id, class_id) VALUES (%s, %s, %s, %s)"
            data = (attendance_date, status, random_member_id, random_class_id)
            cursor.execute(insert_attendance_query, data)
            
    connection.commit()
    print("insert new_attendance success")

def gen_x_courses(x):
    for new_course in range(x):
        course_name = random.choice(courses)
        insert_course_query = "INSERT INTO courses (course_name) VALUES (%s)"
        data = (course_name,)
        cursor.execute(insert_course_query, data)
        
    connection.commit()
    print("insert new_course success")
    
def gen_x_employees(x):
    for new_employee in range(x):
        fn = fake.first_name()
        ln = fake.last_name()
        phone = fake.phone_number()
        email = fake.email()
        hire_date = fake.date_time_this_decade()
        
        insert_employee_query = "INSERT INTO employees (fn, ln, phone, email, hire_date) VALUES (%s, %s, %s, %s, %s)"
        data = (fn, ln, phone, email, hire_date)
        cursor.execute(insert_employee_query, data)
        
    connection.commit()
    print("insert new_employee success")
    
def gen_x_classes(x):
    for new_class in range(x):
        instructor = fake.name()
        schedule = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        capacity = random.randint(10, 30)
        duration_seconds = random.randint(1800, 7200)  # Random duration between 30 minutes and 2 hours
        
        # Get a random employee ID
        employee_id = random_employee_id()
        
        # Get a random course ID
        course_id = random_course_id()
        
        if employee_id is not None and course_id is not None:
            # Insert the class record with employee_id and course_id
            insert_class_query = "INSERT INTO classes (instructor, schedule, capacity, duration_seconds, employee_id, course_id) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (instructor, schedule, capacity, duration_seconds, employee_id, course_id)
            cursor.execute(insert_class_query, data)
            
    connection.commit()
    print("insert new_classes success")
    
def random_employee_id():
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]
    
    if total_employees == 0:
        print("No employees found.")
        return None

    random_employee_id = random.randint(1, total_employees)
    return random_employee_id
    
def get_random_member_id():
    # Check the number of rows in the members table
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]
    
    if total_members == 0:
        print("No members found.")
        return None
    
    # Generate a random primary key within the range of existing members
    random_member_id = random.randint(1, total_members)
    return random_member_id

def get_random_class_id():
    # Check the number of rows in the classes table
    cursor.execute("SELECT COUNT(*) FROM classes")
    total_classes = cursor.fetchone()[0]
    
    if total_classes == 0:
        print("No classes found.")
        return None
    
    # Generate a random primary key within the range of existing classes
    random_class_id = random.randint(1, total_classes)
    return random_class_id


def get_random_member_id():
    # Check the number of rows in the members table
    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]
    
    if total_members == 0:
        print("No members found.")
        return None
    
    # Generate a random primary key within the range of existing members
    random_member_id = random.randint(1, total_members)
    return random_member_id

def get_random_class_id():
    # Check the number of rows in the classes table
    cursor.execute("SELECT COUNT(*) FROM classes")
    total_classes = cursor.fetchone()[0]
    
    if total_classes == 0:
        print("No classes found.")
        return None
    
    # Generate a random primary key within the range of existing classes
    random_class_id = random.randint(1, total_classes)
    return random_class_id

def random_course_id():
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]
    
    if total_courses == 0:
        print("No courses found.")
        return None
    
    random_course_id = random.randint(1, total_courses)
    return random_course_id

def random_employee_id():
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]
    
    if total_employees == 0:
        print("No employees found.")
        return None
    
    random_employee_id = random.randint(1, total_employees)
    return random_employee_id

def drop_table(table_name):
    
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_query)
        cursor.fetchall()
        connection.commit()

def print_em_out():
    
    cursor.execute("SELECT * FROM members")
    members_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM employees")
    employees_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM courses")
    courses_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM equipment")
    equipment_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM transactions")
    transactions_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM classes")
    classes_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM attendance")
    attendance_data = cursor.fetchall()
    
    total_rec_members = 0
    print("Members Table:")
    for row in members_data:
        print(row)
        total_rec_members += 1
    print(f"Total records in Members Table: {total_rec_members}\n")
    
    total_rec_employees = 0
    print("Employees Table:")
    for row in employees_data:
        print(row)
        total_rec_employees += 1
    print(f"Total records in Employees Table: {total_rec_employees}\n")
    
    total_rec_courses = 0
    print("Courses Table:")
    for row in courses_data:
        print(row)
        total_rec_courses += 1
    print(f"Total records in Courses Table: {total_rec_courses}\n")
    
    total_rec_equipment = 0
    print("Equipment Table:")
    for row in equipment_data:
        print(row)
        total_rec_equipment += 1
    print(f"Total records in Equipment Table: {total_rec_equipment}\n")
    
    total_rec_transactions = 0
    print("Transactions Table:")
    for row in transactions_data:
        print(row)
        total_rec_transactions += 1
    print(f"Total records in Transactions Table: {total_rec_transactions}\n")
    
    total_rec_classes = 0
    print("Classes Table:")
    for row in classes_data:
        print(row)
        total_rec_classes += 1
    print(f"Total records in Classes Table: {total_rec_classes}\n")
    
    total_rec_attendance = 0
    print("Attendance Table:")
    for row in attendance_data:
        print(row)
        total_rec_attendance += 1
    print(f"Total records in Attendance Table: {total_rec_attendance}\n")
    
    total_rec_all = total_rec_members + total_rec_employees + total_rec_courses + total_rec_equipment + total_rec_transactions + total_rec_classes + total_rec_attendance
    print(f'Total records in all tables: {total_rec_all}')
    
def get_totals():
    cursor.execute("SELECT COUNT(*) FROM members")
    total_rec_members = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_rec_employees = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_rec_courses = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM equipment")
    total_rec_equipment = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_rec_transactions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM classes")
    total_rec_classes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_rec_attendance = cursor.fetchone()[0]
    
    total_rec_all = total_rec_members + total_rec_employees + total_rec_courses + total_rec_equipment + total_rec_transactions + total_rec_classes + total_rec_attendance
    
    print(f'Total records in Members Table: {total_rec_members}')
    print(f'Total records in Employees Table: {total_rec_employees}')
    print(f'Total records in Courses Table: {total_rec_courses}')
    print(f'Total records in Equipment Table: {total_rec_equipment}')
    print(f'Total records in Transactions Table: {total_rec_transactions}')
    print(f'Total records in Classes Table: {total_rec_classes}')
    print(f'Total records in Attendance Table: {total_rec_attendance}')
    print(f'Total records in all tables: {total_rec_all}')

'''
A report query that uses a JOIN (any type) to report on some aggregate value based on a group by clause.
'''
def get_class_attendance():
    # Write the SQL query
    query = """
        SELECT c.class_id, c.instructor, COUNT(a.attendance_id) as total_attendance
        FROM classes c
        JOIN attendance a ON c.class_id = a.class_id
        GROUP BY c.class_id
    """

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(f"Class ID: {row[0]}, Instructor: {row[1]}, Total Attendance: {row[2]}")

def get_class_with_highest_attendance():
    # Write the SQL query
    query = """
        SELECT class_id, total_attendance
        FROM (
            SELECT c.class_id, COUNT(a.attendance_id) as total_attendance
            FROM classes c
            JOIN attendance a ON c.class_id = a.class_id
            GROUP BY c.class_id
        ) as subquery
        ORDER BY total_attendance DESC
        LIMIT 1
    """

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(f"Class ID: {row[0]}, Total Attendance: {row[1]}")

def create_class_attendance_view():
    # Write the SQL query
    query = """
        CREATE VIEW class_attendance_view AS
        SELECT c.class_id, c.instructor, COUNT(a.attendance_id) as total_attendance
        FROM classes c
        JOIN attendance a ON c.class_id = a.class_id
        GROUP BY c.class_id
    """

    # Execute the query
    cursor.execute(query)
    print("View 'class_attendance_view' created successfully.")

def get_class_with_highest_attendance_from_view():
    # Write the SQL query
    query = """
        SELECT * FROM class_attendance_view
        ORDER BY total_attendance DESC
        LIMIT 1
    """

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(f"Class ID: {row[0]}, Instructor: {row[1]}, Total Attendance: {row[2]}")

#Create average class attendance procedure
def create_average_class_attendance_procedure():
    # Write the SQL query
    query = """
        CREATE PROCEDURE average_class_attendance()
        BEGIN
            SELECT c.class_id, AVG(a.attendance_id) as average_attendance
            FROM classes c
            JOIN attendance a ON c.class_id = a.class_id
            GROUP BY c.class_id;
        END
    """

    cursor.execute(query)

#call procedure defined above ^^^^
def call_average_class_attendance_procedure(cursor):
    # Write the SQL query
    query = "CALL average_class_attendance()"

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(f"Class ID: {row[0]}, Average Attendance: {row[1]}")

def create_mark_all_present_procedure():
    # Write the SQL query
    query = """
        CREATE PROCEDURE mark_all_present(IN class_id INT)
        BEGIN
            DECLARE done INT DEFAULT FALSE;
            DECLARE a_id INT;
            DECLARE cur CURSOR FOR SELECT attendance_id FROM attendance WHERE class_id = class_id;
            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

            OPEN cur;

            read_loop: LOOP
                FETCH cur INTO a_id;
                IF done THEN
                    LEAVE read_loop;
                END IF;
                UPDATE attendance SET status = 'Present' WHERE attendance_id = a_id;
            END LOOP;

            CLOSE cur;
        END
    """

    # Execute the query
    cursor.execute(query)
    print("Stored procedure 'mark_all_present' created successfully.")

def create_after_member_insert_trigger():
    # Write the SQL query
    query = """
        CREATE TRIGGER after_member_insert
        AFTER INSERT ON member FOR EACH ROW
        BEGIN
            INSERT INTO payment (payment_date, amount, payment_method, member_id)
            VALUES (NOW(), '100', 'Credit Card', NEW.member_id);
        END;
    """

    # Execute the query
    cursor.execute(query)

def insert_member_and_trigger_payment():
    # Write the SQL query
    query = """
        INSERT INTO member (first_name, last_name, phone, email, dob, membership_start_date, membership_end_date)
        VALUES ('John', 'Doe', '555-1234', 'john.doe@example.com', '1980-01-01', '2023-01-01', '2023-12-31');
    """

    # Execute the query
    cursor.execute(query)

def create_total_transactions_amount_procedure():
    # Write the SQL query
    query = """
        CREATE PROCEDURE total_transactions_amount(IN member_id INT)
        BEGIN
            SELECT SUM(transactions_amount)
            FROM transactions
            WHERE member_id = member_id;
        END
    """

    # Execute the query
    cursor.execute(query)
    print("Stored procedure 'total_transactions_amount' created successfully.")

#create_tables()
gen_x_members(999)
gen_x_employees(999)
gen_x_courses(999)
gen_x_classes(999)
gen_x_transaction(999)
gen_x_attendance(999)
gen_x_equipment(999)
    
print_em_out()
get_totals()
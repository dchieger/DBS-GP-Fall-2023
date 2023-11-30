import mysql.connector
import datetime
from faker import *
import random

connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root_password",
    database="mysql_db"
)

fake = Faker()
cursor = connection.cursor()

def create_members_table():

        create_table_query = """
        CREATE TABLE Members (
            MemberID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            DateOfBirth DATE,
            Gender ENUM('Male', 'Female', 'Non-binary'),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(99),
            Address VARCHAR(255),
            JoiningDate DATE,
            MembershipType VARCHAR(50),
            EmergencyContactName VARCHAR(99),
            EmergencyContactPhone VARCHAR(99)
        )
        """

        cursor.execute(create_table_query)
        connection.commit()
        print("Members - table created successfully!")

def create_employees_table():

        query = """
        CREATE TABLE Employees (
            EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            DateOfBirth DATE,
            Gender ENUM('Male', 'Female', 'Non-binary'),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(15),
            Address VARCHAR(255),
            HireDate DATETIME,
            Salary DECIMAL(10, 2),
            EmergencyContactName VARCHAR(100),
            EmergencyContactPhone VARCHAR(15)
        )
        """

        cursor.execute(query)
        connection.commit()
        print("Employees - table created successfully!")

def create_employee_salary_statistics_table():
    query = """
    CREATE TABLE IF NOT EXISTS EmployeeSalaryStatistics (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        TotalSalary DECIMAL(10, 2),
        AverageSalary DECIMAL(10, 2),
        LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    cursor.execute(query)
    print("Table 'EmployeeSalaryStatistics' created successfully.")

def create_product_inventory_table():
    try:
        create_table_query = """
        CREATE TABLE ProductInventory (
            ProductID INT AUTO_INCREMENT PRIMARY KEY,
            ProductName VARCHAR(100),
            Price DECIMAL(10, 2),
            QuantityInStock INT,
            Supplier VARCHAR(100),
            PurchaseDate DATETIME,
            ExpirationDate DATETIME,
            BarcodeUPC VARCHAR(50)
        )
        """

        cursor.execute(create_table_query)
        connection.commit()
        print("ProductInventory - table created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_equipment_inventory_table():
    try:
        create_table_query = """
        CREATE TABLE EquipmentInventory  (
            EquipmentID INT AUTO_INCREMENT PRIMARY KEY,
            EquipmentName VARCHAR(100),
            Manufacturer VARCHAR(100),
            PurchaseDate DATETIME,
            SerialNumber VARCHAR(50),
            PurchasePrice DECIMAL(10, 2),
            WarrantyExpirationDate DATETIME
        )
        """

        # Execute the query to create the table
        cursor.execute(create_table_query)

        print("Equipment - table created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_transaction_table():
    try:
        create_table_query = """
        CREATE TABLE Transaction (
            TransactionID INT AUTO_INCREMENT PRIMARY KEY,
            TransactionDate DATETIME,
            MemberID INT,
            TransactionStatus VARCHAR(50),
            Amount DECIMAL(10, 2),
            CardType VARCHAR(99),
            CardHolder VARCHAR(99),
            CardNumber VARCHAR(99),
            ExpiryDate VARCHAR(99),
            CVC VARCHAR(99),
            InvoiceReceiptNumber VARCHAR(50)
        )
        """
        #InvoiceReceiptNumber VARCHAR(50), --- random num we can gen
        #TransactionStatus VARCHAR(50), --- completed, pending, canceled 
        # Execute the query to create the table
        cursor.execute(create_table_query)
        connection.commit()
        print("Transaction - table created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_lost_and_found_table():
    try:
        # Define the SQL query to create the "LostAndFound" table
        create_table_query = """
        CREATE TABLE LostAndFound (
            ItemID INT AUTO_INCREMENT PRIMARY KEY,
            ItemName VARCHAR(100),
            DateFound DATE,
            FoundByMember INT,
            FOREIGN KEY (FoundByMember) REFERENCES Members(MemberID)
        )
        """

        # Execute the query to create the table
        cursor.execute(create_table_query)
        connection.commit()
        print("LostAndFound - table created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_visitors_log_table():
    try:
        create_table_query = """
        CREATE TABLE VisitorsLog (
            LogID INT AUTO_INCREMENT PRIMARY KEY,
            MemberID INT,
            CheckInTime DATETIME,
            FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("VisitorsLog - table created successfully")

    except Exception as e:
        print(f"Error occurred: {e}")

def create_classes_table():
    try:
        create_table_query = """
        CREATE TABLE Classes (
            ClassID INT AUTO_INCREMENT PRIMARY KEY,
            ClassName VARCHAR(255),
            ClassTime DATETIME,
            EmployeeID INT,
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Classes - table created successfully")
    except Exception as e:
        print(f"Error occurred: {e}")

def gen_x_members(x):
    genders = ['Male', 'Female', 'Non-binary']
    membership_types = ['Standard', 'Vetran', 'Student']

    for new_member in range(x):
        fn = fake.first_name()
        ln = fake.last_name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        gender = random.choice(genders)
        email = fake.email()
        phone = str(fake.random_number(digits=10, fix_len=True))
        address = fake.address().replace('\n', ', ')
        join_date = fake.date_this_decade() 
        membership_type = random.choice(membership_types)
        emergency_contact_name = fake.name()
        emergency_contact_phone = str(fake.random_number(digits=10, fix_len=True))

        insert_member_query = """
        INSERT INTO Members (
            FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, 
            Address, JoiningDate, MembershipType, EmergencyContactName, EmergencyContactPhone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (fn, ln, dob, gender, email, phone, address, join_date, membership_type, emergency_contact_name, emergency_contact_phone)
        cursor.execute(insert_member_query, data)

    connection.commit()
    print("insert new_member success")

def gen_x_employees(x):

    genders = ['Male', 'Female', 'Non-binary']

    for new_employee in range(x):
        fn = fake.first_name()
        ln = fake.last_name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
        gender = random.choice(genders)
        email = fake.email()
        phone = str(fake.random_number(digits=10, fix_len=True))
        address = fake.address().replace('\n', ', ')
        hire_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        salary = random.uniform(45000, 90000)
        emergency_contact_name = fake.name()
        emergency_contact_phone = str(fake.random_number(digits=10, fix_len=True))

        insert_employee_query = """
        INSERT INTO Employees (
            FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, 
            Address, HireDate, Salary, EmergencyContactName, EmergencyContactPhone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (fn, ln, dob, gender, email, phone, address, hire_date, salary, emergency_contact_name, emergency_contact_phone)
        cursor.execute(insert_employee_query, data)

    connection.commit()
    print("insert new_employee success")

def gen_x_products(x):

    foods = ["Grilled Chicken Breast", "Salad with Mixed Greens", "Brown Rice", "Quinoa Salad", "Protein Shake", "Greek Yogurt", "Oatmeal", "Egg White Omelette", "Avocado Toast", "Lean Turkey Wrap", "Kale Smoothie", "Mixed Berry Parfait", "Almonds", "Hummus and Veggies", "Cottage Cheese", "Whey Protein Powder", "Multivitamin Supplement", "Fish Oil Capsules", "Chia Seeds", "Sweet Potato Fries (baked)", "Steamed Broccoli", "Tuna Salad", "Whole Grain Bread", "Green Tea"][:15]


    for new_product in range(x):
        product_name = random.choice(foods)
        price = round(random.uniform(1.0, 50.0), 2)  
        quantity_in_stock = random.randint(1, 100) 
        supplier = fake.company()
        purchase_date = fake.past_date()  
        expiration_date = fake.future_date() 
        barcode_upc = str(fake.unique.random_number(digits=12))  # UPC barcodes are typically 12 digits long

        insert_product_query = """
        INSERT INTO ProductInventory (
            ProductName, Price, QuantityInStock, Supplier, PurchaseDate, 
            ExpirationDate, BarcodeUPC
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (product_name, price, quantity_in_stock, supplier, purchase_date, expiration_date, barcode_upc)
        cursor.execute(insert_product_query, data)

    connection.commit()
    print("insert new_product success")

def gen_x_equipment(x):

    equipment = ['Dumbbells', 'Barbells', 'Weight Plates', 'Kettle Bells', 'Medicine Balls', 'Weighted Balls', 'Resistance Bands', 'Sandbags', 'Jump Rope', 'Stretch Bars' ]
    equipment_manufacturers = ["IronFlex Tech", "PowerPulse Dynamics", "GymGear Innovations", "EpicFit Systems", "Titanic Fitness Solutions", "Zenith Muscle Machines", "Quantum Liftware", "AeroFlex Athletics", "HyperDrive Fitness", "XtremeForge Equipment"]

    for new_equipment in range(x):
        equipment_name = random.choice(equipment)
        manufacturer = random.choice(equipment_manufacturers)
        purchase_date = fake.past_date(start_date="-10y") 
        serial_number = fake.unique.random_number(digits=24)
        purchase_price = round(random.uniform(100.0, 500.0), 2) 
        warranty_expiration_date = fake.future_date(end_date="+5y")

        insert_equipment_query = """
        INSERT INTO EquipmentInventory (
            EquipmentName, Manufacturer, PurchaseDate, SerialNumber, 
            PurchasePrice, WarrantyExpirationDate
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (equipment_name, manufacturer, purchase_date, serial_number, purchase_price, warranty_expiration_date)
        cursor.execute(insert_equipment_query, data)

    connection.commit()
    print("insert new_equipment success")

def gen_x_transactions(x):
    transaction_statuses = ['Completed', 'Pending', 'Failed']


    for new_transaction in range(x):
        cc_transaction = fake.credit_card_full()
        transaction_date = fake.date_time_this_year()
        member_id = random.randint(1, 100)  # Random member ID between 1 and 100
        transaction_status = random.choice(transaction_statuses)
        amount = round(random.uniform(1.0, 500.0), 2)  # Random transaction amount between 1 and 1000
        card_type, card_holder, card_number, expiry_date, cvc = cc_transaction.split('\n')
        card_type = card_type.strip()
        card_holder = card_holder.strip()
        card_number = card_number.strip()
        expiry_date = expiry_date.strip()
        cvc = cvc.strip()
        invoice_receipt_number = fake.unique.random_number(digits=8)

        insert_transaction_query = """
        INSERT INTO Transaction (
            TransactionDate, MemberID, TransactionStatus, Amount, CardType, 
            CardHolder, CardNumber, ExpiryDate, CVC, InvoiceReceiptNumber
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (transaction_date, member_id, transaction_status, amount, card_type, card_holder, card_number, expiry_date, cvc, invoice_receipt_number)
        cursor.execute(insert_transaction_query, data)

    connection.commit()
    print("insert new_transaction success")

def gen_x_lost_and_found_items(x):
    
    lost_and_found_items = ['Wallet', 'Keys', 'Phone', 'Jacket', 'Umbrella', 'Backpack', 'Glasses', 'Watch', 'Earrings', 'Ring', 'Hat', 'Scarf', 'Gloves', 'Headphones', 'Water Bottle']

    for new_item in range(x):
        item_name = random.choice(lost_and_found_items)
        date_found = fake.past_date(start_date="-1y")  # Item found within the last year
        found_by_member = random.randint(1, 3)  # Random member ID between 1 and 100

        insert_item_query = """
        INSERT INTO LostAndFound (
            ItemName, DateFound, FoundByMember
        ) VALUES (%s, %s, %s)
        """
        data = (item_name, date_found, found_by_member)
        cursor.execute(insert_item_query, data)

    connection.commit()
    print("insert new_lost_item success")

def gen_x_visitors_log_entries(x):
    for new_entry in range(x):
        member_id = random.randint(1, 100)  # Random member ID between 1 and 100
        check_in_time = fake.date_time_this_year()  # Check-in time within the current year

        insert_log_entry_query = """
        INSERT INTO VisitorsLog (
            MemberID, CheckInTime
        ) VALUES (%s, %s)
        """
        data = (member_id, check_in_time)
        cursor.execute(insert_log_entry_query, data)

    connection.commit()
    print("insert new_visitors_log_entry success")

def gen_x_classes(x):
    
    class_names = ['Yoga', 'Pilates', 'Zumba', 'Kickboxing', 'Spinning', 'CrossFit', 'Boot Camp', 'Aerobics']

    for new_class in range(x):
        class_name = random.choice(class_names)
        class_time = fake.date_time_this_year()  # Class time within the current year
        employee_id = random.randint(1, 100)  # Random employee ID between 1 and 100

        insert_class_query = """
        INSERT INTO Classes (
            ClassName, ClassTime, EmployeeID
        ) VALUES (%s, %s, %s)
        """
        data = (class_name, class_time, employee_id)
        cursor.execute(insert_class_query, data)

    connection.commit()
    print("insert new_class success")

def genesis():
    #create our tables for data insertion
    create_members_table()
    create_employees_table()
    create_employee_salary_statistics_table()

    #TRIGGER
    create_salary_statistics_trigger()
    create_increase_salaries_procedure()

    create_product_inventory_table()
    create_equipment_inventory_table()
    create_transaction_table()
    create_lost_and_found_table()
    create_visitors_log_table()
    create_classes_table()


    #There must be atleast 100 employees and members in our database
    #The func of the rest of the generation classes grabs a random number from 1-100 corresponding to the member and employee id
    gen_x_members(100)
    gen_x_employees(1)
    gen_x_employees(99)


    gen_x_products(50)
    gen_x_equipment(50)
    gen_x_transactions(50)
    gen_x_lost_and_found_items(50)
    gen_x_visitors_log_entries(50)
    gen_x_classes(50)

def printer(table_name=None):

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
    
    print(f'Total records in Members Table: {total_rec_members}')
    print(f'Total records in Employees Table: {total_rec_employees}')
    print(f'Total records in ProductInventory Table: {total_rec_product_inventory}')
    print(f'Total records in EquipmentInventory Table: {total_rec_equipment_inventory}')
    print(f'Total records in Transactions Table: {total_rec_transaction}')
    print(f'Total records in LostAndFound Table: {total_rec_lost}')
    print(f'Total records in VisitorsLog Table: {total_rec_visitors}')
    print(f'Total records in Classes Table: {total_rec_classes}')
    print(f'Total records in all tables: {total_rec_all}')

    if table_name:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        for record in records:
            print(record)
    elif table_name is None:
        print("No arguments provided for specific print")

#First requirement
#How many classes these employees are actually teaching
def report_employee_classes():
    query = """
    SELECT E.EmployeeID, E.FirstName, E.LastName, COUNT(C.ClassID) as NumberOfClasses
    FROM Employees E
    JOIN Classes C ON E.EmployeeID = C.EmployeeID
    GROUP BY E.EmployeeID, E.FirstName, E.LastName;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#create a view and give the average of the numbers of employees who taught more than one class
def create_employee_classes_view():
    create_view_query = """
    CREATE VIEW EmployeeClassesView AS
    SELECT E.EmployeeID, E.FirstName, E.LastName, COUNT(C.ClassID) as NumberOfClasses
    FROM Employees E
    JOIN Classes C ON E.EmployeeID = C.EmployeeID
    GROUP BY E.EmployeeID, E.FirstName, E.LastName;
    """
    try:
        cursor.execute(create_view_query)
        print("View 'EmployeeClassesView' created successfully.")
    except mysql.connector.ProgrammingError:
        print("View 'EmployeeClassesView' already exists.")
#requirment 4
def view_employee_classes_view():
    query = "SELECT * FROM EmployeeClassesView"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Requirement 2
def get_employees_with_above_average_salary():
    query = """
    SELECT EmployeeID, FirstName, LastName, Salary
    FROM Employees
    WHERE Salary > (SELECT AVG(Salary) FROM Employees)
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#requirement 5
#A stored procedure that can be called by a query to perform some math operation on the data and returns a value(s).
def create_total_transaction_amount_procedure():
    query = """
    CREATE PROCEDURE TotalTransactionAmount()
    BEGIN
        SELECT SUM(Amount) AS TotalAmount FROM Transaction;
    END;
    """
    try:
        cursor.execute(query)
        print("Stored procedure 'TotalTransactionAmount' created successfully.")
    except mysql.connector.ProgrammingError:
        print("Stored procedure 'TotalTransactionAmount' already exists.")

def get_total_transaction_amount():
    # Ensure the stored procedure exists
    create_total_transaction_amount_procedure()

    # Call the stored procedure
    cursor.callproc('TotalTransactionAmount')

    # Fetch the result
    result = []
    for result_set in cursor.stored_results():
        result = result_set.fetchall()

    # Return the total transaction amount
    if result:
        total_amount = result[0][0]
        return total_amount
    else:
        return None

#Requirement 6
# (X1) (Xs connected) A stored procedure that uses a cursor to access and manipulate (update/change) data.
def create_increase_salaries_procedure():
    query = """
    CREATE PROCEDURE IncreaseSalaries(IN increase_percentage DECIMAL(5, 2))
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE emp_id INT;
        DECLARE emp_salary DECIMAL(10, 2);
        DECLARE cur CURSOR FOR SELECT EmployeeID, Salary FROM Employees;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        OPEN cur;

        read_loop: LOOP
            FETCH cur INTO emp_id, emp_salary;
            IF done THEN
                LEAVE read_loop;
            END IF;
            UPDATE Employees SET Salary = emp_salary * (1 + increase_percentage / 100) WHERE EmployeeID = emp_id;
        END LOOP;

        CLOSE cur;
    END;
    """
    try:
        cursor.execute(query)
        print("Stored procedure 'IncreaseSalaries' created successfully.")
    except mysql.connector.ProgrammingError:
        print("Stored procedure 'IncreaseSalaries' already exists.")

# (X2) demo the procedure
def call_increase_salaries_procedure(increase_percentage):
    query = "CALL IncreaseSalaries(%s)"
    data = (increase_percentage,)  # wrap the integer in a tuple
    cursor.execute(query, data)
    print(f"Stored procedure 'IncreaseSalaries' called with parameter {increase_percentage}.")

# (X3) actually show the procedure works
def get_employee_salaries():
    query = "SELECT FirstName, LastName, Salary FROM Employees LIMIT 5"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# (Y1) Create a trigger to track the total and avg salary of all employees and log it 
def create_salary_statistics_trigger():
    genesis_query = '''
    INSERT INTO EmployeeSalaryStatistics (TotalSalary, AverageSalary)
    VALUES (0, 0)
    ON DUPLICATE KEY UPDATE ID = ID;
    '''
    try:
        cursor.execute(genesis_query)
        print("genesis_query successfully. OKOKOK")
    except mysql.connector.ProgrammingError:
        print("genesis_query FAILURE")

    query = """
    DELIMITER //
    CREATE TRIGGER UpdateSalaryStatistics
    AFTER INSERT ON Employees
    FOR EACH ROW
    BEGIN
        DECLARE totalSalary DECIMAL(10, 2);
        DECLARE averageSalary DECIMAL(10, 2);

        SELECT SUM(Salary) INTO totalSalary FROM Employees;
        SELECT AVG(Salary) INTO averageSalary FROM Employees;

        INSERT INTO EmployeeSalaryStatistics (TotalSalary, AverageSalary)
        VALUES (totalSalary, averageSalary);
    END //
    DELIMITER;
    """
    try:
        cursor.execute(query)
        print("Trigger 'update_salary_statistics' created successfully.")
    except mysql.connector.ProgrammingError:
        print("Trigger 'update_salary_statistics' already exists.")

# (Y2) View the triggers and how they have effected the database      
def get_last_salary_statistics():
    query = "SELECT * FROM EmployeeSalaryStatistics ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    return result

#(Y3)

#genesis()
view_employee_classes_view()
create_increase_salaries_procedure()
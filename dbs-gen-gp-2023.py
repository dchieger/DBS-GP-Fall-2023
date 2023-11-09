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


equipment = ['Dumbbells', 'Barbells', 'Weight Plates', 'Kettle Bells', 'Medicine Balls', 'Weighted Balls', 'Resistance Bands', 'Sandbags', 'Jump Rope', 'Stretch Bars' ]

machines = ['Treadmill', 'Elliptical', 'Stationary Bike', 'Rowing Machine', 'Stair Climber', 'Chest Press Machine', 'Lat Pulldown Machine', 'Cable Machine', 'Leg Press Machine']

cursor = connection.cursor()

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
        card_type, card_holder, card_number, expiry_date, cvc = cc_transaction.split('\n')
        card_type = card_type.strip()
        card_holder = card_holder.strip()
        card_number = card_number.strip()
        expiry_date = expiry_date.strip()
        cvc = cvc.strip()
    
        insert_transaction_query = "INSERT INTO transactions (card_type, card_holder, card_number, expiry_date, cvc) VALUES (%s, %s, %s, %s, %s)"
        data = (card_type, card_holder, card_number, expiry_date, cvc)
        cursor.execute(insert_transaction_query, data)
    
    connection.commit()
    print("insert new_transaction success")
    
def gen_x_equipment(x):
    
    characters = string.ascii_letters + string.digits
    
    for new_equipment in range(x):
        equipment_name = random.choice(equipment)
        sn = ''.join(random.choice(characters) for _ in range(28))
        
        
        insert_equipment_query = "INSERT INTO equipment (name, sn) VALUES (%s, %s)"
        data = (equipment_name, sn)
        cursor.execute(insert_equipment_query, data)
        
    connection.commit()
    print("insert new_equipment success")
    




def create_tables():
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        phone VARCHAR(255),
        email VARCHAR(255),
        dob DATE,
        join_date DATE,
        address TEXT,
        member_uuid VARCHAR(36)
    )
    """)
    cursor.fetchall()
    connection.commit()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        card_type VARCHAR(255),
        card_holder VARCHAR(255),
        card_number VARCHAR(255),
        expiry_date VARCHAR(10),
        cvc VARCHAR(10)
    )
    """)
    cursor.fetchall()
    connection.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        sn VARCHAR(255)
    )
    """)
    cursor.fetchall()
    connection.commit()
    print('tables created successfully')
    
def drop_table(table_name):
    
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_query)
    
def print_em_out():
    cursor.execute("SELECT * FROM members")
    members_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM equipment")
    equipment_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM transactions")
    transactions_data = cursor.fetchall()
    
    total_rec = 0
    
    for row in members_data:
        print(row)
        total_rec +=1
        
    for row in equipment_data:
        print(row)  
        total_rec +=1
        
    for row in transactions_data:
        print(row)
        total_rec +=1
        
    print('Total records')
    print(total_rec)
        
        
#create_tables()
gen_x_members(99)
gen_x_transaction(99)
gen_x_equipment(99)
print_em_out()



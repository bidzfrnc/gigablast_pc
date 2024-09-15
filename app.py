from flask import Flask, render_template, request, redirect, url_for
# importing required library
import string
import random
import mysql.connector
#the connection object
myconn = mysql.connector.connect(
host ="localhost",
user ="root",
passwd ="",
database = "my_miniproj_db"
)

cursorObject = myconn.cursor()
cursorObject.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        product_price DECIMAL(10, 2) NOT NULL,
        product_stock INT NOT NULL,
        product_image VARCHAR(255),
        product_specs TEXT
    )
''')

cursorObject.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        transaction_id VARCHAR(15) PRIMARY KEY,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255),
        customer_phone_no VARCHAR(255),
        customer_address TEXT,
        product_name VARCHAR(255) NOT NULL,
        product_image VARCHAR(255),
        product_price DECIMAL(10, 2) NOT NULL,
        product_quantity INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        payment_method VARCHAR(255) NOT NULL
    )
''')
myconn.commit()


app = Flask(__name__)
app.static_folder = 'static' 
app.static_url_path = '/static'  

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/viewproducts')
def viewproducts():
    cursorObject = myconn.cursor()
    select_query = "SELECT product_name, product_image, product_price, product_stock, product_specs FROM products"
    cursorObject.execute(select_query)
    product_data = cursorObject.fetchall()
    return render_template('viewproducts.html', product_data=product_data)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        transaction_id = generate_transaction_id()
        name = request.form.get('name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        product_name = request.form.get('product_name')
        product_image = request.form.get('product_image')
        product_price = float(request.form.get('product_price'))
        quantity = int(request.form.get('quantity'))
        total_price = product_price * quantity

        if not name or not email or not phone_no or not address or not payment_method:
            return "Please complete the form."

        insert_query = '''
        INSERT INTO orders (transaction_id, customer_name, customer_email, customer_phone_no, customer_address, product_name, product_image, product_price, product_quantity, total_price, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (transaction_id, name, email, phone_no, address, product_name, product_image, product_price, quantity, total_price, payment_method)
    cursorObject.execute(insert_query, values)
    myconn.commit() 

    return redirect(url_for('display_orders'))




def generate_transaction_id():
    characters = string.ascii_letters + string.digits
    while True:
        transaction_id = ''.join(random.choice(characters) for _ in range(15))
        cursorObject.execute('SELECT COUNT(*) FROM orders WHERE transaction_id = %s', (transaction_id,))
        count = cursorObject.fetchone()[0]
        if count == 0:
            return transaction_id.upper()

@app.route('/order', methods=['GET'])
def display_orders():
    if request.method == 'GET':
        select_query = '''
            SELECT transaction_id, customer_name, customer_email, customer_phone_no, customer_address,
            product_name, product_image, product_price, product_quantity, total_price, payment_method
            FROM orders
        '''
        cursorObject.execute(select_query)
        orders_data = cursorObject.fetchall()
        return render_template('order.html', orders=orders_data)
    else:
        return "Invalid request method"


# editing order
@app.route('/update_order/<transaction_id>', methods=['GET'])
def display_update_form(transaction_id):
    try:
        select_query = '''
            SELECT transaction_id, customer_name, customer_email, customer_phone_no, customer_address,
            product_name, product_image, product_price, product_quantity, total_price, payment_method
            FROM orders
            WHERE transaction_id = %s
        '''
        cursorObject.execute(select_query, (transaction_id,))
        order_data = cursorObject.fetchone()

        return render_template('order.html', order=order_data)
    except mysql.connector.Error as err:
        # Handle any potential database errors here
        return f"Error fetching order: {err}"
@app.route('/update_order', methods=['POST'])
def update_order():
    try:
        if request.method == 'POST':
            transaction_id = request.form.get('transaction_id')
            customer_name = request.form.get('customer_name')
            customer_email = request.form.get('customer_email')
            customer_phone_no = request.form.get('customer_phone_no')
            customer_address = request.form.get('customer_address')
            product_name = request.form.get('product_name')
            product_image = request.form.get('product_image')
            product_price = float(request.form.get('product_price'))  
            product_quantity = int(request.form.get('product_quantity')) 
            total_price = request.form.get('total_price')
            payment_method = request.form.get('payment_method')
            

            total_price = product_price * product_quantity

            values = (
                customer_name,
                customer_email,
                customer_phone_no,
                customer_address,
                product_name,
                product_image,
                product_price,
                product_quantity,
                total_price,
                payment_method,
                transaction_id 
            )


            update_query = '''
                UPDATE orders
                SET
                    customer_name = %s,
                    customer_email = %s,
                    customer_phone_no = %s,
                    customer_address = %s,
                    product_name = %s,
                    product_image = %s,
                    product_price = %s,
                    product_quantity = %s,
                    total_price = %s,
                    payment_method = %s
                WHERE transaction_id = %s
            '''

            cursorObject.execute(update_query, values)
            myconn.commit()  
            return redirect(url_for('display_orders'))
    except mysql.connector.Error as err:
        
        return f"Error updating order: {err}"

# delete
@app.route('/delete_order/<transaction_id>', methods=['GET'])
def delete_order(transaction_id):
    try:
        cursorObject.execute('DELETE FROM orders WHERE transaction_id = %s', (transaction_id,))
        myconn.commit()
        
        return redirect(url_for('display_orders'))
    except mysql.connector.Error as err:
        
        return f"Error deleting order: {err}"
    
if __name__ == '__main__':
    app.run(debug = True)

from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import get_db_connection
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (username, password, name) VALUES (%s, %s, %s)", (username, password, name))
        conn.commit()
        user_id = cursor.lastrowid

        if role == 'customer':
            customer_id = cursor.lastrowid
            cursor.execute("INSERT INTO Customer (customer_id, user_id) VALUES (%s, %s)", (customer_id, user_id))
        else:
            manager_id = cursor.lastrowid
            cursor.execute("INSERT INTO Manager (manager_id, user_id) VALUES (%s, %s)", (manager_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT * FROM Customer WHERE user_id = %s", (user['user_id'],))
            customer = cursor.fetchone()
            session['user_id'] = user['user_id']
            if customer:
                session['role'] = 'customer'
                cursor.close()
                conn.close()
                return redirect('/customer')
            else:
                cursor.execute("SELECT * FROM Manager WHERE user_id = %s", (user['user_id'],))
                manager = cursor.fetchone()
                session['role'] = 'manager'
                cursor.close()
                conn.close()
                return redirect('/restaurant')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/customer')
def customer_home():
    if session.get('role') != 'customer':
        return redirect('/')
    return render_template('customer_dashboard.html')

@app.route('/customer/search', methods=['GET'])
def customer_search():
    keyword = request.args.get('keyword', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.restaurant_id, r.name, r.cuisine_type, r.adress,
        COUNT(rt.rating_id) as total_reviews,
        ROUND(AVG(rt.rate), 1) as avg_rating
        FROM Restaurant r
        LEFT JOIN Keyword k ON r.restaurant_id = k.restaurant_id
        LEFT JOIN Rating rt ON r.restaurant_id = rt.restaurant_id
        WHERE k.key_text LIKE %s
        GROUP BY r.restaurant_id
    """, (f"%{keyword}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('search_results.html', restaurants=results, keyword=keyword)

@app.route('/customer/search/menu', methods=['GET'])
def search_menu():
    keyword = request.args.get('keyword')
    if not keyword:
        return redirect('/customer/search')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT restaurant_id 
        FROM Keyword 
        WHERE key_text = %s
    """, (keyword,))
    rows = cursor.fetchall()
    restaurant_ids = [row['restaurant_id'] for row in rows]

    items = []
    if restaurant_ids:
        format_strings = ','.join(['%s'] * len(restaurant_ids))
        cursor.execute(f"""
            SELECT 
                m.item_id, m.name, m.description, m.price, m.dis_percentage,m.dis_end_date,
                CASE
                    WHEN m.dis_percentage IS NOT NULL AND m.dis_end_date >= CURDATE()
                    THEN ROUND(m.price * (1 - m.dis_percentage / 100), 2)
                    ELSE m.price
                END AS effective_price,
                r.name AS restaurant_name
            FROM MenuItem m
            JOIN Restaurant r ON m.restaurant_id = r.restaurant_id
            WHERE m.restaurant_id IN ({format_strings})
        """, tuple(restaurant_ids))
        items = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('customer_menu.html', items=items, keyword=keyword, now=datetime.now)



@app.route('/customer/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    quantity = int(request.form.get('quantity', 1))
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    # customer ID bul
    cursor.execute("SELECT customer_id FROM Customer WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Customer not found", 404
    customer_id = row['customer_id']


    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cart_id, quantity FROM Cart 
        WHERE customer_id = %s AND item_id = %s AND status = 'preparing'
    """, (customer_id, item_id))
    existing = cursor.fetchone()

    if existing:
        cart_id, current_quantity = existing
        new_quantity = current_quantity + quantity
        cursor.execute("""
            UPDATE Cart SET quantity = %s 
            WHERE cart_id = %s
        """, (new_quantity, cart_id))
    else:
        cursor.execute("""
            INSERT INTO Cart (customer_id, restaurant_id, item_id, quantity, status)
            VALUES (%s, (SELECT restaurant_id FROM MenuItem WHERE item_id = %s), %s, %s, 'preparing')
        """, (customer_id, item_id, item_id, quantity))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/customer/cart/view')


@app.route('/customer/cart/view')
def view_cart():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT customer_id FROM Customer WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Customer not found", 404
    customer_id = row['customer_id']

    cursor.execute("""
        SELECT c.cart_id, m.name, c.quantity, m.price, (c.quantity * m.price) AS total
        FROM Cart c
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE c.customer_id = %s AND c.status = 'preparing'
    """, (customer_id,))
    cart_items = cursor.fetchall()

    total_price = sum(item['total'] for item in cart_items)

    cursor.close()
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)



@app.route('/customer/cart/checkout', methods=['POST'])
def checkout_cart():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT customer_id FROM Customer WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Customer not found", 404
    customer_id = row['customer_id']

    cursor.execute("""
        UPDATE Cart 
        SET status = 'pending' 
        WHERE customer_id = %s AND status = 'preparing'
    """, (customer_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect('/customer/cart/view')

@app.route('/customer/rate', methods=['GET', 'POST'])
def rate_order():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get customer ID
    cursor.execute("SELECT customer_id FROM Customer WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Customer not found", 404
    customer_id = row['customer_id']

    if request.method == 'POST':
        cart_id = request.form['cart_id']
        restaurant_id = request.form['restaurant_id']
        rating = int(request.form['rating'])
        comment = request.form['comment'].strip()

        cursor.execute("""
            SELECT timestamp FROM Cart 
            WHERE cart_id = %s AND customer_id = %s AND status = 'accepted'
        """, (cart_id, customer_id))
        result = cursor.fetchone()

        if result:
            timestamp = result['timestamp']
            allow_comment = datetime.now() <= timestamp + timedelta(hours=24)

            cursor.execute("SELECT * FROM Rating WHERE cart_id = %s", (cart_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO Rating (rate, comment, customer_id, restaurant_id, cart_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    rating,
                    comment if allow_comment else None,
                    customer_id,
                    restaurant_id,
                    cart_id
                ))
                conn.commit()

        cursor.close()
        conn.close()
        return redirect('/customer/rate')

    cursor.execute("""
        SELECT c.cart_id, r.name AS restaurant_name, r.restaurant_id, m.name AS item_name, c.quantity, c.timestamp
        FROM Cart c
        JOIN Restaurant r ON c.restaurant_id = r.restaurant_id
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE c.customer_id = %s AND c.status = 'accepted'
        AND c.cart_id NOT IN (SELECT cart_id FROM Rating)
    """, (customer_id,))
    carts = cursor.fetchall()

    cursor.execute("""
        SELECT r.name AS restaurant_name, m.name AS item_name, rt.rate, rt.comment, c.timestamp
        FROM Rating rt
        JOIN Cart c ON rt.cart_id = c.cart_id
        JOIN Restaurant r ON rt.restaurant_id = r.restaurant_id
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE rt.customer_id = %s
        ORDER BY rt.rating_id DESC
    """, (customer_id,))
    ratings = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('rate.html', carts=carts, ratings=ratings, now=datetime.now, timedelta=timedelta)



@app.route('/restaurant')
def restaurant_home():
    if session.get('role') != 'manager':
        return redirect('/')
    return render_template('restaurant_dashboard.html')

@app.route('/restaurant/menu', methods=['GET', 'POST'])
def manage_menu():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("SELECT manager_id FROM Manager WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return "Manager not found", 404
        manager_id = row['manager_id']

        cursor.execute("SELECT restaurant_id FROM Restaurant WHERE manager_id = %s", (manager_id,))
        row = cursor.fetchone()
        if not row:
            return "Restaurant not found", 404
        restaurant_id = row['restaurant_id']

        if request.method == 'POST':
            name = request.form.get('name', '')
            description = request.form.get('description', '')
            price = request.form.get('price', '')
            image = request.form.get('image', '')
            cursor.execute(
                "INSERT INTO MenuItem (restaurant_id, name, description, price, image) VALUES (%s, %s, %s, %s, %s)",
                (restaurant_id, name, description, price, image)
            )
            item_id = cursor.lastrowid
            conn.commit()

        cursor.execute("SELECT * FROM MenuItem WHERE restaurant_id = %s", (restaurant_id,))
        items = cursor.fetchall()
        return render_template('menu.html', items=items)

    except Exception as err:
        print(f"Error: {err}")
        return "An error occurred", 500

    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/restaurant/keywords', methods=['GET', 'POST'])
def add_keyword():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT manager_id FROM Manager WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Manager not found", 404
    manager_id = row['manager_id']

    cursor.execute("SELECT restaurant_id FROM Restaurant WHERE manager_id = %s", (manager_id,))
    row = cursor.fetchone()
    if not row:
        return "Restaurant not found", 404
    restaurant_id = row['restaurant_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        text = request.form.get('key_text', '')
        if text:
            cursor.execute(
                "INSERT INTO Keyword (key_text, manager_id, restaurant_id) VALUES (%s, %s, %s)",
                (text, manager_id, restaurant_id)
            )
            conn.commit()
        cursor.close()
        conn.close()
        return redirect('/restaurant/keywords')
    else:
        cursor.execute("SELECT * FROM Keyword WHERE restaurant_id = %s", (restaurant_id,))
        keywords = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('keywords.html', keywords=keywords)
    


    

@app.route('/restaurant/orders')
def view_orders():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT manager_id FROM Manager WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return "Manager not found", 404
    manager_id = row['manager_id']

    cursor.execute("SELECT restaurant_id FROM Restaurant WHERE manager_id = %s", (manager_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return "Restaurant not found", 404
    restaurant_id = row['restaurant_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.cart_id, c.customer_id, m.name AS item_name, c.quantity
        FROM Cart c
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE c.restaurant_id = %s AND c.status = 'pending'
    """, (restaurant_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/restaurant/orders/accept/<int:cart_id>')
def accept_order(cart_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Cart SET status = 'accepted', timestamp = NOW() WHERE cart_id = %s", (cart_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/restaurant/orders')


@app.route('/restaurant/stats')
def view_stats():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT manager_id FROM Manager WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Manager not found", 404
    manager_id = row['manager_id']

    cursor.execute("SELECT restaurant_id FROM Restaurant WHERE manager_id = %s", (manager_id,))
    row = cursor.fetchone()
    if not row:
        return "Restaurant not found", 404
    restaurant_id = row['restaurant_id']

    cursor.execute("""
        SELECT COUNT(*) AS total_orders,
               SUM(c.quantity * m.price) AS total_revenue
        FROM Cart c
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE c.restaurant_id = %s AND c.status = 'accepted'
    """, (restaurant_id,))
    summary = cursor.fetchone()

    cursor.execute("""
        SELECT m.name, SUM(c.quantity) AS total_sold, SUM(c.quantity * m.price) AS revenue
        FROM Cart c
        JOIN MenuItem m ON c.item_id = m.item_id
        WHERE c.restaurant_id = %s AND c.status = 'accepted'
        GROUP BY m.item_id
    """, (restaurant_id,))
    item_stats = cursor.fetchall()

    last_month = datetime.now() - timedelta(days=30)
    cursor.execute("""
    SELECT u.name AS customer_name, c.customer_id, COUNT(*) AS order_count
    FROM Cart c
    JOIN Customer cu ON c.customer_id = cu.customer_id
    JOIN User u ON cu.user_id = u.user_id
    WHERE c.restaurant_id = %s AND c.status = 'accepted' AND c.timestamp >= %s
    GROUP BY c.customer_id
    ORDER BY order_count DESC
    LIMIT 1
""", (restaurant_id, last_month))
    top_customer = cursor.fetchone()

    cursor.execute("""
    SELECT c.cart_id, c.customer_id, u.name AS customer_name,
           m.name AS item_name, m.price, c.quantity,
           (c.quantity * m.price) AS total, c.timestamp
    FROM Cart c
    JOIN MenuItem m ON c.item_id = m.item_id
    JOIN Customer cu ON c.customer_id = cu.customer_id
    JOIN User u ON cu.user_id = u.user_id
    WHERE c.restaurant_id = %s AND c.status = 'accepted' AND c.timestamp >= %s
    ORDER BY total DESC
    LIMIT 1
""", (restaurant_id, last_month))
    high_value_cart = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('stats.html',
                           summary=summary,
                           item_stats=item_stats,
                           top_customer=top_customer,
                           high_value_customer=high_value_cart)


@app.route('/restaurant/discounts', methods=['GET', 'POST'])
def manage_discounts():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT manager_id FROM Manager WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        return "Manager not found", 404
    manager_id = row['manager_id']

    cursor.execute("SELECT restaurant_id FROM Restaurant WHERE manager_id = %s", (manager_id,))
    row = cursor.fetchone()
    if not row:
        return "Restaurant not found", 404
    restaurant_id = row['restaurant_id']

    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        dis_percentage = float(request.form['dis_percentage'])
        dis_end_date = request.form['dis_end_date']  # yyyy-mm-dd

        cursor.execute("""
            UPDATE MenuItem
            SET dis_percentage = %s, dis_end_date = %s
            WHERE item_id = %s AND restaurant_id = %s
        """, (dis_percentage, dis_end_date, item_id, restaurant_id))
        conn.commit()

    cursor.execute("SELECT * FROM MenuItem WHERE restaurant_id = %s", (restaurant_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('manage_discounts.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)

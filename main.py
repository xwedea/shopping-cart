from http.client import REQUEST_URI_TOO_LONG
import re
from flask import Flask, session, render_template, redirect, url_for, request
# from ds import products
import sqlite3
from livereload import Server
import re
import time

app = Flask('app')
app.secret_key = "CHANGE ME, ok"

@app.route('/')
def main_page():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()
	
	args = request.args
	args.to_dict()
	
	if ("category" in args.keys()):
		category = args["category"]
		cursor.execute("SELECT * FROM product WHERE category=?", (category,))
	else:
		cursor.execute("SELECT * FROM product;")

	products = cursor.fetchall()

	return render_template("home.html", products=products)

@app.route('/product')
def product():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	args = request.args
	args.to_dict()

	if "name" in args.keys():
		name = args["name"]
		cursor.execute("SELECT * FROM product WHERE name=?", (name,))
		product = cursor.fetchone()
	elif "id" in args.keys():
		id = args["id"]
		cursor.execute("SELECT * FROM product WHERE id=?", (id,))
		product = cursor.fetchone()
	
	if product:
		return render_template("product.html", product=product)
	else:
		return render_template("error.html")

@app.route('/add-to-cart', methods=["POST","GET"])
def add_to_cart():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	id = request.form["product-id"]
	name = request.form["product-name"]

	cart = session["cart"]
	print(request.form)
	if (id in cart.keys()):
		cart[id]["quantity"] += 1
	else:
		cart[id] = {
			"name": name,
			"quantity": 1
		}
	session["cart"] = cart
	
	return redirect("/cart")

@app.route('/login', methods=["GET", "POST"])
def login():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
		user = cursor.fetchone()

		if user:
			session["email"] = email
			session["name"] = user["name"]
			session["cart"] = {}
			return redirect("/")
		else:
			error = "Invalid email or password!"
			return render_template("login.html", error=error)
		
	return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		name = request.form["name"]

		pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
		if not re.match(pat, email):
			error = "Invalid email!"
			return render_template("signup.html", error=error)
		elif len(password) < 4:
			error = "Password length must be at least 4"
			return render_template("signup.html", error=error)
		elif name == "":
			error = "Name cannot be blank!"
			return render_template("signup.html", error=error)
		else:

			cursor.execute("INSERT INTO user VALUES (?,?,?)", (email, name, password))
			connection.commit()

			error = "Account succesfully created!"
			return render_template("login.html", error=error)
		
	return render_template("signup.html")

@app.route('/cart', methods=["POST", "GET"])
def cart():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	msg = ""

	if request.method == "GET":
		if session.get("email"):
			cart = session["cart"]
			print(cart)
			print(type(cart))
			return render_template("cart.html", cart=cart)
		else:
			return redirect("login")
	else: # POST
		cart = session["cart"]
		if request.form["action"] == "checkout":
			total = 0
			cur_time = time.strftime('%Y-%m-%d %H:%M:%S')

			for id in cart.keys():
				cursor.execute("select * from product where id = ?", (id,))
				product = cursor.fetchone()
				new_qty = int(request.form["quantity-" + str(id)])	
				if new_qty > product["stock"]:
					msg = f"There are {product['stock']} {product['name']} in stock! You specified {new_qty}"
					return render_template("cart.html", cart=cart, msg=msg)
				elif new_qty < 0:
					msg = f"We don't know how to deliver {new_qty} {product['name']}"
					return render_template("cart.html", cart=cart, msg=msg)
			
			# if no error in quantities -> checkout
			for id in cart.keys():
				cursor.execute("select * from product where id = ?", (id,))
				product = cursor.fetchone()
				new_qty = int(request.form["quantity-" + str(id)])

				total += new_qty * product["price"]
				cursor.execute("update product set stock = ? where id = ?", (product['stock']-new_qty, id))
				cursor.execute("insert into order_product values (?,?,?,?)", (session["email"],cur_time,id,new_qty))
				connection.commit()

				session["cart"] = {}

			
			print(cur_time)
			cursor.execute("insert into orders values (?,?,?)", (session["email"], cur_time, total))
			connection.commit()
			

		elif request.form["action"] == "update":
			copy_cart = cart.copy()
			for id in copy_cart:
				cursor.execute("select * from product where id = ?", (id,))
				product = cursor.fetchone()
				new_qty = int(request.form["quantity-" + str(id)])
				if (new_qty == 0):
					cart.pop(id)
					session["cart"] = cart
				elif new_qty > product["stock"]:
					msg = f"There are {product['stock']} {product['name']} in stock! You specified {new_qty}"
				elif new_qty < 0:
					msg = f"We don't know how to deliver {new_qty} {product['name']}"
				else: # VALID INPUT
					cart[id]["quantity"] = new_qty
					session["cart"] = cart

	cart = session["cart"]
		
	return render_template("cart.html", cart=cart, msg=msg)


@app.route('/orders')
def orders():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	if session.get("email"):
		email = session["email"]
		cursor.execute("SELECT * FROM orders JOIN order_product ON orders.order_date = order_product.date_of_order JOIN product ON order_product.product_id = product.id WHERE customer_email=?", (email,))
		products = cursor.fetchall()
		cursor.execute("SELECT * FROM orders")
		orders = cursor.fetchall()
		return render_template("orders.html", products=products, orders=orders)
	else:
		return redirect("/login")



@app.route('/logout', methods=["POST"])
def logout():
	connection = sqlite3.connect("shop.db")
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	session.clear()
	return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
# app.run(host='0.0.0.0', port=8080)

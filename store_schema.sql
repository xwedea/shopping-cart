DROP TABLE IF EXISTS user;

CREATE TABLE user (
	email varchar(255),
	name varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	PRIMARY KEY (email)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
	id int,
	name varchar(255) NOT NULL,
	price int NOT NULL,
	stock int NOT NULL,
	category varchar(255) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category) REFERENCES category(name)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
	customer_email varchar(255),
	order_date DATETIME NOT NULL,
	total int NOT NULL,
	PRIMARY KEY (customer_email, order_date)
);

DROP TABLE IF EXISTS order_product;
CREATE TABLE order_product (
  email varchar(255),
	date_of_order DATETIME,
	product_id int,
	quantity int NOT NULL,
	PRIMARY KEY (email, date_of_order, product_id),
	FOREIGN KEY (email, date_of_order) REFERENCES orders(customer_email, order_date)
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
	name varchar(255) PRIMARY KEY
);

INSERT INTO user (email, name, password)
VALUES ("testuser@gwu", "testuser", "testpass");

INSERT INTO product (id, name, price, stock, category)
VALUES (2134, "apple", 3, 10, "food");
INSERT INTO product (id, name, price, stock, category)
VALUES (4323, "chocolate", 2, 10, "food");
INSERT INTO product (id, name, price, stock, category)
VALUES (4232, "pasta", 5, 34, "food");
INSERT INTO product (id, name, price, stock, category)
VALUES (2145, "cheese", 6, 2, "food");
INSERT INTO product (id, name, price, stock, category)
VALUES (5343, "wine", 12, 5, "drinks");
INSERT INTO product (id, name, price, stock, category)
VALUES (5435, "beer", 3, 10, "drinks");
INSERT INTO product (id, name, price, stock, category)
VALUES (3234, "notebook", 1, 1, "office");
INSERT INTO product (id, name, price, stock, category)
VALUES (6434, "pen", 4, 4, "office");
INSERT INTO product (id, name, price, stock, category)
VALUES (4362, "eraser", 1, 59, "office");



CREATE DATABASE FOOD_SYSTEM;
USE FOOD_SYSTEM;

CREATE TABLE User (
    user_id INT PRIMARY KEY auto_increment,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY auto_increment,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Manager (
    manager_id INT PRIMARY KEY auto_increment,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Phone_Number (
    number VARCHAR(20) PRIMARY KEY,
    country_code VARCHAR(10),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Address (
    street VARCHAR(100),
    city VARCHAR(50),
    postal_code VARCHAR(20) PRIMARY KEY NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Restaurant (
    restaurant_id INT PRIMARY KEY auto_increment,
    name VARCHAR(50) NOT NULL,
    adress Varchar(50),
    cuisine_type VARCHAR(50),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
);

CREATE TABLE Keyword (
    keyword_id INT PRIMARY KEY auto_increment,
    key_text VARCHAR(100),
	manager_id INT,
	restaurant_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
);

CREATE TABLE MenuItem (
    item_id INT PRIMARY KEY auto_increment,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255),
    dis_percentage DECIMAL(5,2) DEFAULT NULL,
    dis_end_date DATE DEFAULT NULL,
    restaurant_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

CREATE TABLE Cart (
    cart_id INT PRIMARY KEY auto_increment,
    customer_id INT,
    restaurant_id INT,
    quantity INT,
    status VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    item_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (item_id) REFERENCES MenuItem(item_id)
);

CREATE TABLE Rating (
    rating_id INT PRIMARY KEY auto_increment,
    rate INT CHECK (rate BETWEEN 1 AND 5),
    comment TEXT DEFAULT NULL,
    customer_id INT,
    restaurant_id INT,
    cart_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (cart_id) REFERENCES Cart(cart_id)
);
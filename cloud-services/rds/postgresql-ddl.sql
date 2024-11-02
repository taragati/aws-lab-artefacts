CREATE TABLE INVENTORY (
    id SERIAL PRIMARY KEY,
    product_id INT,
    stock INT,
    FOREIGN KEY (product_id) REFERENCES PRODUCT(id)
);

CREATE TABLE PRODUCT (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2)
);

CREATE TABLE ORDERS (
    id SERIAL PRIMARY KEY,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(id)
);


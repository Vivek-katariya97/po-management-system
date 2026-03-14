CREATE TABLE Vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    rating FLOAT
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(255) UNIQUE NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    stock_level INT DEFAULT 0,
    category VARCHAR(255)
);

CREATE TABLE PurchaseOrders (
    id SERIAL PRIMARY KEY,
    reference_no VARCHAR(255) UNIQUE NOT NULL,
    vendor_id INT NOT NULL REFERENCES Vendors(id),
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE PurchaseOrderItems (
    id SERIAL PRIMARY KEY,
    purchase_order_id INT NOT NULL REFERENCES PurchaseOrders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

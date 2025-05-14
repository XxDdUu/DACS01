create database QLDTCNCH

use QLDTCNCH

CREATE TABLE BRANCHES (
	Branch_ID INT PRIMARY KEY AUTO_INCREMENT, -- AUTO_INCREMENT CHO MYSQL
	Branch_name NVARCHAR(255),
	Branch_address NVARCHAR(255),
	Branch_phone_number CHAR(15) CHECK(REGEXP_LIKE(Branch_phone_number,"^[0-9]{10,15}$")),
	Create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Employer_ID INT,
    Enterprise_ID Varchar(255)
--     foreign key (Employer_ID) references EMPLOYER(Employer_ID),
--     foreign key (Enterprise_ID) references EMPLOYER(Enterprise_ID)
);
CREATE TABLE REVENUE (
	Revenue_ID INT PRIMARY KEY AUTO_INCREMENT, -- AUTO_INCREMENT CHO MYSQL
	Revenue_date DATE,
	Amount DECIMAL(15, 2),
	Create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	Branch_ID INT
--     foreign key (Branch_ID) references BRANCHES(Branch_ID)
);
CREATE TABLE EMPLOYER(
	Employer_ID INT PRIMARY KEY AUTO_INCREMENT, -- AUTO_INCREMENT CHO MYSQL
	Employer_name NVARCHAR(255),
    Employer_Phone_Number Varchar(255),
    Employer_Email Varchar(255),
	DOB DATE,
	Create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	Employer_password Varchar(255),
    Enterprise_ID Varchar(255)
--     Foreign key(Enterprise_ID) references ENTERPRISE(Enterprise_ID)
);

ALTER TABLE ENTERPRISE ADD Enterprise_password Varchar(255) /* use this */ 


CREATE TABLE ENTERPRISE(
	Enterprise_ID Varchar(255) PRIMARY KEY,employer
	Enterprise_NAME NVARCHAR(255),
    Enterprise_FOUNDER NVARCHAR(255),
    ADDRESS TEXT,
    Enterprise_PHONE_NUMBER VARCHAR(255),
    BUSINESS_TYPE NVARCHAR(255),
    INDUSTRY NVARCHAR(255),
    Enterprise_password Varchar(255)
);
CREATE TABLE PRODUCT(
		Product_ID INT PRIMARY KEY AUTO_INCREMENT, -- AUTO_INCREMENT CHO MYSQL
        Product_NAME NVARCHAR(255),
        PRICE DECIMAL(15,2),
        AMOUNT INT,
        Branch_ID int
--         foreign key (Branch_ID) references BRANCHES(Branch_ID)
);
CREATE TABLE PRODUCT_SALES (
	SALE_ID VARCHAR(255),
    Product_ID INT,
    Branch_ID INT,
    SALE_DATE DATE,
    QUANTITY_SOLD INT,
    SALE_AMOUNT DECIMAL(15,2)
--     foreign key (Product_ID) references PRODUCT(Product_ID),
--     foreign key (Branch_ID) references BRANCHES(Branch_ID)
);
-- khoa ngoai branches
ALTER TABLE BRANCHES 
ADD FOREIGN KEY (Employer_ID) REFERENCES EMPLOYER(Employer_ID) ON DELETE CASCADE,
ADD FOREIGN KEY (Enterprise_ID) REFERENCES ENTERPRISE(Enterprise_ID) ON DELETE CASCADE;
-- khoa ngoai revenue
ALTER TABLE REVENUE
ADD foreign key (Branch_ID) references BRANCHES(Branch_ID) ON DELETE CASCADE
-- khoa ngoai employer
ALTER TABLE EMPLOYER
ADD Foreign key(Enterprise_ID) references ENTERPRISE(Enterprise_ID) ON DELETE CASCADE
-- khoa ngoai product
ALTER TABLE PRODUCT 
ADD foreign key (Branch_ID) references BRANCHES(Branch_ID) ON DELETE CASCADE
-- khoa ngoai product_sales
ALTER TABLE PRODUCT_SALES
ADD foreign key (Product_ID) references PRODUCT(Product_ID) ON DELETE CASCADE,
ADD foreign key (Branch_ID) references BRANCHES(Branch_ID) ON DELETE CASCADE
-- Default cho create_at
ALTER TABLE EMPLOYER
MODIFY COLUMN Create_at DATETIME DEFAULT CURRENT_TIMESTAMP
ALTER TABLE BRANCHES
MODIFY COLUMN Create_at DATETIME DEFAULT CURRENT_TIMESTAMP
ALTER TABLE REVENUE
MODIFY COLUMN Create_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- unique cho employer & enterprise
ALTER TABLE EMPLOYER
ADD unique (Employer_Email),
ADD unique (Employer_Phone_Number)
ALTER TABLE ENTERPRISE
ADD unique (Enterprise_PHONE_NUMBER)
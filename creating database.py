import mysql.connector as ms
m=ms.connect(host="localhost", user='root', password='&Bushra.S.583')
mc=m.cursor()
mc.execute('CREATE database Crumbs;')
mc.execute('USE crumbs;')
mc.execute('''CREATE TABLE Menu (id varchar (3) NOT NULL,
name varchar (50) NOT NULL,
PRIMARY KEY (id))''')
mc.execute('''CREATE TABLE Cakes (id varchar (3) NOT NULL,
name varchar (50) NOT NULL,
price_1kg int (5) NOT NULL,
PRIMARY KEY (id))''')
mc.execute('''CREATE TABLE Pastries (id varchar (3) NOT NULL,
name varchar (50) NOT NULL,
price_perpiece int (3) NOT NULL,
PRIMARY KEY (id))''')
mc.execute('''CREATE TABLE Cookies (id varchar (3) NOT NULL,
name varchar (50) NOT NULL,
price_500g int (4) NOT NULL,
PRIMARY KEY (id))''')
mc.execute('''create table beverages (id varchar (3) not null,
name varchar (50) not null,
price_medium int(3) not null,
primary key (id))''')
mc.execute('''CREATE TABLE Employee(
id varchar(3) primary key,
name varchar(50)NOT NULL,
Salary int(5)NOT NULL,
Department varchar (20) NOT NULL)''')
mc.execute('''CREATE TABLE Personal_details(
id varchar(3) primary key,
name varchar(50)NOT NULL,
Phone_No bigint(10)NOT NULL,
Email_id varchar (40) NOT NULL)''')
mc.execute(''' create table c_details
(id int auto_increment primary key,
name varchar (30) NOT NULL,
phone_no bigint(10) NOT NULL,
address varchar (70),
amount int,
date_time varchar(50))''')
mc.execute('''CREATE TABLE admin
(id varchar(50), password varchar (20))''')
mc.execute('''INSERT INTO Menu (id, name) values
('C00', 'Cakes'), ('P00', 'Pastries'),
('K00', 'cookies'), ('B00', 'Beverages')''')
mc.execute('''INSERT INTO Cakes (id, name, price_1kg) values
('C01','vanilla', 1200), ('C02','pineapple',1200),
('C03','strawberry',1280), ('C04','blueberry', 1280),
('C05','choco delight',1280), ('C06','black forest', 1480),
('C07','Cheesecake',1680), ('C08','butter scotch', 1800),
('C09','piramys ',1800), ('C10','red velvet', 2000)''')
mc.execute('''INSERT INTO Pastries (id,name, price_perpiece) values
('P01', 'Vanilla',40), ('P02','Chocolate',40),
('P03','Pineapple',40), ('P04', 'Strawberry',40),
('P05','Blueberry',40), ('P06', 'Mango crush',40),
('P07', 'Guava love',40), ('P08','Litchi',40),
('P09', 'Butter Scotch',50), ('P10', 'Chocochip',50)''')
mc.execute('''INSERT INTO Cookies (id, name, price_500g) values
('K01', 'Peanut Butter', 1000), ('K02', 'Oatmeal', 1000),
('K03', 'Raisin', 1250), ('K04', 'Toffee Pecan', 1250),
('K05', 'Almond Butter', 1250),('K06', 'Fudge Walnut',1500),
('K07', 'Macadamia',1500), ('K08', 'Chocolate',1500),
('K09', 'Walnut', 1500), ('K10', 'White Choco',2000)''')
mc.execute('''insert into Beverages (id, name, price_medium) values
('B01', 'Apple Juice',50), ('B02', 'Banana Milk',50),
('B03', 'Citrus Peach',70), ('B04', 'Mango Rush', 70),
('B05', 'Choco Shake', 70), ('B06', 'Espresso', 120),
('B07', 'Americano', 120), ('B08', 'Cold Coffee', 120),
('B09', 'Cafe Mocha', 150), ('B10', 'Cappucino',150)''')
mc.execute('''INSERT INTO Employee (id, name,Salary,Department) values
('E01','Rupsa',50000,'Beverages'), ('E02','Salman',20000,'Delivery'),
('E03','Varun',45000,'Baking'), ('E04','Rashmi',15000,'Delivery'),
('E05','Diwaker',23000,'Decoration'), ('E06','Himanshu',50000,'Baking'),
('E07','Sam',25000,'Decoration'), ('E08','Jack',38000,'Beverages'),
('E09','Alice',30000,'Decoration'), ('E10','Jess',18000,'Delivery'),
('E11','Jacob',40000,'Baking')''')
mc.execute('''INSERT INTO personal_details (id, name,Phone_no,Email_id) values
('E01','Rupsa',9453866239,'rupsa@gmail.com'), ('E02','Salman',7548399873,'salman@gmail.com'),
('E03','Varun',8762744983, 'varun@gmail.com'), ('E04','Rashmi',7538200379,'rashmi@gamil.com'),
('E05','Diwaker',9689300238,'diwaker@gmail.com'), ('E06','Himanshu',8430500340,'himanshu@gmail.com'),
('E07','Sam',8918250312,'sam01@gamil.com'), ('E08','Jack',9256174449,'jack23@gamil.com'),
('E09','Alice',9647299564,'alice9@gamil.com'), ('E10','Jess',7649739564,'jess2@gmail.com'),
('E11','Jacob',8573099543,'jacob@gmail.com')''')
mc.execute('''INSERT INTO admin (id, password) values
('admin','987abc')''')
m.commit()
print('Database and tables created and data entered to the tables.')
m.close()

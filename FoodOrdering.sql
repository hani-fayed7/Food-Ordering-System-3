Create Schema FoodOrdering;
CREATE TABLE Customers ( 
	Customer_ID INT AUTO_INCREMENT,
    FirstName VARCHAR(18) NOT NULL,
    LastName VARCHAR(18) NOT NULL,
    PhoneNumber INT NOT NULL,
    Steet VARCHAR(20) NOT NULL,
    City VARCHAR(20) NOT NULL,
    Building VARCHAR(20),
    Floor INT,
    PRIMARY KEY(Customer_ID)
);

CREATE TABLE Menu_Items (
	Item_ID INT AUTO_INCREMENT,
    Item_Name VARCHAR(25) UNIQUE NOT NULL,
    Item_Type VARCHAR(25) NOT NULL,
    Item_Price DECIMAL(3, 2) NOT NULL,
    Item_Dsc VARCHAR(200),
    PRIMARY KEY(Item_ID),
    CONSTRAINT ITEM_PRICE_LESS_THAN_ZERO CHECK (Item_Price >0)
);

CREATE TABLE Ingredients(
	Ingredient_ID INT AUTO_INCREMENT,
    Ingredient_Name VARCHAR(30) UNIQUE NOT NULL,
    Ingredient_Price Decimal(6,2) NOT NULL,
    PRIMARY KEY(Ingredient_ID),
    CONSTRAINT INGREDIENT_PRICE_LESS_THAN_ZERO CHECK (Ingredient_Price >0)
);

CREATE TABLE Employees (
	Employee_ID INT AUTO_INCREMENT,
    FirstName VARCHAR(18) NOT NULL,
    LastName VARCHAR(18) NOT NULL,
    PhoneNumber INT UNIQUE NOT NULL,
    Job_title VARCHAR(18) NOT NULL,
    Emp_Status Varchar(18) NOT NULL,
    Login_pass Varchar(30) NOT NULL,
    PRIMARY KEY(Employee_ID)
);

CREATE TABLE Orders (
	Order_ID INT AUTO_INCREMENT,
    Order_date date NOT NULL,
    Order_time Time NOT NULL,
    Cust_ID INT,
    Emp_ID INT NOT NULL,
    PRIMARY KEY (Order_ID),
    FOREIGN KEY (Cust_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Emp_ID) REFERENCES Employees(Employee_ID)
);

CREATE TABLE Order_Items (
	Qty INT NOT NULL,
    Order_ID INT NOT NULL,
    Item_ID INT NOT NULL,
    Item_Total_Price DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID),
    FOREIGN KEY (Item_ID) REFERENCES Menu_Items (Item_ID),
    UNIQUE(Order_ID,Item_ID),
    CONSTRAINT QTY_LESS_THAN_ZERO CHECK (Qty>0),
	CONSTRAINT ITEM_TOTAL_PRICE_CHECK CHECK (Item_Total_Price > 0)
);

CREATE TABLE Menu_Ingredients (
	Ingredient_ID INT NOT NULL,
    Item_ID INT NOT NULL,
    FOREIGN KEY (Item_ID) REFERENCES Menu_Items (Item_ID) ON DELETE CASCADE,
	FOREIGN KEY (Ingredient_ID) REFERENCES Ingredients (Ingredient_ID),
    UNIQUE (Ingredient_ID,Item_ID)
);

-- Populating the Database 
-- Inserting the items on the menu
-- Burgers
INSERT INTO Menu_Items(Item_Name, Item_Type, Item_Price, Item_Dsc) VALUES 
('Beef Burger', 'Burger', 8.99, 'A classic beef burger with lettuce, tomato, onion, and cheese.'),
('Chicken Burger', 'Burger', 9.49, 'A grilled chicken burger with lettuce, tomato, onion, and mayo.'),
('Cheese Burger', 'Burger', 7.99, 'A classic cheeseburger with lettuce, tomato, and onions'),
('Zinger Burger', 'Burger', 4.50, 'Spicy fried chicken patty with lettuce and mayo');

-- Snadwiches
INSERT INTO Menu_Items(Item_Name, Item_Type, Item_Price, Item_Dsc) VALUES 
('Crispy Sandwich', 'Sandwiches', 3.99, 'A crispy sandwich with lettuce, tomato, and mayonnaise'),
('Chicken Sub Sandwich', 'Sandwiches', 5.99, 'A tasty sub sandwich with grilled chicken, cheese, lettuce, and tomato'),
('Tawook Sandwich', 'Sandwiches', 8.99, 'A sandwich with grilled chicken, lettuce, tomatoes, pickles, and garlic sauce'),
('Francisco Sandwiches', 'Sandwiches', 8.50, 'A delicious sandwich made with grilled chicken, avocado, lettuce, tomato, and mayo.');

-- Desserts
INSERT INTO Menu_Items (Item_Name, Item_Type, Item_Price, Item_Dsc) VALUES
('Brownies', 'Dessert', 2.99, 'A chocolatey treat with nuts and fudgy texture'),
('Tiramisu', 'Dessert', 4.99, 'An Italian dessert made with coffee, ladyfingers, and mascarpone cheese'),
('Cake', 'Dessert', 3.49, 'A classic cake with fluffy layers and creamy frosting'),
('Muffins', 'Dessert', 1.99, 'A baked good with a soft crumb and various flavors such as blueberry or chocolate chip');

-- Beverages
INSERT INTO Menu_Items (Item_Name, Item_Type, Item_Price, Item_Dsc) VALUES
('Soft Drinks', 'Beverage', 1.49, 'A selection of carbonated beverages such as cola, lemon-lime, or ginger ale'),
('Coffee Frappe', 'Beverage', 4.99, 'A blended coffee drink with milk and ice, topped with whipped cream and drizzle'),
('Ice Tea', 'Beverage', 2.49, 'A refreshing tea drink served with ice and lemon'),
('Water', 'Beverage', 0.99, 'A bottle of still or sparkling water, depending on preference');

-- Inserting the ingredients
INSERT INTO Ingredients (Ingredient_Name, Ingredient_Price)
VALUES ('Beef Patty', 4.99),
	   ('Lettuce', 0.25),
	   ('Tomato', 0.20),
	   ('Onion', 0.15),
	   ('Cheese', 0.50),
	   ('Burger Bun', 0.50),
       ('Chicken Patty', 3.99),
       ('Mayonnaise', 0.30),
	   ('Spices', 0.40),
	   ('Cheddar Patty', 1.99),
       ('Bread', 0.50),
       ('Chicken Fillet', 2.99),
       ('Sub Roll', 0.99),
       ('Pickles', 0.30),
       ('Garlic Sauce', 0.50),
       ('Tawook Chicken', 2.99),
       ('Caleslaw', 0.6),
       ('Avocado', 1.50),
       ('Flour', 0.20),
       ('Sugar', 0.30),
       ('Cocoa Powder', 0.50),
	   ('Butter', 0.80),
	   ('Eggs', 0.40),
       ('Nuts', 0.60),
       ('Ladyfingers', 1.50),
       ('Espresso', 0.50),
       ('Mascarpone Cheese', 2.99),
       ('Milk', 0.50),
       ('Blueberries', 1.50),
       ('Chocolate Chips', 1.20),
       ('Cola', 0.99),
       ('Lemon-Lime', 0.99),
       ('Coffee', 0.50),
       ('Ice', 0.10),
       ('Whipped Cream', 0.50),
       ('Drizzle', 0.30),
       ('Tea Bags', 0.30),
       ('Water', 0.10),
       ('Lemon', 0.30),
       ('Water Bottle', 0.99);
       
-- Connececting Menu_ingredients with its ingredients in Menu_ingredients Table
-- Connect Beef Burger to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Beef Burger'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Beef Patty', 'Lettuce', 'Tomato', 'Onion', 'Cheese', 'Burger Bun')
) AS Ingredient;

-- Connect Chicken Burger to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Chicken Burger'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Chicken Patty', 'Lettuce', 'Tomato', 'Onion', 'Mayonnaise', 'Burger Bun')
) AS Ingredient;

-- Connect Cheese Burger to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Cheese Burger'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Chicken Patty', 'Lettuce', 'Tomato', 'Onion', 'Cheese', 'Burger Bun')
) AS Ingredient;

-- Connect Zinger Burger to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Zinger Burger'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Chicken Patty', 'Lettuce', 'Tomato', 'Onion', 'Mayonnaise', 'Spices', 'Burger Bun')
) AS Ingredient;

-- Connect Tawook Sandwich to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Tawook Sandwich'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Tawook Chicken', 'Caleslaw', 'Pickles', 'Garlic Sauce', 'Bread')
) AS Ingredient;

-- Connect Francisco Sandwiches to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Francisco Sandwiches'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Avocado', 'Lettuce', 'Tomato', 'Onion', 'Chicken Fillet', 'Bread')
) AS Ingredient;

-- Connect Brownies to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Brownies'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Nuts', 'Flour', 'Sugar', 'Eggs', 'Butter')
) AS Ingredient;

-- Connect Tiramisu to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Tiramisu'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Ladyfingers', 'Espresso', 'Mascarpone Cheese', 'Sugar', 'Cocoa Powder')
) AS Ingredient;

-- Connect Muffins to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Muffins'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Flour', 'Sugar', 'Eggs', 'Milk', 'Blueberries', 'Chocolate Chips')
) AS Ingredient;

-- Connect Coffee Frappe to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Coffee Frappe'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Coffee', 'Milk', 'Ice', 'Whipped Cream', 'Drizzle')
) AS Ingredient;

-- Connect Ice Tea to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Ice Tea'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Tea Bags', 'Water', 'Sugar', 'Lemon')
) AS Ingredient;

-- Connect Soft Drinks to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Soft Drinks'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Cola','Lemon-Lime')
) AS Ingredient;

-- Connect Water to its ingredients
INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID)
SELECT Item_ID, Ingredient_ID FROM (
SELECT Item_ID FROM Menu_Items WHERE Item_Name = 'Water'
) AS Item, (
SELECT Ingredient_ID FROM Ingredients
WHERE Ingredient_Name IN ('Water Bottle')
) AS Ingredient;

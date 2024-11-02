from tkinter import ttk, messagebox
from tkinter.ttk import Combobox

import mysql.connector
from tkinter import *

from datetime import datetime

# Trying to Connect to Database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="FouAd.SouBra@844",
        port=3306,
        database="FoodOrdering"
    )
    db.autocommit = True
except mysql.connector.Error as error:
    print("Database Connection Failed!")
    quit()

print("Successfully Connected.")

# create a cursor object
cur = db.cursor()

try:
    manager_values = ("Fouad", "Soubra", 3846519, "manager", "active", "password")
    manager_query = "INSERT INTO Employees (FirstName, LastName, PhoneNumber, Job_title, Emp_Status, Login_pass) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(manager_query, manager_values)
except mysql.connector.IntegrityError:
    # Handle duplicate value error
    pass

# create an employee
try:
    employee_values = ("Hani", "Fayed", 81681151, "employee", "active", "password")
    employee_query = "INSERT INTO Employees (FirstName, LastName, PhoneNumber, Job_title, Emp_Status, Login_pass) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(employee_query, employee_values)
except mysql.connector.IntegrityError:
    # Handle duplicate value error
    pass

try:
    employee_values = ("Haitham", "Dayeh", 76470605, "employee", "active", "password")
    employee_query = "INSERT INTO Employees (FirstName, LastName, PhoneNumber, Job_title, Emp_Status, Login_pass) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(employee_query, employee_values)
except mysql.connector.IntegrityError:
    # Handle duplicate value error
    pass

# create the main window
root = Tk()
root.title("Login Interface")

# create a label for the username
user_label = Label(root, text="Employee Name:")
user_label.grid(row=0, column=0, padx=10, pady=10)

# create an entry for the username
user_var = StringVar()
user_entry = Entry(root, textvariable=user_var)
user_entry.grid(row=0, column=1, padx=10, pady=10)

# create a label for the password
pass_label = Label(root, text="Login Password:")
pass_label.grid(row=1, column=0, padx=10, pady=10)

# create an entry for the password
pass_var = StringVar()
pass_entry = Entry(root, show="*", textvariable=pass_var)
pass_entry.grid(row=1, column=1, padx=10, pady=10)

employee = None
order_id = None


# create a function to check if the login credentials are correct
def login():
    cur = db.cursor()
    query = "SELECT * FROM Employees WHERE FirstName = %s AND Login_pass = %s"
    values = (user_entry.get(), pass_entry.get())
    cur.execute(query, values)
    global employee
    employee = cur.fetchall()
    if len(employee) > 0:
        emp_name = employee[0][1]
        job_title = employee[0][4]
        emp_status = employee[0][5]
        if emp_status == "inactive":
            messagebox.showerror("Error", "Employee is inactive. Please contact your manager.")
        elif job_title == "manager":
            user_var.set("")
            pass_var.set("")
            open_admin_interface()
        elif job_title != "manager":
            user_var.set("")
            pass_var.set("")
            open_employee_interface(emp_name)
    else:
        messagebox.showerror("Error", "Invalid Username or Password!")
    cur.close()


# create a button for the login
login_button = Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


# function to open the admin interface
def open_admin_interface():
    # create the admin interface
    admin_window = Toplevel()
    admin_window.title("Admin Interface")

    # hide the login interface
    root.withdraw()
    # create a frame for the header
    header_frame = Frame(admin_window, pady=20)
    header_frame.pack()

    menu = Menu(admin_window)
    admin_window.config(menu=menu)

    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="Sign Out", command=lambda: sign_out())
    file_menu.add_separator()

    help_menu = Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)

    def how_to_use():
        htu = Tk()
        htu.minsize(width=100, height=100)
        htu.resizable(width=False, height=False)
        htu.title("How To Use")
        htu_label = Label(htu, justify=LEFT,
                          text="1. Click Add item to menu to add items\n2. Click Delete Item From Menu to delete menu items\n3. Click add igredients to menu to add diffrent ingredients to the menu\n4. Click on the change employee status button to make the employees active or inactives\n5. if you want to add an employee you can simply press it's button\n6. If you want to sign out click on File->Sign Out",
                          font=("Helvetica", 10))
        htu_label.pack()
        htu.mainloop()

    def about():
        abt = Tk()
        abt.minsize(width=100, height=100)
        abt.resizable(width=False, height=False)
        abt.title("About")
        abt_label = Label(abt, justify=LEFT,
                          text="Thank you for using our program...\nProgrammed By:  Hani Fayed\n                          Fouad Soubra\n                          Haitham Dayeh",
                          font=("Helvetica", 10))
        abt_label.pack()
        abt.mainloop()

    help_menu.add_command(label="How to use", command=how_to_use)
    help_menu.add_command(label="About", command=about)

    # add a label for the header
    admin_label = Label(header_frame, text="Welcome Admin!", font=("Arial", 24))
    admin_label.pack()

    # create a frame for the menu management section
    menu_frame = Frame(admin_window, padx=20, pady=20)
    menu_frame.pack()

    # add a label for the menu management section
    menu_label = Label(menu_frame, text="Menu Management", font=("Arial", 18))
    menu_label.pack()

    # add a frame for the menu management buttons
    menu_button_frame = Frame(menu_frame)
    menu_button_frame.pack()

    # add a button to add an item to the menu
    add_item_button = Button(menu_button_frame, text="Add Item to Menu", font=("Arial", 14), command=add_item_to_menu)
    add_item_button.pack(side=LEFT, padx=10)

    # add a button to delete an item from the menu
    delete_item_button = Button(menu_button_frame, text="Delete Item from Menu", font=("Arial", 14),
                                command=delete_menu_item)
    delete_item_button.pack(side=LEFT, padx=10)

    # add a button to edit an item in the menu
    edit_item_button = Button(menu_button_frame, text="Edit Item in Menu", font=("Arial", 14), command=update_menu_item)
    edit_item_button.pack(side=LEFT, padx=10)

    # add a button to add ingredients to the menu
    add_ingredients_button = Button(menu_frame, text="Add Ingredients to Menu", font=("Arial", 14),
                                    command=add_ingredients)
    add_ingredients_button.pack(pady=10)

    # create a frame for the employee management section
    employee_frame = Frame(admin_window, padx=20, pady=20)
    employee_frame.pack()

    # add a label for the employee management section
    employee_label = Label(employee_frame, text="Employee Management", font=("Arial", 18))
    employee_label.pack()

    # add a frame for the employee management buttons
    employee_button_frame = Frame(employee_frame)
    employee_button_frame.pack()

    # add a button to change an employee's job status to inactive
    inactive_button = Button(employee_button_frame, text="Change Employee Status", font=("Arial", 14),
                             command=update_employee_status)
    inactive_button.pack(side=LEFT, padx=10)

    # add a button to add an employee
    add_employee_button = Button(employee_frame, text="Add Employee", font=("Arial", 14), command=add_employee)
    add_employee_button.pack(pady=10)

    # create a frame for the back button
    back_button_frame = Frame(admin_window)
    back_button_frame.pack()

    # add a back button to return to the login interface
    def sign_out():
        admin_window.destroy()
        root.deiconify()

    # run the admin interface
    admin_window.mainloop()


# function to open the employee interface
def open_employee_interface(emp_name):
    # destroy the login interface
    root.withdraw()

    # create the employee interface
    employee_window = Toplevel()
    employee_window.title("Employee Interface")
    employee_window.minsize(width=800, height=505)
    employee_window.resizable(width=False, height=False)

    # add widgets to the employee interface
    employee_label = Label(employee_window, text=f"Welcome  {emp_name}!")
    employee_label.pack()

    menu = Menu(employee_window)
    employee_window.config(menu=menu)

    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="New order", command=lambda: new_order())
    file_menu.add_separator()
    file_menu.add_command(label="Sign Out", command=lambda: sign_out())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=employee_window.quit)

    help_menu = Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)

    def how_to_use():
        htu = Tk()
        htu.minsize(width=100, height=100)
        htu.resizable(width=False, height=False)
        htu.title("How To Use")
        htu_label = Label(htu, justify=LEFT,
                          text="1. Click on your desired meal\n2. Enter the quantity of your meal located in the textbox\n3. Click proceed when you finish\n4. If you want to begin a new order and reset the variables click on File->new order\n5. If you want to sign out click on File->Sign Out",
                          font=("Helvetica", 10))
        htu_label.pack()
        htu.mainloop()

    def about():
        abt = Tk()
        abt.minsize(width=100, height=100)
        abt.resizable(width=False, height=False)
        abt.title("About")
        abt_label = Label(abt, justify=LEFT,
                          text="Thank you for using our program...\nProgrammed By:  Hani Fayed\n                          Fouad Soubra\n                          Haitham Dayeh",
                          font=("Helvetica", 10))
        abt_label.pack()
        abt.mainloop()

    help_menu.add_command(label="How to use", command=how_to_use)
    help_menu.add_command(label="About", command=about)

    Title = Frame(employee_window, width=500, height=100, bd=12)
    Title.pack(side=TOP)

    title1 = Label(Title, text="   Food Ordering System   ", font=("Freestyle Script", 40))
    title1.grid(row=0, column=0)

    buttons_frame = Frame(employee_window, width=900, height=200, bd=9)
    buttons_frame.pack(side=BOTTOM)

    delivery_frame = Frame(buttons_frame, width=450, height=200, bd=9)
    delivery_frame.pack(side=LEFT)

    dineIn_frame = Frame(buttons_frame, width=450, height=200, bd=9)
    dineIn_frame.pack(side=RIGHT)

    menu_frame = Frame(employee_window, width=900, height=600)
    menu_frame.pack(side=BOTTOM)

    food_frame = Frame(menu_frame, width=900, height=250)
    food_frame.pack(side=TOP)

    sideFood_frame = Frame(menu_frame, width=900, height=250)
    sideFood_frame.pack(side=BOTTOM)

    burger_frame = Frame(food_frame, width=450, height=250, bd=12)
    burger_frame.pack(side=LEFT)

    sandwich_frame = Frame(food_frame, width=450, height=250, bd=12)
    sandwich_frame.pack(side=RIGHT)

    dessert_frame = Frame(sideFood_frame, width=450, height=250, bd=12)
    dessert_frame.pack(side=LEFT)

    beverages_frame = Frame(sideFood_frame, width=450, height=250, bd=12)
    beverages_frame.pack(side=RIGHT)

    burger_label = Label(burger_frame, text="Burgers", font=("Freestyle Script", 25))
    burger_label.grid(row=0, column=0)

    sandwich_label = Label(sandwich_frame, text="Sandwiches", font=("Freestyle Script", 25))
    sandwich_label.grid(row=0, column=0)

    dessert_label = Label(dessert_frame, text="Desserts", font=("Freestyle Script", 25))
    dessert_label.grid(row=0, column=0)

    beverages_label = Label(beverages_frame, text="Beverages", font=("Freestyle Script", 25))
    beverages_label.grid(row=0, column=0)

    delivery_button = Button(delivery_frame, text="Delivery", font=("arial", 15), command=lambda: delivery_click())
    delivery_button.pack()

    dineIn_button = Button(dineIn_frame, text="Dine-In", font=("arial", 15), command=lambda: dine_in_click())
    dineIn_button.pack()

    var_dict = {}
    itemType = ['Burger', 'Sandwiches', 'Dessert', 'Beverage']
    frames = [burger_frame, sandwich_frame, dessert_frame, beverages_frame]
    for i in range(4):
        with db.cursor() as cursor:
            query = "SELECT * FROM Menu_Items WHERE Item_Type = %s"
            value = itemType[i]
            cursor.execute(query, [value])
            records = cursor.fetchall()

        counter = 1
        for record in records:
            var = IntVar()
            text = StringVar()
            menuItem_label = Label(frames[i], text=f"{record[1]}...................{record[3]}$", font=("arial", 15))
            menuItem_label.grid(row=counter, column=0)

            menuItem_quantity = Entry(frames[i], width=5, font=("arial", 10), justify=RIGHT, bd=2, textvariable=var)
            menuItem_quantity.grid(row=counter, column=1)
            var_dict[record[1]] = var

            counter += 1

    def orders():
        # insert the order into the Orders table
        with db.cursor() as mycursor:
            # get the current date and time
            order_date = datetime.now().date()
            order_time = datetime.now().time()

            # get the employee id
            mycursor.execute("SELECT Employee_ID FROM Employees WHERE PhoneNumber = %s", (employee[0][3],))
            emp_ID = mycursor.fetchone()
            emp_ID = int(emp_ID[0])

            # insert the order into the database table Orders
            orders_sql = "INSERT INTO Orders (Order_date, Order_time, Emp_ID) VALUES (%s, %s, %s)"
            mycursor.execute(orders_sql, (order_date, order_time, emp_ID))

            # get the order id
            global order_id
            order_id = mycursor.lastrowid

        # insert the order items into the Order_Items table
        for item_name, var in var_dict.items():
            quantity = var.get()
            if quantity > 0:
                with db.cursor() as mycursor:
                    # get the item id
                    mycursor.execute("SELECT Item_ID FROM Menu_Items WHERE Item_Name = %s", (item_name,))
                    item_id = mycursor.fetchone()
                    item_id = int(item_id[0])

                    # get the item price
                    mycursor.execute("SELECT Item_Price FROM Menu_Items WHERE Item_Name = %s", (item_name,))
                    item_price = mycursor.fetchone()
                    item_price = float(item_price[0])

                    # calculate the total price of the item
                    total_item_price = item_price * float(quantity)

                    # insert the order item into the database table Order_Items
                    orderItems_sql = "INSERT INTO Order_Items (Qty, Order_ID, Item_ID, Item_Total_Price) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(orderItems_sql, (quantity, order_id, item_id, total_item_price))

        new_order()

    def print_receipt():
        # Get the order details from the database
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT Orders.Order_date AS date, Orders.Order_time AS time, Menu_Items.Item_Name, Order_Items.Qty, Order_Items.Item_Total_Price "
                "FROM Orders "
                "INNER JOIN Order_Items ON Orders.Order_ID = Order_Items.Order_ID "
                "INNER JOIN Menu_Items ON Order_Items.Item_ID = Menu_Items.Item_ID "
                "WHERE orders.Order_ID = %s",
                (order_id,))
            order_details = cursor.fetchall()

        if order_details:
            # Create a tkinter window
            receipt = Tk()
            receipt.title("Receipt")
            receipt.minsize(width=100, height=100)
            receipt.resizable(width=False, height=False)

            # Create a label for the receipt header
            header_label = Label(receipt, text=f"Receipt #{order_id}", font=("courier new", 16))
            header_label.pack(pady=10)

            # Create a label for the order date and time
            date_label = Label(receipt, text=f"Date: {order_details[0][0]}", font=("courier new", 11))
            date_label.pack(anchor='w')

            time_label = Label(receipt, text=f"Time: {order_details[0][1]}", font=("courier new", 11))
            time_label.pack(anchor='w')

            line_label = Label(receipt, text="---------------------------------------------", font=("courier new", 10))
            line_label.pack()
            # Create a label for each item ordered
            total = 0.00
            for item in order_details:
                item_label = Label(receipt, text=f"{item[2]} x{item[3]}..............${item[4]:.2f}",
                                   font=("courier new", 10))
                item_label.pack(anchor='w')
                total = float(item[4]) + float(total)

            # create a line and the total label
            label = Label(receipt, text="---------------------------------------------", font=("courier new", 10))
            label.pack()

            total_label = Label(receipt, text=f"total.................................${total:.2f}",
                                font=("courier new", 10))
            total_label.pack(anchor='w')
            return receipt
        else:
            messagebox.showerror("Error", "Order details not found.")

    def delivery_click():
        if any(var.get() > 0 for var in var_dict.values()):
            # Create cursor object
            mycursor = db.cursor()

            # Create GUI window
            window = Tk()
            window.title("Customer Information")

            # Add labels for each attribute
            Label(window, text="First Name").grid(row=0)
            Label(window, text="Last Name").grid(row=1)
            Label(window, text="Phone Number").grid(row=2)
            Label(window, text="Street").grid(row=3)
            Label(window, text="City").grid(row=4)
            Label(window, text="Building").grid(row=5)
            Label(window, text="Floor").grid(row=6)

            # Add entry fields for each attribute
            first_name_entry = Entry(window)
            last_name_entry = Entry(window)
            phone_number_entry = Entry(window)
            street_entry = Entry(window)
            city_entry = Entry(window)
            building_entry = Entry(window)
            floor_entry = Entry(window)

            first_name_entry.grid(row=0, column=1)
            last_name_entry.grid(row=1, column=1)
            phone_number_entry.grid(row=2, column=1)
            street_entry.grid(row=3, column=1)
            city_entry.grid(row=4, column=1)
            building_entry.grid(row=5, column=1)
            floor_entry.grid(row=6, column=1)

            # Add button to submit data
            submit_button = Button(window, text="Submit", command=lambda: insert_customer())
            submit_button.grid(row=7, column=1)

            # Define function to insert data into database
            def insert_customer():
                first_name = first_name_entry.get() or None
                last_name = last_name_entry.get() or None
                phone_number = phone_number_entry.get() or None
                street = street_entry.get() or None
                city = city_entry.get() or None
                building = building_entry.get() or None
                floor = floor_entry.get() or None

                # Use SQL INSERT statement to insert data into database
                sql = "INSERT INTO Customers (FirstName, LastName, PhoneNumber, Steet, City, Building, Floor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (first_name, last_name, phone_number, street, city, building, floor)
                try:
                    mycursor.execute(sql, val)
                    customer_id = mycursor.lastrowid
                    messagebox.showinfo("Success", "Succeful")
                    window.destroy()
                    orders()
                    mycursor.execute("UPDATE Orders SET Cust_ID = %s WHERE Order_ID = %s", (customer_id, order_id))
                    customer_info(first_name, last_name, phone_number, street, city, building, floor)
                    mycursor.close()

                except mysql.connector.Error as error:
                    messagebox.showerror("Error", "failed to add customer")

            print("Delivery option selected")
            # Add your code for delivery option here
        else:
            messagebox.showerror("Error", "Excuse me?")

    def customer_info(first_name, last_name, phone_number, street, city, building, floor):
        new_receipt = print_receipt()
        # create a line and the total label
        label = Label(new_receipt, text="---------------------------------------------", font=("courier new", 10))
        label.pack()

        # create a label for each piece of customer information

        Label(new_receipt, text="Customer Info\n..............", font=("courier new", 11)).pack(anchor='w')
        Label(new_receipt, text=f"First Name: {first_name}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"Last Name: {last_name}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"Phone Number: {phone_number}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"Street: {street}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"City: {city}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"Building: {building}", font=("courier new", 10)).pack(anchor='w')
        Label(new_receipt, text=f"Floor: {floor}", font=("courier new", 10)).pack(anchor='w')

    def dine_in_click():
        if any(var.get() > 0 for var in var_dict.values()):
            orders()
            print_receipt()
            print("Dine-in option selected")
        else:
            messagebox.showerror("Error", "Excuse me?")

    def new_order():
        for item_name, var in var_dict.items():
            var.set("0")

    def sign_out():
        employee_window.destroy()
        root.deiconify()
    # run the employee interface
    employee_window.mainloop()



def add_item_to_menu():
    # Define the function to add the item to the database
    def add_to_database():
        item_name = name_entry.get() or None
        item_type = type_combobox.get()
        price_str = price_entry.get().strip()
        if price_str:
            item_price = float(price_str)
        else:
            item_price = None
        item_description = desc_entry.get() or None
        item_ingredients = ingredient_listbox.curselection()

        # Insert the new item into the Menu_Items table
        mycur = db.cursor()

        sql = "INSERT INTO Menu_Items (Item_Name, Item_Type, Item_Price, Item_Dsc) VALUES (%s, %s, %s, %s)"
        val = (item_name, item_type, item_price, item_description)
        try:
            mycur.execute(sql, val)
            messagebox.showinfo("Success", "Item has been added successfully.")
            window.destroy()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to add Item: {error}")

        # Get the ID of the newly inserted item
        item_id = mycur.lastrowid

        # Insert the selected ingredients into the Menu_Ingredients table
        for i in item_ingredients:
            ingredient_name = ingredient_names[i]
            sql = "SELECT Ingredient_ID FROM Ingredients WHERE Ingredient_Name = %s"
            val = (ingredient_name,)
            mycur.execute(sql, val)
            result = mycur.fetchone()
            if result is not None:
                ingredient_id = result[0]
                sql = "INSERT INTO Menu_Ingredients (Item_ID, Ingredient_ID) VALUES (%s, %s)"
                val = (item_id, ingredient_id)
                mycur.execute(sql, val)

        db.commit()
        mycur.close()

    # Create the window
    window = Tk()
    window.title("Add Item to Menu")
    window.geometry("400x300")

    # Retrieve the ingredient names from the Ingredients table
    mycursor = db.cursor()
    mycursor.execute("SELECT Ingredient_Name FROM Ingredients")
    ingredient_names = [result[0] for result in mycursor.fetchall()]
    mycursor.close()

    # Create the labels and entry boxes for the item information
    name_label = Label(window, text="Name:")
    name_label.grid(column=0, row=0)
    name_entry = Entry(window)
    name_entry.grid(column=1, row=0)

    type_label = Label(window, text="Type:")
    type_label.grid(column=0, row=1)
    type_combobox = Combobox(window, values=["Burger", "Sandwiches", "Beverage", "Dessert"])
    type_combobox.grid(column=1, row=1)
    type_combobox.current(0)

    price_label = Label(window, text="Price:")
    price_label.grid(column=0, row=2)
    price_entry = Entry(window)
    price_entry.grid(column=1, row=2)

    desc_label = Label(window, text="Description:")
    desc_label.grid(column=0, row=3)
    desc_entry = Entry(window)
    desc_entry.grid(column=1, row=3)

    # Create the label and listbox for the ingredient names
    ingredient_label = Label(window, text="Ingredients:")
    ingredient_label.grid(column=0, row=4)
    ingredient_listbox = Listbox(window, selectmode="multiple")
    for ingredient_name in ingredient_names:
        ingredient_listbox.insert(END, ingredient_name)
    ingredient_listbox.grid(column=1, row=4)

    # Create the "Add" button
    add_button = Button(window, text="Add", command=add_to_database)
    add_button.grid(column=0, row=5, columnspan=2)

    # Run the window
    window.mainloop()


def add_ingredients():
    # Define the function to add the item to the database
    def add_to_database():
        Ingredient_name = name_entry.get().strip()
        Ingredient_price = price_entry.get().strip()

        if not Ingredient_name:
            messagebox.showerror("Error", "Please enter an ingredient name.")
            return
        try:
            ingredient_price = float(Ingredient_price)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")
            return

        # Insert the new item into the Menu_Items table
        mycur = db.cursor()

        sql = "INSERT INTO Ingredients (Ingredient_Name, Ingredient_Price) VALUES (%s, %s)"
        val = (Ingredient_name, Ingredient_price)
        mycur.execute(sql, val)
        db.commit()
        messagebox.showinfo("Success", "Ingredient added successfully.")

        # Close the cursor object
        mycur.close()
        # Destroy the window and close connection
        window.destroy()

    # Create the window
    window = Tk()
    window.title("Add Ingredients")
    window.geometry("350x200")

    # Create the frames
    top_frame = Frame(window, pady=10)
    top_frame.pack()
    middle_frame = Frame(window, pady=10)
    middle_frame.pack()
    bottom_frame = Frame(window)
    bottom_frame.pack()

    # Create the labels and entry boxes for the input fields
    name_label = Label(top_frame, text="Ingredient name:")
    name_label.pack(side=LEFT, padx=10)
    name_entry = Entry(top_frame, width=30)
    name_entry.pack(side=LEFT)

    price_label = Label(middle_frame, text="Ingredient price:")
    price_label.pack(side=LEFT, padx=10)
    price_entry = Entry(middle_frame, width=30)
    price_entry.pack(side=LEFT)

    # Create the "Add" and "Cancel" buttons
    add_button = Button(bottom_frame, text="Add", command=add_to_database)
    add_button.pack(side=LEFT, padx=10)
    cancel_button = Button(bottom_frame, text="Cancel", command=window.destroy)
    cancel_button.pack(side=LEFT)

    # Run the window
    window.mainloop()


def delete_menu_item():
    # Define the function to delete the item from the database
    def delete_from_database():
        item_name = name_combobox.get()

        # Delete the item from the Menu_Items table
        mycur = db.cursor()

        sql = "DELETE FROM Menu_Items WHERE Item_Name = %s"
        val = (item_name,)
        mycur.execute(sql, val)

        db.commit()
        mycur.close()
        window.destroy()

    # Create the window
    window = Tk()
    window.title("Delete Item from Menu")
    window.geometry("400x200")

    # Retrieve the item names from the Menu_Items table
    mycursor = db.cursor()
    mycursor.execute("SELECT Item_Name FROM Menu_Items")
    item_names = [result[0] for result in mycursor.fetchall()]
    mycursor.close()

    # Create the label and combobox for selecting the item to delete
    name_label = Label(window, text="Select item to delete:", font=("Helvetica", 14))
    name_label.pack(pady=(20, 5))
    name_combobox = Combobox(window, font=("Helvetica", 14), values=item_names)
    name_combobox.pack(pady=(5, 20))
    name_combobox.current(0)

    # Create the "Delete" button
    delete_button = Button(window, text="Delete", font=("Helvetica", 14), bg="#f44336", fg="#fff",
                           command=delete_from_database)
    delete_button.pack(pady=(0, 20))

    # Run the window
    window.mainloop()


def update_menu_item():
    # Define the function to update the menu item
    def update_item():
        # Get the selected item ID and the updated item information from the user input
        selected_item = item_combobox.get()
        selected_item_id = item_ids[selected_item]
        updated_name = name_entry.get().strip()
        updated_type = type_combobox.get()
        updated_price = price_entry.get().strip()
        updated_description = desc_entry.get().strip()

        # Validate the input
        if not updated_name:
            messagebox.showerror("Error", "Please enter an item name.")
            return
        if not updated_description:
            messagebox.showerror("Error", "Please enter a description.")
            return
        try:
            updated_price = float(updated_price)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")
            return

        # Update the Menu_Items table with the new information
        mycursor = db.cursor()
        sql = "UPDATE Menu_Items SET Item_Name = %s, Item_Type = %s, Item_Price = %s, Item_Dsc = %s WHERE Item_ID = %s"
        val = (updated_name, updated_type, updated_price, updated_description, selected_item_id)
        mycursor.execute(sql, val)
        db.commit()
        mycursor.close()
        messagebox.showinfo("Success", "Item has been updated successfully.")
        window.destroy()

    # Create the window
    window = Tk()
    window.title("Update Menu Item")

    # Retrieve the current information for the menu items
    mycursor = db.cursor()
    sql = "SELECT Item_ID, Item_Name FROM Menu_Items"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()

    # Create the dictionary to map item names to item IDs
    item_ids = {}
    for result in results:
        item_ids[result[1]] = result[0]

    # Create the dropdown list for the menu items
    item_label = Label(window, text="Select Item:")
    item_label.grid(row=0, column=0, padx=10, pady=10)
    item_combobox = ttk.Combobox(window, values=[result[1] for result in results])
    item_combobox.grid(row=0, column=1)
    item_combobox.current(0)

    # Create the labels and entry boxes for the item information
    name_label = Label(window, text="Name:")
    name_label.grid(row=1, column=0, padx=10, pady=10)
    name_entry = Entry(window, width=30)
    name_entry.grid(row=1, column=1)

    type_label = Label(window, text="Type:")
    type_label.grid(row=2, column=0, padx=10, pady=10)
    type_combobox = ttk.Combobox(window, values=["Burger", "Sandwiches", "Dessert", "Beverage"])
    type_combobox.grid(row=2, column=1)

    price_label = Label(window, text="Price:")
    price_label.grid(row=3, column=0, padx=10, pady=10)
    price_entry = Entry(window, width=10)
    price_entry.grid(row=3, column=1)

    desc_label = Label(window, text="Description:")
    desc_label.grid(row=4, column=0, padx=10, pady=10)
    desc_entry = Entry(window, width=30)
    desc_entry.grid(row=4, column=1)

    # Create the buttons
    update_button = Button(window, text="Update Item", command=update_item)
    update_button.grid(row=5, column=0, padx=10, pady=10)

    cancel_button = Button(window, text="Cancel", command=window.destroy)
    cancel_button.grid(row=5, column=1, padx=10, pady=10)

    # Bind the dropdown list to a function that updates the labels and entry boxes with the current information for the selected item
    def update_info(*args):
        selected_item = item_combobox.get()
        selected_item_id = item_ids[selected_item]
        mycursor = db.cursor()
        sql = "SELECT Item_Name, Item_Type, Item_Price, Item_Dsc FROM Menu_Items WHERE Item_ID = %s"
        val = (selected_item_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        mycursor.close()

        name_entry.delete(0, END)
        name_entry.insert(0, result[0])
        type_combobox.set(result[1])
        price_entry.delete(0, END)
        price_entry.insert(0, result[2])
        desc_entry.delete(0, END)
        desc_entry.insert(0, result[3])

    # Bind the update_info() function to the Combobox widget's <<ComboboxSelected>> event, so that the labels and entry boxes
    # are automatically updated with the information for the selected item whenever the user selects a different item from
    # the dropdown list.
    item_combobox.bind("<<ComboboxSelected>>", update_info)
    update_info()

    # Run the window
    window.mainloop()


def update_employee_status():
    # Define the function to update the employee status
    def update_status():
        # Get the selected employee ID and update the employee status in the database
        selected_employee_id = int(employee_combobox.get())
        selected_status = status_combobox.get()
        mycursor = db.cursor()
        sql = "UPDATE Employees SET Emp_Status = %s WHERE Employee_ID = %s"
        val = (selected_status, selected_employee_id)
        mycursor.execute(sql, val)
        db.commit()
        mycursor.close()
        messagebox.showinfo("Success", "Employee status has been updated successfully.")
        window.destroy()

    # Create the window
    window = Tk()
    window.title("Update Employee Status")

    # Create the dropdown list for the employee IDs
    employee_label = Label(window, text="Select Employee ID:")
    employee_label.grid(row=0, column=0, padx=10, pady=10)
    mycursor = db.cursor()
    sql = "SELECT Employee_ID, Job_title FROM Employees WHERE Job_title != 'manager'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mycursor.close()
    employee_ids = [result[0] for result in results]
    employee_combobox = ttk.Combobox(window, values=employee_ids)
    employee_combobox.grid(row=0, column=1)
    employee_combobox.current(0)

    # Function to update the selected employee's name based on the selected ID
    def update_employee_name(event):
        selected_id = int(employee_combobox.get())
        mycursor = db.cursor()
        sql = "SELECT FirstName, LastName FROM Employees WHERE Employee_ID = %s"
        val = (selected_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        mycursor.close()
        selected_name = f"{result[0]} {result[1]}"
        employee_name_label.config(text=selected_name)

    # Bind the update_employee_name function to the Combobox widget's <<ComboboxSelected>> event
    employee_combobox.bind("<<ComboboxSelected>>", update_employee_name)

    # Create the label for the selected employee name
    employee_name_label = Label(window, text="")
    employee_name_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Create the dropdown list for the status
    status_label = Label(window, text="Status:")
    status_label.grid(row=2, column=0, padx=10, pady=10)
    status_combobox = ttk.Combobox(window, values=["active", "inactive"])
    status_combobox.grid(row=2, column=1)
    status_combobox.current(0)

    # Create the button to update the employee status
    update_button = Button(window, text="Update Status", command=update_status)
    update_button.grid(row=3, column=0, padx=10, pady=10)

    # Create the button to cancel the update
    cancel_button = Button(window, text="Cancel", command=window.destroy)
    cancel_button.grid(row=3, column=1, padx=10, pady=10)

    # Run the window
    window.mainloop()


def add_employee():
    # Define the function to add a new employee
    def add_new_employee():
        # Get the employee information from the entry fields and insert into the database
        first_name = first_name_entry.get() or None
        last_name = last_name_entry.get() or None
        phone_number = phone_number_entry.get() or None
        job_title = job_title_entry.get() or None
        emp_status = status_combobox.get()
        login_pass = login_pass_entry.get() or None
        mycursor = db.cursor()
        sql = "INSERT INTO Employees (FirstName, LastName, PhoneNumber, Job_title, Emp_Status, Login_pass) \
               VALUES (%s, %s, %s, %s, %s, %s)"
        val = (first_name, last_name, phone_number, job_title, emp_status, login_pass)
        try:
            mycursor.execute(sql, val)
            db.commit()
            mycursor.close()
            messagebox.showinfo("Success", "Employee has been added successfully.")
            window.destroy()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to add employee: {error}")

    # Create the window
    window = Tk()
    window.title("Add Employee")

    # Create the label and entry for the first name
    first_name_label = Label(window, text="First Name:")
    first_name_label.grid(row=0, column=0, padx=10, pady=10)
    first_name_entry = Entry(window)
    first_name_entry.grid(row=0, column=1)
    first_name_entry.focus()

    # Create the label and entry for the last name
    last_name_label = Label(window, text="Last Name:")
    last_name_label.grid(row=1, column=0, padx=10, pady=10)
    last_name_entry = Entry(window)
    last_name_entry.grid(row=1, column=1)

    # Create the label and entry for the phone number
    phone_number_label = Label(window, text="Phone Number:")
    phone_number_label.grid(row=2, column=0, padx=10, pady=10)
    phone_number_entry = Entry(window)
    phone_number_entry.grid(row=2, column=1)

    # Create the label and entry for the job title
    job_title_label = Label(window, text="Job Title:")
    job_title_label.grid(row=3, column=0, padx=10, pady=10)
    job_title_entry = Entry(window)
    job_title_entry.grid(row=3, column=1)

    # Create the dropdown list for the status
    status_label = Label(window, text="Status:")
    status_label.grid(row=4, column=0, padx=10, pady=10)
    status_combobox = ttk.Combobox(window, values=["active", "inactive"])
    status_combobox.grid(row=4, column=1)
    status_combobox.current(0)

    # Create the label and entry for the login password
    login_pass_label = Label(window, text="Login Password:")
    login_pass_label.grid(row=5, column=0, padx=10, pady=10)
    login_pass_entry = Entry(window, show="*")
    login_pass_entry.grid(row=5, column=1)

    # Create the button to add the new employee
    add_button = Button(window, text="Add Employee", command=add_new_employee)
    add_button.grid(row=6, column=0, padx=10, pady=10)

    # Create the button to cancel the add employee action
    cancel_button = Button(window, text="Cancel", command=window.destroy)
    cancel_button.grid(row=6, column=1, padx=10, pady=10)

    # Run the window
    window.mainloop()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# run the main loop
root.mainloop()

# close the cursor and database connection
db.close()
import sqlite3
import datetime

#import the databasesud
#from /home/pudrunui/Documents/Database/expenses import expenses.db

# define which database you want to use
db_name = "/home/pudrunui/Documents/Homestay_apps/db_list/expenses.db"
table_name = "expenses"

conn = sqlite3.connect(db_name)    # connect to database
cur = conn.cursor()

while True:
    print("Currently writing to database named: {table_name}".format(table_name = table_name))
    print("Select an option:")
    print("1.Add new expense")
    print("2.View expenses summary")
    print("3.Remove expense from summary")
    print("4.Exit")

    choice = int(input())

    if choice == 1:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cur.execute('''SELECT DISTINCT category FROM {table_name}'''.format(table_name = table_name))

        categories = cur.fetchall()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category[0]}")
        print(f"{len(categories) + 1}. Create a new category")
              
        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Eneter the new category name: ")
        else:
            category = categories[category_choice - 1][0]

        price = input("Enter the price of the expense: ")

        cur.execute('''INSERT INTO {table_name} (Date, description, category, price) VALUES (?, ?, ?, ?)'''.format(table_name = table_name), (date, description, category, price))

        
        conn.commit()
    
    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View monthly expenses by category")
        # may add additional options in the future

        view_choice = int(input())

        if view_choice == 1:
            cur.execute("SELECT * FROM {table_name}".format(table_name = table_name))
            expenses = cur.fetchall()
            for expenses in expenses:
                print(expenses)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input(" Enter the year (YYYY): ")
            cur.execute("""SELECT category, SUM(price) FROM {table_name}
                        WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                        GROUP BY category""".format(table_name = table_name), (month, year))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")
        else:
            print("exiting program")
            exit()

    else:
        print("Exiting program")
        exit()
    
    '''
    elif choice == 3:
        cur.execute("""SELECT category, SUM(price) FROM {table_name}
                        WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                        GROUP BY category""".format(table_name = table_name), (month, year))
    '''
            

    
    print("\n")
''' 
    repeat = input("Would you like to do something else (y/n)?: ")
    # if you enter anything but yes then it will break out of the loop
    if repeat.lower() != "y":
        break
'''

conn.close()

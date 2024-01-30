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
    print("3.Modify existing expense")
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

    elif choice == 3:
        expense_id = int(input("Enter the ID of the expense you want to modify: "))

        cur.execute("SELECT * FROM {table_name} WHERE id = ?".format(table_name=table_name), (expense_id,))
        expense = cur.fetchone()

        if not expense:
            print("Expense not found.")
        else:
            print("Current expense details:")
            print("ID:", expense[0])
            print("Date:", expense[1])
            print("Description:", expense[2])
            print("Category:", expense[3])
            print("Price:", expense[4])

            # Get new values for modification
            new_date = input("Enter the new date(YYYY-MM-DD) (press Enter to keep the current value): ") or expense[1]
            new_description = input("Enter the new description (press Enter to keep the current value): ") or expense[2]
            new_category = input("Enter the new category (press Enter to keep the current value): ") or expense[3]
            new_price = input("Enter the new price (press Enter to keep the current value): ") or expense[4]

            # Update the expense in the database
            cur.execute(
                """UPDATE {table_name} SET Date=?, description=?, category=?, price=? WHERE id=?""".format(
                    table_name=table_name
                ),
                (new_date, new_description, new_category, new_price, expense_id),
            )
            conn.commit()
            print("Expense updated successfully.")

    else:
        print("Exiting program")
        exit()       

    
    print("\n")


conn.close()

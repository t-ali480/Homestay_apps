import sqlite3

# define which database you want to use
db_name = "/home/hetman/projects/project_money/expenses_tracker/db_list/March_24.db"
table_name = "March_24"

conn = sqlite3.connect(db_name)    # connect to database
cur = conn.cursor()

while True:
    print("Currently writing to database named: {table_name}".format(table_name=table_name))
    print("Select an option:")
    print("1.Add new expense")
    print("2.View expenses summary")
    print("3.Modify existing expense")
    print("4.Exit")

    choice = int(input())

    if choice == 1:
        description = input("Enter the description of the expense: ")

        cur.execute('''SELECT DISTINCT category FROM {table_name}'''.format(table_name=table_name))

        categories = cur.fetchall()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category[0]}")
        print(f"{len(categories) + 1}. Create a new category")
              
        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else:
            category = categories[category_choice - 1][0]

        price = input("Enter the price of the expense: ")

        cur.execute('''INSERT INTO {table_name} (description, category, price) VALUES (?, ?, ?)'''.format(table_name=table_name), (description, category, price))

        conn.commit()
    
    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View expenses by category")
        # may add additional options in the future

        view_choice = int(input())

        if view_choice == 1:
            cur.execute("SELECT * FROM {table_name}".format(table_name=table_name))
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            cur.execute("""SELECT category, SUM(price) FROM {table_name} GROUP BY category""".format(table_name=table_name))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")

    elif choice == 3:
        expense_id = int(input("Enter the ID of the expense you want to modify: "))

        cur.execute("SELECT * FROM {table_name} WHERE id = ?".format(table_name=table_name), (expense_id,))
        expense = cur.fetchone()

        if not expense:
            print("Expense not found.")
        else:
            print("Current expense details:")
            print("ID:", expense[0])
            print("Description:", expense[1])
            print("Category:", expense[2])
            print("Price:", expense[3])

            # Get new values for modification
            new_description = input("Enter the new description (press Enter to keep the current value): ") or expense[1]
            new_category = input("Enter the new category (press Enter to keep the current value): ") or expense[2]
            new_price = input("Enter the new price (press Enter to keep the current value): ") or expense[3]

            # Update the expense in the database
            cur.execute("""UPDATE {table_name} SET description=?, category=?, price=? WHERE id=?""".format(table_name=table_name), (new_description, new_category, new_price, expense_id))
            conn.commit()
            print("Expense updated successfully.")

    else:
        print("Exiting program")
        break

    print("\n")


conn.close()

from influxdb import InfluxDBClient
import datetime

# Define InfluxDB connection parameters
influx_host = 'localhost'
influx_port = 8086
influx_user = 'username'
influx_password = 'password'
influx_database = 'expenses'

# Connect to InfluxDB
influx_client = InfluxDBClient(host=influx_host, port=influx_port, username=influx_user, password=influx_password, database=influx_database)
influx_client.switch_database(influx_database)

# Define measurement name
meas_name = "expenses"

while True:
    print(f"Currently writing to database named: {meas_name}")
    print("Select an option:")
    print("1. Add new expense")
    print("2. View expenses summary")
    print("3. Modify existing expense")
    print("4. Exit")

    choice = int(input())

    if choice == 1:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cur = influx_client.query(f'''SELECT DISTINCT("category") FROM {meas_name}''')

        categories = cur.get_points()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category['category']}")
        print(f"{len(categories) + 1}. Create a new category")
              
        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else:
            category = list(categories)[category_choice - 1]['category']

        price = input("Enter the price of the expense: ")

        # Create JSON data for InfluxDB
        json_body = [
            {
                "measurement": meas_name,
                "time": date,
                "fields": {
                    "description": description,
                    "category": category,
                    "price": float(price),
                },
            }
        ]

        # Write data to InfluxDB
        influx_client.write_points(json_body)

    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View monthly expenses by category")
        # may add additional options in the future

        view_choice = int(input())

        if view_choice == 1:
            cur = influx_client.query(f"SELECT * FROM {meas_name}")
            expenses = cur.get_points()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cur = influx_client.query(f"""SELECT "category", SUM("price") FROM {meas_name}
                        WHERE time >= '{year}-{month}-01' AND time < '{year}-{int(month) + 1}-01'
                        GROUP BY "category" """)
            expenses = cur.get_points()
            for expense in expenses:
                print(f"Category: {expense['category']}, Total: {expense['sum']}")
        else:
            print("Exiting program")
            exit()

    elif choice == 3:
        expense_id = int(input("Enter the ID of the expense you want to modify: "))

        cur = influx_client.query(f'SELECT * FROM {meas_name} WHERE "id" = {expense_id}')
        expense = list(cur.get_points())

        if not expense:
            print("Expense not found.")
        else:
            expense = expense[0]
            print("Current expense details:")
            print("ID:", expense['id'])
            print("Date:", expense['time'])
            print("Description:", expense['description'])
            print("Category:", expense['category'])
            print("Price:", expense['price'])

            # Get new values for modification
            new_date = input("Enter the new date (YYYY-MM-DD) (press Enter to keep the current value): ") or expense['time']
            new_description = input("Enter the new description (press Enter to keep the current value): ") or expense['description']
            new_category = input("Enter the new category (press Enter to keep the current value): ") or expense['category']
            new_price = input("Enter the new price (press Enter to keep the current value): ") or expense['price']

            # Update the expense in the database
            influx_client.write_points([{
                "measurement": meas_name,
                "tags": {"id": expense['id']},
                "time": new_date,
                "fields": {
                    "description": new_description,
                    "category": new_category,
                    "price": float(new_price),
                },
            }], database=influx_database)
            
            print("Expense updated successfully.")

    else:
        print("Exiting program")
        exit()

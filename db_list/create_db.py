from influxdb import InfluxDBClient

# Define InfluxDB connection parameters
influx_host = 'localhost'
influx_port = 8086
influx_user = 'username'
influx_password = 'password'
influx_database = 'expenses'

# Connect to InfluxDB
influx_client = InfluxDBClient(host=influx_host, port=influx_port, username=influx_user, password=influx_password)

# Create a new database
influx_client.create_database(influx_database)

# Switch to the created database
influx_client.switch_database(influx_database)

# Define a measurement name
meas_name = "expenses"

# Define a retention policy (optional)
retention_policy = "autogen"

# Create a retention policy (optional)
influx_client.create_retention_policy(retention_policy, '30d', 1, default=True)

# Commit changes
influx_client.close()

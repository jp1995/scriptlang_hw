import mysql.connector


class Connection:
    """Connection credentials and database functionality."""

    def __init__(self, host: str, username: str, password: str, database):
        """Class constructor."""
        self.database = database
        self.mydb = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        self.mycursor = self.mydb.cursor()

    def create_db(self, database_name: str):
        """Create a database."""
        self.mycursor.execute(f"CREATE DATABASE {database_name}")

    def check_db(self):
        """List all databases."""
        self.mycursor.execute("SHOW DATABASES")
        for x in self.mycursor:
            print(x)

    def create_table(self, table_name: str, *args: str):
        """Create table."""
        self.mycursor.execute(f"CREATE TABLE {table_name} ({args[0]})")
        for i in args[1:]:
            self.mycursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {i}")

    def check_table(self):
        """List all tables."""
        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            print(x)

    def set_primary_key(self, table_name: str):
        """Set a primary key."""
        self.mycursor.execute(f"ALTER TABLE {table_name} ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

    def insert_multiple_rows(self, table_name, table_values: list, *args: str):
        """Insert multiple rows."""
        cols = ''
        values = '%s, ' * len(table_values[0])
        for i in args:
            cols += i + ', '
        cols = cols[:-2]
        values = values[:-2]
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"
        self.mycursor.executemany(sql, table_values)
        print(self.mycursor.rowcount, "was inserted.")

    def select_from_table(self, table_name):
        """Select from a table."""
        self.mycursor.execute(f"SELECT * FROM {table_name}")
        myresult = self.mycursor.fetchall()
        for x in myresult:
            print(x)

    def drop_table(self, table_name):
        """Drop table if it exists."""
        self.mycursor.execute(f"DROP TABLE IF EXISTS {table_name}")


if __name__ == '__main__':
    Connection("localhost", "user", "password", None).create_db('mydatabase')
    init = Connection("localhost", "user", "password", "mydatabase")
    init.check_db()
    init.create_table("customers", 'name VARCHAR(255)', 'address VARCHAR(255)')
    init.check_table()
    init.set_primary_key('customers')
    customers_list = [
        ('Peter', 'Lowstreet 4'),
        ('Amy', 'Apple st 652'),
        ('Hannah', 'Mountain 21'),
        ('Michael', 'Valley 345'),
        ('Sandy', 'Ocean blvd 2'),
        ('Betty', 'Green Grass 1'),
        ('Richard', 'Sky st 331'),
        ('Susan', 'One way 98'),
        ('Vicky', 'Yellow Garden 2'),
        ('Ben', 'Park Lane 38'),
        ('William', 'Central st 954'),
        ('Chuck', 'Main Road 989'),
        ('Viola', 'Sideway 1633')
    ]
    init.insert_multiple_rows('customers', customers_list, 'name', 'address')
    init.select_from_table('customers')
    init.drop_table('customers')

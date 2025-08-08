import psycopg2

# Function to create a connection to the PostgreSQL database
def create_connection():
    return psycopg2.connect(
        host="172.17.0.3",                   # or your host name
        user="postgres",                   # PostgreSQL username
        password="1234",                   # PostgreSQL password
        dbname="userinfo"   # PostgreSQL database name
    )

# Function to create the table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usernames (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    connection.commit()
    cursor.close()

# Function to insert a name into the database and write to file
def insert_name(connection, name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO usernames (name) VALUES (%s)", (name,))
    connection.commit()
    cursor.close()

    with open("servers.txt", "a") as file:
        file.write(name + "\n")

# Function to fetch all usernames from the database
def fetch_all_usernames(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM usernames")
    usernames = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return usernames

# Main function
def main():
    connection = create_connection()
    create_table(connection)

    while True:
        print("1. Add a name")
        print("2. Show all usernames")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter a name: ")
            insert_name(connection, name)
            print(f"Name '{name}' added to the database.")
        elif choice == "2":
            usernames = fetch_all_usernames(connection)
            if usernames:
                print("Usernames in the database:")
                for name in usernames:
                    print(name)
            else:
                print("No usernames found in the database.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()

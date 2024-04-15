import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy

# Create a SQLAlchemy engine
engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:Nigamasree.27@localhost/my_management")

try:
    # Fetch data from the database
    query = """
        SELECT DATE_FORMAT(check_in_date, '%Y-%m-%d') AS date, 
               SUM(expenditure) AS expenditure, 
               SUM(cost) AS cost, 
               SUM(num_guests) AS total_guests
        FROM guests
        GROUP BY DATE_FORMAT(check_in_date, '%Y-%m-%d')
    """
    df = pd.read_sql(query, engine)

    # Calculate profit
    df['revenue'] = df['expenditure'] - df['cost']

    # Plotting
    plt.figure(figsize=(14, 8))

    # Plot Expenditure
    plt.plot(df['date'], df['expenditure'], label='Expenditure', color='blue')

    # Plot Cost
    plt.plot(df['date'], df['cost'], label='Cost', color='red')

    # Plot Total Guests
    plt.plot(df['date'], df['total_guests'], label='Total Guests', color='green')

    # Plot Profit
    plt.plot(df['date'], df['revenue'], label='Profit', color='orange')

    # Set title and labels
    plt.title('Hotel Revenue and Factors Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Amount / Number of Guests', fontsize=14)

    # Show legend
    plt.legend(fontsize=12)

    # Show grid
    plt.grid(True)

    # Show plot
    plt.show()

except sqlalchemy.exc.OperationalError as error:
    print("Error reading data from MySQL:", error)

finally:
    # Dispose the engine
    engine.dispose()

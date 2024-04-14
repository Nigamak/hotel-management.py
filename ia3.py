from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Placeholder function for demonstration
def calculate_expenditure(room_type, room_cost, check_in_date, check_out_date):
    # Dummy implementation, replace with your logic
    duration = (check_out_date - check_in_date).days
    return duration * room_cost

# Placeholder function for demonstration
def get_room_cost(room_type):
    # Dummy implementation, replace with your logic
    return 4500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form['name']
    email = request.form['email']
    mobile_no = request.form['mobile_no']
    check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d').date()
    check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d').date()
    room_type = request.form['room_type']
    num_guests = int(request.form['num_guests'])
    special_requests = request.form['special_requests']

    # Get the cost of the selected room type
    room_cost = get_room_cost(room_type)

    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nigamasree.27",
            database="myrestaurant"
        )

        cursor = connection.cursor()

        # Get the next available room number
        cursor.execute("SELECT MAX(roomno) FROM guests")
        last_roomno = cursor.fetchone()[0] or 299  # Get the last room number or set to 299 if no rooms are allotted yet
        next_roomno = min(500, last_roomno + 1)  # Ensure the room number does not exceed 500

        # Calculate expenditure based on room type, room cost, and duration of stay
        expenditure = calculate_expenditure(room_type, room_cost, check_in_date, check_out_date)

        # SQL query to insert data into the database
        insert_query = """
        INSERT INTO guests (Name, mobile_no, check_in_date, check_out_date, room_type, roomno, num_guests, special_requests, expenditure,cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Data tuple for insertion
        data = (name, mobile_no, check_in_date, check_out_date, room_type, next_roomno, num_guests, special_requests, expenditure, room_cost)

        # Execute the INSERT query
        cursor.execute(insert_query, data)

        # Commit changes to the database
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Flash a success message
        flash("Room booked successfully!", "success")

        # Redirect to the home page
        return redirect('/')
    
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table:", error)
        flash("Failed to book room. Please try again later.", "error")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

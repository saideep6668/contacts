import MySQLdb
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nani@1234'
app.config['MYSQL_DB'] = 'nikil'

mysql = MySQL(app)

# ...
@app.route('/')
def layout():
    return render_template('layout.html')
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        # Get form data including the uploaded image
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        
        # Handle image upload
        image = request.files['image']
        if image:
            # Securely save the image file with a unique name
            filename = secure_filename(image.filename)
            image.save('uploads/' + filename)  # Save the image to the "uploads" directory
            image_url = url_for('uploaded_file', filename=filename)
        else:
            image_url = None

        # Insert the data into the database, including the image URL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (first_name, last_name, email, phone_number, image) VALUES (%s, %s, %s, %s, %s)",
                    (first_name, last_name, email, phone_number, image_url))
        mysql.connection.commit()
        cur.close()

        flash('Contact added successfully', 'success')
        return redirect(url_for('view_contacts'))

    return render_template('add_contact.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


@app.route('/view_contacts')
def view_contacts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, first_name, last_name, email, image FROM contacts")
    contacts = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'email': row[3], 'image': row[4]} for row in cur.fetchall()]
    cur.close()

    return render_template('view_contacts.html', contacts=contacts)


@app.route('/view_contact/<int:id>')
def view_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact = cur.fetchone()
    cur.close()

    if contact:
        print("Contact data retrieved successfully:", contact)
        return render_template('view_contact.html', contact=contact)
    else:
        flash('Contact not found', 'danger')
        return redirect(url_for('view_contacts'))

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact_tuple = cur.fetchone()
    
    if contact_tuple:
        # Convert the contact tuple to a dictionary
        contact = {
            'id': contact_tuple[0],
            'first_name': contact_tuple[1],
            'last_name': contact_tuple[2],
            'email': contact_tuple[3],
            'phone_number': contact_tuple[4]
        }

        if request.method == 'POST':
            # Process the form data here and update the contact in the database
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone_number = request.form['phone_number']

            cur.execute("UPDATE contacts SET first_name=%s, last_name=%s, email=%s, phone_number=%s WHERE id=%s",
                        (first_name, last_name, email, phone_number, contact['id']))
            mysql.connection.commit()
            cur.close()

            flash('Contact updated successfully', 'success')
            return redirect(url_for('view_contacts'))

        return render_template('edit_contact.html', contact=contact)
    else:
        flash('Contact not found', 'danger')
        return redirect(url_for('view_contacts'))


@app.route('/delete_contact/<int:id>', methods=['GET', 'POST'])
def delete_contact(id):
    if request.method == 'POST':
        # Perform the actual deletion of the contact
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM contacts WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        flash('Contact deleted successfully', 'success')
        return redirect(url_for('view_contacts'))
    
    # If it's a GET request, display a confirmation page
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact_tuple = cur.fetchone()
    cur.close()

    if contact_tuple:
        contact = {
            'id': contact_tuple[0],
            'first_name': contact_tuple[1],
            'last_name': contact_tuple[2],
            'email': contact_tuple[3],
            'phone_number': contact_tuple[4],
            'image': contact_tuple[5]
        }

        return render_template('delete_contact.html', contact=contact)
    else:
        flash('Contact not found', 'danger')
        return redirect(url_for('view_contacts'))



if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
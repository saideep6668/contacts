from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
import os
import uuid

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'saideep'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'saideep1234'
app.config['MYSQL_DB'] = 'saideep'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_filename(filename):
    extension = filename.rsplit('.', 1)[1]
    unique_filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

@app.route('/')
def index():
    search_query= request.form.get("search")

    if search_query:
        cur = mysql.connection.cursor()
        query= "SELECT  id, name, email, image_url FROM contacts WHERE name LIKE %s"
        cur.execute(query,("%" + search_query + "%"))
        contacts = [{'id': row[0], 'name': row[1], 'email': row[2], 'image_url': row[3]} for row in cur.fetchall()]
        cur.close()
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, image_url FROM contacts")
        contacts = [{'id': row[0], 'name': row[1], 'email': row[2], 'image_url': row[3]} for row in cur.fetchall()]
        cur.close()

    return render_template('index.html', contacts=contacts)


@app.route("/details/<int:id>")
def details(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contacts = cur.fetchone()
    cur.close()
    # print(contacts)

    if contacts:
        return render_template("details.html", contacts=contacts)
    else:
        flash("Contact not found.", "danger")
        return redirect(url_for("index"))



@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = generate_filename(image.filename)
                image.save(filename)
                image_url = url_for('uploaded_file', filename=os.path.basename(filename))
            else:
                image_url = None
        else:
            image_url = None

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO contacts (name, email, phone, image_url) VALUES (%s, %s, %s, %s)",
            (name, email, phone, image_url)
        )
        mysql.connection.commit()
        cur.close()

        flash("Contact added successfully.", "success")
        return redirect(url_for("index"))
    return render_template("add.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact = cur.fetchone()
    cur.close()

    if not contact:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE contacts SET name = %s, email = %s, phone = %s  WHERE id = %s",
            (name, email, phone,  id)
        )
        mysql.connection.commit()
        cur.close()

        flash("Contact updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", contact=contact)

@app.route("/delete/<int:id>")
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash("Contact deleted successfully.", "success")
    return redirect(url_for("index"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)




























# from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
# import os
# import uuid
# import json
# # from werkzeug.utils import secure_filename

# app = Flask(__name__ ,static_url_path='/static')
# app.secret_key = 'saideep'

# # Sample initial contacts
# contacts = [
#     {
#         "id": 1,
#         "firstname": "Shoeb",
#         "email": "shoeb@brio.co.in",
#         "phone": "9032324440",
#         "image_url" : "https://i.ibb.co/V3513MS/image4.png"
#     },
#     {
#         "id": 2,
#         "name": "Vamshi",
#         "email": "vamsidhar.muggullah@brio.co.in",
#         "phone": "9177395206",
#         "image_url": "https://scontent.fhyd11-3.fna.fbcdn.net/v/t39.30808-6/355154179_6417338745022757_1167272310648121438_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=a2f6c7&_nc_ohc=Wo50tlLlbjMAX9D1EgV&_nc_ht=scontent.fhyd11-3.fna&oh=00_AfCw0R1R15BXpI6h2oCBYZSZAPzoDWHTu6E3rcfsdGPbXQ&oe=650CADB0",
#     },
# ]
# # "image_url": "https://i.ibb.co/HFdSBPr/image1.jpg",
# # https://i.ibb.co/DkMpfvz/image3.jpg

# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def generate_filename(filename):
#     extension = filename.rsplit('.', 1)[1]
#     unique_filename = f'{uuid.uuid4()}.{extension}'
#     return os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

# # Helper function to save contacts to local storage
# def save_contacts():
#     with open("contacts.json", "w") as file:
#         json.dump(contacts, file)

# # Helper function to load contacts from local storage
# def load_contacts():
#     try:
#         with open("contacts.json", "r") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return []

# @app.route("/")
# def index():
#     return render_template("index.html", contacts=contacts)

# # Add a new route for displaying contact details
# @app.route("/details/<int:id>")
# def contact_details(id):
#     contact = next((c for c in contacts if c["id"] == id), None)
#     if not contact:
#         return redirect(url_for("index"))
#     return render_template("details.html", contact=contact)


# @app.route("/add", methods=["GET", "POST"])
# def add_contact():
#     if request.method == "POST":
#         new_contact = {
#             "id": len(contacts) + 1,
#             "name": request.form["name"],
#             "email": request.form["email"],
#             "phone": request.form["phone"],
#         }

#         if 'image' in request.files:
#             image = request.files['image']
#             if image.filename != '':
#                 filename = generate_filename(image.filename)
#                 image.save(filename)
#                 new_contact["image_url"] = url_for('uploaded_file', filename=os.path.basename(filename))

#         contacts.append(new_contact)
#         save_contacts()
#         flash("Contact added successfully.", "success")
#         return redirect(url_for("index"))
#     return render_template("add.html")

# @app.route("/edit/<int:id>", methods=["GET", "POST"])
# def edit_contact(id):
#     contact = next((c for c in contacts if c["id"] == id), None)
#     if not contact:
#         return redirect(url_for("index"))

#     if request.method == "POST":
#         contact["name"] = request.form["name"]
#         contact["email"] = request.form["email"]
#         contact["phone"] = request.form["phone"]
#         save_contacts()
#         flash("Contact updated successfully.", "success")
#         return redirect(url_for("index"))

#     return render_template("edit.html", contact=contact)

# @app.route("/delete/<int:id>")
# def delete_contact(id):
#     contact = next((c for c in contacts if c["id"] == id), None)
#     if contact:
#         contacts.remove(contact)
#         save_contacts()
#         flash("Contact deleted successfully.", "success")
#     return redirect(url_for("index"))

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# if __name__ == "__main__":
#     app.run(debug=True)

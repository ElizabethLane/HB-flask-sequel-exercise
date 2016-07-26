from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""
    

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html", first=first, last=last, github=github)

    return html

@app.route("/create-new-student")
def student_add():
    """Add a student"""

    html = render_template("create_new_student.html")

    return html

@app.route("/student-added", methods=['POST'])
def create_student():
    
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    github = request.form.get('github')

    QUERY = "INSERT INTO students VALUES(:firstname, :lastname, :github)"

    hackbright.db.session.execute(QUERY, {'firstname': first_name, 
                       'lastname': last_name, 'github': github})

    hackbright.db.session.commit()

    NEW_QUERY = """SELECT first_name, last_name, github
                FROM students 
                """

    cursor = hackbright.db.session.execute(NEW_QUERY)
    result = cursor.fetchall()


    return "Success! You've added the student. Here's your new database. \n %s" % (result)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

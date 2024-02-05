from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    snum = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.snum}: {self.title}"


# Drop tables
with app.app_context():
    db.drop_all()

# Recreate tables
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def home():
    # Handling POST Request
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # Check if title and description are not empty
        if title and description:
            todo = Todo(title=title, description=description)
            db.session.add(todo)
            db.session.commit()

            # Redirect to the same route using a GET request to avoid form resubmission on refresh
            return redirect(url_for('home'))

    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Convert UTC time to Indian Standard Time (IST)
    ist = pytz.timezone('Asia/Kolkata')
    current_time_ist = current_time_utc.replace(
        tzinfo=pytz.utc).astimezone(ist)

    # Setting up todos
    allTodos = Todo.query.all()

    return render_template("index.html", current_time=current_time_ist, allTodos=allTodos)


@app.route('/about')
def about():
    aboutInfo = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illum architecto inventore eum. Omnis sapiente laudantium veniam quos ratione unde quam, nemo eaque expedita nulla eos doloribus totam voluptates illum natus possimus recusandae accusamus at dolorem magni quia. Architecto minus soluta iusto iste doloremque, eaque ducimus facilis nesciunt ab commodi magni a perferendis id ipsa ad adipisci consequatur nisi culpa molestiae ea dicta autem natus veniam! Esse accusantium veritatis optio vero magnam quas, qui modi nesciunt blanditiis praesentium repellendus magni reiciendis voluptatum ducimus quisquam incidunt doloremque rerum exercitationem minus dolore eos laborum ullam nostrum? Vero, ad sequi temporibus similique aut quisquam facilis accusantium nobis voluptatibus nostrum expedita, animi atque doloremque ea, voluptatem magnam voluptates maxime praesentium natus aspernatur! Non eligendi magnam incidunt dolore voluptatibus, aspernatur maxime doloremque distinctio laboriosam velit deleniti pariatur exercitationem sunt praesentium enim ab perspiciatis ad. Minima odit quod fugit aspernatur optio exercitationem recusandae iure praesentium labore, sint excepturi veritatis dignissimos id. Veritatis eius repellendus sequi quibusdam maiores harum aspernatur itaque fugiat voluptate nemo accusamus, aliquam ut quia autem adipisci maxime architecto inventore sunt facere, ullam rem quae labore? Voluptates obcaecati voluptatum pariatur cum quisquam quod dolor atque deleniti culpa, aspernatur asperiores veritatis rem mollitia. Provident, vel ex!"
    return render_template("about.html", aboutInfo=aboutInfo)


@app.route('/update/<int:snum>', methods=['GET', 'POST'])
def update(snum):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']

        if title and description:
            todo = Todo.query.filter_by(snum=snum).first()
            todo.title = title
            todo.description = description
            db.session.add(todo)
            db.session.commit()

            return redirect(url_for('home'))

    todo = Todo.query.get(snum)

    return render_template("update.html", todo=todo)


@app.route('/delete/<int:snum>')
def delete(snum):
    db.session.delete(Todo.query.get(snum))
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/contact')
def contact():
    contactInfo = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illum architecto inventore eum. Omnis sapiente laudantium veniam quos ratione unde quam, nemo eaque expedita nulla eos doloribus totam voluptates illum natus possimus recusandae accusamus at dolorem magni quia. Architecto minus soluta iusto iste doloremque, eaque ducimus facilis nesciunt ab commodi magni a perferendis id ipsa ad adipisci consequatur nisi culpa molestiae ea dicta autem natus veniam! Esse accusantium veritatis optio vero magnam quas, qui modi nesciunt blanditiis praesentium repellendus magni reiciendis voluptatum ducimus quisquam incidunt doloremque rerum exercitationem minus dolore eos laborum ullam nostrum? Vero, ad sequi temporibus similique aut quisquam facilis accusantium nobis voluptatibus nostrum expedita, animi atque doloremque ea, voluptatem magnam voluptates maxime praesentium natus aspernatur! Non eligendi magnam incidunt dolore voluptatibus, aspernatur maxime doloremque distinctio laboriosam velit deleniti pariatur exercitationem sunt praesentium enim ab perspiciatis ad. Minima odit quod fugit aspernatur optio exercitationem recusandae iure praesentium labore, sint excepturi veritatis dignissimos id. Veritatis eius repellendus sequi quibusdam maiores harum aspernatur itaque fugiat voluptate nemo accusamus, aliquam ut quia autem adipisci maxime architecto inventore sunt facere, ullam rem quae labore? Voluptates obcaecati voluptatum pariatur cum quisquam quod dolor atque deleniti culpa, aspernatur asperiores veritatis rem mollitia. Provident, vel ex!"
    return render_template("contact.html", contactInfo=contactInfo)


if __name__ == "__main__":
    app.run(debug=True)

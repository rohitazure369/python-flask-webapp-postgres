
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# change below value based on your configuration
###############################################
server_url = "rkpostgressql.postgres.database.azure.com"
db_name = "pythontaskapp"
username = "sqladmin"
password = "AzureAdmin100!"

####################################

# Construct the SQLALCHEMY_DATABASE_URI using the variables

database_uri = f"postgresql://{username}:{password}@{server_url}/{db_name}"

# Assign the constructed URI to app.config
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri




db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        new_user = User(name=request.form['name'])
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

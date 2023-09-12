from flask import Flask, render_template , url_for, flash, redirect, request, jsonify
from forms import admin_login_form, User_login_form
from flask_login import LoginManager, UserMixin 
from flask_login import login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy as sq
from sqlalchemy import func, ForeignKey
import datetime
from sqlalchemy.orm import session, sessionmaker, relationship





app = Flask(__name__)
app.secret_key = '1227kgjs68&*jhfdjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///VotingSystem.db'
app.config['JSONIFY_MIMETYPE'] = 'application/json'
db = sq(app)
login_manager = LoginManager(app)



@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)



### MODELS #################################################################

class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    Tell = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def is_active(self):
        return True
    

# Election database
class Elections(db.Model):
    __tablename__ = 'Elections'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ElectionName = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    startDate = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow)
    EndDate = db.Column(db.Date, nullable=False)
    Isactive = db.Column(db.Boolean, nullable=False)


class candidates(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    electionsId = db.Column(db.Integer, ForeignKey('Elections.id') , nullable=False)
    fullName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tell = db.Column(db.Integer, nullable=False)
    birthDate = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(255), nullable=False)
    halheys = db.Column(db.String, nullable=False)
    point1 = db.Column(db.String, nullable=False)
    point2 = db.Column(db.String)
    point3 = db.Column(db.String)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    election = relationship('Elections', backref='candidates')
    







with app.app_context():
    db.create_all()
    













##### ROUTING #################################
@app.route('/')
def Home():
    return render_template("index.html")

@app.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('Home'))




@app.route('/admin_login' , methods=['POST', 'GET'])
def admin_login():

    if current_user.is_authenticated:
        return redirect(url_for('AdminHome'))

    Form = admin_login_form()
 
    if Form.validate_on_submit():
        user = AdminUser.query.filter_by(username=Form.username.data).first()
        if user and Form.password.data == user.password:
            flash(f"Successfully logged in" , category="success")
            login_user(user)
            return redirect(url_for('AdminHome'))
        else:
            flash(f'Invalid username or password', category='danger')


    return render_template("admin_login.html" , form = Form, title="Admin Login")




@app.route('/admin/Dashboard', methods = ['GET'])
def AdminHome():
    if not current_user.is_authenticated:
        flash(f'Please login first...', category='danger')
        return redirect(url_for('admin_login'))
    else:
        # user = request.args.get('user')
        # email = request.args.get('email')
        image = candidates.query.get(1) #==========================================================================?????
        print(image)
        return render_template('admin/AdminHome.html', user= current_user   )
    

@app.route('/admin/ElectionRegistration' , methods=['POST', 'GET'])
def ElectionRegistration():
    if not current_user.is_authenticated:
        flash(f'Please login first...', category='danger')
        return redirect(url_for('admin_login'))
    else:
        if request.method == 'GET':
            return render_template('admin/ElectionRegister.html', title='Election Registeration' , user= current_user)
        elif request.method == 'POST':
            max_id = db.session.query(func.max(Elections.id)).scalar()
            if max_id == None:
                max_id = 1
            else:
                max_id += 1

            elecId = max_id
            elecName = request.form.get('ElectionName')
            elecdesc = request.form.get('desc')
            elecEndDate_str = request.form.get('EndDate')
            elecEndDate = datetime.datetime.strptime(elecEndDate_str, '%Y-%m-%d' ).date()
            elecIsActive_bool = request.form.get('IsActive')
            # print(elecIsActive_bool)
            if elecIsActive_bool == "Yes":
                elecIsActive = True
            else:
                elecIsActive = False
            
            NewElection = Elections(id=elecId, ElectionName=elecName, description= elecdesc,EndDate=elecEndDate, Isactive=elecIsActive)
            db.session.add(NewElection)
            db.session.commit()
            flash(f"successfully generated new election", category='success')
            return render_template('admin/ElectionRegister.html', title='Election Registeration' , user=current_user)



@app.route('/admin/NewCandidate', methods=['POST', 'GET'])
def CandidateRegistration():
    if not current_user.is_authenticated:
        flash(f'Please login first...', category='danger')
        return redirect(url_for('admin_login'))
    else:
        elections = Elections.query.filter(Elections.Isactive == True ).all()
        if request.method == 'POST':
            max_id = db.session.query(func.max(candidates.id)).scalar()
            if max_id:
                max_id += 1
            else:
                max_id = 1

            electioName = request.form.get('ElecName')
            election = db.session.query(Elections).filter_by(ElectionName=electioName).first()
            
            
            id = max_id
            electionId = election.id
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            Phone = request.form.get('Phone')
            birthDate_str = request.form.get('date')
            birthDate = datetime.datetime.strptime(birthDate_str, '%Y-%m-%d' ).date()
            sex = request.form.get('sex')
            halhays = request.form.get('halhays')
            point1 = request.form.get('point1')
            point2 = request.form.get('point2')
            point3 = request.form.get('point3')
            description = request.form.get('description')
            image_file = request.files['image'].read()

            NewCandidate = candidates(id=id, electionsId=electionId, fullName=fullname, email=email, tell=Phone, birthDate=birthDate, sex=sex, 
                                      halheys=halhays, point1=point1, point2=point2, point3=point3, description=description, image=image_file)
            db.session.add(NewCandidate)
            db.session.commit()



        return render_template('admin/candidateRegister.html', elections=elections, user= current_user, title= 'CandidateRegistration')



@app.route('/admin/elections')
def elections():
    elections = db.session.query(Elections).all()

    return render_template('admin/elections.html', elections=elections, user= current_user, title="All Elections")



@app.route('/admin/Candidates' , methods=['POST'])
def candidatesPAge():
    if request.method == 'POST':
        try:
            election_id = request.json['election']


            print("Election ID: ",  election_id)
            # if request.method == 'GET':

            candidate = db.session.query(candidates).filter(candidates.electionsId == election_id).all()
            election = db.session.query(Elections).filter(Elections.id == election_id).first()
            print("election: ", election)
            print("Canndidate:" , candidate)
            response_data = {'message': 'Success'}
            new = {'Data': 'New data'}
            print(jsonify(new))
            return jsonify(response_data)
            # return render_template('admin/candidates.html', title='Candidates', election=election, candidates=candidate, user=current_user)
            # print("Hello!")
        except Exception as e:
            error_response = {'error': 'Invalid data', 'details': str(e)}
            return jsonify(error_response), 400





@app.route('/admin/candidatesfghsf2')
def candidatefgzf2():
    election = request.args.get('election')
    candidate = request.args.get('candidates')
    return render_template('admin/candidates.html', title='Candidates', election=election, candidates=candidate, user=current_user) 





# @app.route('/admin/Edit_elections')
# def edit_elections():
#     id = request.

 



# ========= User Management system =============================
@app.route('/User_login' , methods=['POST', 'GET'])
def User_login():
    Form = User_login_form()

    if Form.validate_on_submit():
        username = Form.username.data
        password = Form.password.data

        if username == "1" and password == "1":
            return render_template("index.html")
        else:
            flash(f'Invalid username or password', category='danger')
            return render_template("index.html")


    return render_template("user_login.html" , form = Form, title="User Login")



if __name__ == '__main__':
    app.run(debug=True)
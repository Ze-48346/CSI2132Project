from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import *
from sqlalchemy.orm import query, session, relationship


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@localhost:5432/CSI2132Project'  # 这里改成自己本地的数据库用户和密码
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app = Flask(__name__)
app.secret_key = "CSI2132"
app.config.from_object(Config)
db = SQLAlchemy(app)
Bootstrap(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            identification = request.form.get("identification")
            if identification == "Dentist":
                return redirect(url_for('dentist_page'))
            if identification == "Receptionist":
                return redirect(url_for('receptionist_page'))
            if identification == "Patient":
                return redirect(url_for('patient_page'))
        else:
            flash("Wrong")
    if request.method == 'GET':
        return render_template('Login.html')


@app.route("/patient", methods=['GET', 'POST'])
def patient_page():
    if request.method == 'GET':
        return render_template('PatientUI.html')
    if request.method == 'POST':
        if request.form.get('btn_check_historyMedical') == 'btn_check_historyMedical':
            SSN = request.form.get('check_historyMedical')
            users = User.query.filter(User.SSN == SSN)
            h_medicals = History_Medical.query.filter(History_Medical.patient_SSN == SSN).all()
            if not h_medicals:
                flash("Doesn't exist")
            return render_template('PatientUI.html', h_medicals=h_medicals)
        if request.form.get('check_upcoming_appoinment') == 'check_upcoming_appoinment':
            SSN = request.form.get('check_appointment_patient')
            appointments = Appointment.query.filter(Appointment.patient_SSN == SSN).all()
            return render_template('PatientUI.html', appointments=appointments)






@app.route("/receptionist", methods=['GET', 'POST'])
def receptionist_page():
    if request.method == 'GET':
        return render_template('ReceptionistUI.html')
    if request.method == 'POST':
        add = request.form.get('Add')
        update = request.form.get('Update')
        list = request.form.get('List')
        if add == 'Add':
            patient_SSN = request.form.get('add_SSN')
            date = request.form.get('add_appointment_date')
            start_time = request.form.get('add_start_time')
            end_time = request.form.get('add_end_time')
            dentist_SSN = request.form.get('add_dentist_SSN')
            new_Appointment = Appointment(patient_SSN=patient_SSN, date=date, start_time=start_time, end_time=end_time,
                                          Dentist_SSN=dentist_SSN)
            db.session.add(new_Appointment)
            db.session.commit()
            flash("Add success")
            return render_template('ReceptionistUI.html')
        if update == 'Update':
            patient_SSN = request.form.get('update_SSN')
            date = request.form.get('update_appointment_date')
            start_time = request.form.get('update_start_time')
            end_time = request.form.get('update_end_time')
            dentist_SSN = request.form.get('update_dentist_SSN')
            appointment = Appointment.query.filter(Appointment.patient_SSN == patient_SSN,
                                                   Appointment.date == date).first()
            if appointment:
                db.session.query(Appointment).filter(Appointment.patient_SSN == patient_SSN,
                                                     Appointment.date == date).update(
                    {'start_time': start_time, 'end_time': end_time, 'Dentist_SSN': dentist_SSN})
                db.session.commit()
                flash("Update Success")
            return render_template('ReceptionistUI.html')
        if list == 'List':
            dentists = role.query.filter(
                or_(role.identification1 == "Dentist", role.identification2 == "Dentist",
                    role.identification3 == "Dentist")).all()
            return render_template('ReceptionistUI.html', dentists=dentists)


# @app.route("/receptionist", methods=['GET', 'POST'])
# def update_patientInfo():
#
#
#
# @app.route("/receptionist", methods=['GET', 'POST'])
# def list_All_dentist():


@app.route("/dentist", methods=['GET', 'POST'])
def dentist_page():
    if request.method == 'GET':
        return render_template('DentistUI.html')
    if request.method == 'POST':
        if request.form.get('check_PMH') == 'check_PMH':
            SSN = request.form.get('check_historyMedical')
            h_medicals = History_Medical.query.filter_by(patient_SSN=SSN).all()
            if not h_medicals:
                flash("Doesn't exist")
            return render_template('DentistUI.html', h_medicals=h_medicals)
        if request.form.get('Check') == 'Check':
            SSN = request.form.get('Check_appointment')
            appointments = Appointment.query.filter(Appointment.patient_SSN == SSN).all()
            return render_template('DentistUI.html', appointments=appointments)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        gender = request.form.get("gender")
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        phone_number = request.form.get("phone_number")
        SSN = request.form.get("SSN")
        identification = request.form.get("identification")
        address = request.form.get("Address")
        user = User.query.filter(User.SSN == SSN).first()
        if user:
            identification_copy = role.query.filter(role.SSN == SSN).filter(
                or_(role.identification1 == identification, role.identification2 == identification,
                    role.identification3 == identification)).first()
            if identification_copy:
                flash("Your already sign up as " + identification)
            else:
                identification_m = role.query.filter(role.SSN == SSN).first()
                identification1_1 = identification_m.identification1
                identification2_1 = identification_m.identification2
                if not identification1_1:
                    db.session.query(role).filter(User.SSN == SSN).update(
                        {'identification1': identification})
                elif not identification2_1:
                    db.session.query(role).filter(User.SSN == SSN).update(
                        {'identification2': identification})
                else:
                    db.session.query(role).filter(User.SSN == SSN).update(
                        {'identification3': identification})

                db.session.commit()

        else:
            new_User = User(firstname=firstname, lastname=lastname, gender=gender, email=email, password=password,
                            phone=phone_number, SSN=SSN, address=address)

            new_role = role(SSN=SSN, identification1=identification, user_SSN=SSN)

            db.session.add(new_User)
            db.session.add(new_role)
            db.session.commit()

        return redirect(url_for('index'))


class User(db.Model):
    __tablename__ = 'User'
    SSN = Column(Integer, primary_key=true, unique=true)
    firstname = Column(String(40))
    lastname = Column(String(40))
    password = Column(String(40))
    gender = Column(String(40))
    email = Column(String(40))
    phone = Column(String(40))
    address = Column(String(40))
    province = Column(String(40))
    role = relationship('role', backref='User')

    History_Medical = relationship('History_Medical', backref='User')

    Appointment = relationship('Appointment', backref='User')


class role(db.Model):
    __tablename__ = 'role'
    SSN = Column(Integer, primary_key=true, unique=true)
    identification1 = Column(String(30))
    identification2 = Column(String(30))
    identification3 = Column(String(30))
    user_SSN = Column(Integer, ForeignKey('User.SSN'))


class Appointment(db.Model):
    __tablename__ = 'Appointment'
    patient_SSN = Column(Integer, primary_key=true)
    date = Column(String(30))
    start_time = Column(String(30))
    end_time = Column(String(30))
    Dentist_SSN = Column(String(30))
    user_SSN = Column(Integer, ForeignKey('User.SSN'))


class History_Medical(db.Model):
    __tablename__ = 'History_Medical'
    patient_SSN = Column(Integer, primary_key=true)
    pass_appointmentdate = Column(String(30))
    record = Column(String(30))
    user_SSN = Column(Integer, ForeignKey('User.SSN'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)

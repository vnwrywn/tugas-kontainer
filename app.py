from flask import Flask, render_template, url_for, request, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db = SQLAlchemy(app)
app.secret_key = 'SFiEuxaK90EFuQ_j9X9_Fw'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(64), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username

class Pasien(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama = db.Column(db.String(100), nullable=False)
	pekerjaan = db.Column(db.String(100), nullable=False)
	tanggal_lahir = db.Column(db.String(100), nullable=False)
	tanggal_masuk = db.Column(db.String(100), nullable=False)
	kategori = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '<Pasien %r>' % self.id

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		akun = User.query.filter_by(username=request.form['username']).first()
		if akun is None:
			return '''
				<div class="myadmin-alert myadmin-alert-icon myadmin-alert-click alert-danger myadmin-alert-top alerttop" style="display: block;"> <i class="ti-user"></i> Username atau Password salah <a href="#" class="closed">×</a> </div>
				'''

		if request.form['password']==akun.password:
			session['loggedin'] = True
			session['id'] = akun.id
			session['username'] = akun.username
			return redirect('/rekam_data')

		return '''
			<div class="myadmin-alert myadmin-alert-icon myadmin-alert-click alert-danger myadmin-alert-top alerttop" style="display: block;"> <i class="ti-user"></i> Username atau Password salah <a href="#" class="closed">×</a> </div>
			'''

	else:
		return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/rekam_data', methods=['GET'])
def rekam_data():
	if 'id' not in session:
		return redirect('/login')

	warna = {
		0: 'blue',
		1: 'gray',
		2: 'green',
		3: 'megna',
		4: 'purple'
	}
	seluruh_pasien = Pasien.query.order_by(Pasien.id).all()
	return render_template('rekam-data.html', color=warna[randint(0, 4)], seluruh_pasien=seluruh_pasien)

@app.route('/input_data', methods=['POST', 'GET'])
def input_data():
	if 'id' not in session:
		return redirect('/login')

	if request.method == 'POST':
		pasien_baru = Pasien(nama=request.form['nama'], pekerjaan=request.form['pekerjaan'], tanggal_lahir=request.form['tanggalLahir'], tanggal_masuk=request.form['tanggalMasuk'], kategori=request.form['kategori'])
		try:
			db.session.add(pasien_baru)
			db.session.commit()
			return redirect('/rekam_data')
		except:
			return 'Terjadi kendala ketika menambahkan pasien baru'
	else:
		return render_template('input-data.html')

@app.route('/delete/<int:id>')
def delete(id):
	data = Pasien.query.get_or_404(id)

	try:
		db.session.delete(data)
		db.session.commit()
		return redirect('/rekam_data')
	except:
		return 'Terjadi kendala ketika menghapus pasien'

@app.route('/edit_data/<int:id>', methods=['GET', 'POST'])
def update(id):
	data = Pasien.query.get_or_404(id)
	if request.method == 'POST':
		data.nama = request.form['nama']
		data.tanggal_lahir = request.form['tanggalLahir']
		data.tanggal_masuk = request.form['tanggalMasuk']
		data.pekerjaan = request.form['pekerjaan']
		data.kategori = request.form['kategori']
		try:
			db.session.commit()
			return redirect('/rekam_data')
		except:
			return 'Terjadi kendala ketika mengubah data'
	else:
		return render_template('update.html', pasien=data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

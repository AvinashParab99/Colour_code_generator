import numpy as np
from PIL import Image, ImageOps
from flask import Flask, render_template, request, redirect, session
import psycopg2


# PostgreSQL database configuration
DB_NAME = "your_database_name"
DB_USER = "your_database_user"
DB_PASSWORD = "your_database_password"
DB_HOST = "your_database_host"
DB_PORT = "your_database_port"

def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def rgb_to_hex(rgb):
	return '%02x%02x%02x' % rgb


def give_most_hex(file_path, code):
	my_image = Image.open(file_path).convert('RGB')
	size = my_image.size
	if size[0] >= 400 or size[1] >= 400:
		my_image = ImageOps.scale(image=my_image, factor=0.2)
	elif size[0] >= 600 or size[1] >= 600:
		my_image = ImageOps.scale(image=my_image, factor=0.4)
	elif size[0] >= 800 or size[1] >= 800:
		my_image = ImageOps.scale(image=my_image, factor=0.5)
	elif size[0] >= 1200 or size[1] >= 1200:
		my_image = ImageOps.scale(image=my_image, factor=0.6)
	my_image = ImageOps.posterize(my_image, 2)
	image_array = np.array(my_image)

	# create a dictionary of unique colors with each color's count set to 0
	# increment count by 1 if it exists in the dictionary
	unique_colors = {} # (r, g, b): count
	for column in image_array:
		for rgb in column:
			t_rgb = tuple(rgb)
			if t_rgb not in unique_colors:
				unique_colors[t_rgb] = 0
			if t_rgb in unique_colors:
				unique_colors[t_rgb] += 1

	# get a list of top ten occurrences/counts of colors
	# from unique colors dictionary
	sorted_unique_colors = sorted(
		unique_colors.items(), key=lambda x: x[1],
	reverse=True)
	converted_dict = dict(sorted_unique_colors)
	# print(converted_dict)

	# get only 10 highest values
	values = list(converted_dict.keys())
	# print(values)
	top_10 = values[0:]
	# print(top_10)

	# code to convert rgb to hex
	if code == 'hex':
		hex_list = []
		for key in top_10:
			hex = rgb_to_hex(key)
			hex_list.append(hex)
		return hex_list
	else:
		return top_10


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		f = request.files['file']
		colour_code = request.form['colour_code']
		colours = give_most_hex(f.stream, colour_code)
		return render_template('index.html',
							colors_list=colours,
							code=colour_code)
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        cur.close()
        conn.close()

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/profile')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'logged_in' in session:
        return render_template('profile.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
	app.run(debug=True)

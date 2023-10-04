import os 
import datetime
from flask import Flask, render_template, request, redirect



app = Flask(__name__)

image_directory = r"H:\UNIVERSITY\Semister3\Online voting system\images"

def generate_filename(original_filename):
    timestamp = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}{ext}"


def save_image(image_data, image_filename):
    unique_filename = generate_filename(image_filename)
    image_path = os.path.join(image_directory, unique_filename)

    with open(image_path, "wb") as f:
        f.write(image_data)
    return unique_filename


def retrieve_image(image_filename):
    image_path = os.path.join(image_directory, image_filename)

    with open(image_path, "rb") as f:
        image_data = f.read()
    
    return image_data
    


@app.route('/')
def home():
    return render_template('admin/home.html')



@app.route('/uploadimage', methods=['POST'])
def upload_image():
    image_file = request.files['image'].read()
    # original_image_name = request.form['image_name']
    original_image_name = image_file.filename
    # original_image_name = 'Hussein.png'
    image = save_image(image_file, original_image_name)
    print("successfully uploaded image")
    return redirect('home')



if __name__ == '__main__':
    app.run(debug=True)
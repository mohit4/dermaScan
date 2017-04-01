# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from app.init_app import app, db
from app.models import UserProfileForm

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('test/test.html')


# The User page is accessible to authenticated users (users that have logged in)
@app.route('/user')
@login_required  # Limits access to authenticated users
def user_page():
    return render_template('pages/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@app.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@app.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)


UPLOAD_FOLDER = '/home/himanshu/SIH/web/images'
# from PIL import Image
# from io import BytesIO
# import base64
import json
import time
import base64
@app.route('/test1', methods=['GET', 'POST'])
def test():
    try:
        a = request.form
        filename  = str(int(time.time())) + '.png'
        filepath = UPLOAD_FOLDER + '/' + filename
        img_data = a['img_data'].split(',')[1]

        with open(filepath, "wb") as fh:
            fh.write(base64.b64decode(img_data))
        return json.dumps({"success": True})
    except: 
        return json.dumps({"success": False})


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask import send_from_directory
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/test', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user dones not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flask('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            return render_template_string('uploaded')
    return render_template('test/test.html')
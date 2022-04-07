import os
from vc_flask.MyFlask import app, Response, request, abort, url_for, send_from_directory
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def done():
    file = request.files.get('pic')
    print(file.filename)
    # print(request.files)
    # return '111'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
        return '1111'
    return '2222'

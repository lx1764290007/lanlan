from flask import Flask, jsonify, Response, request, abort, url_for,send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'D:\\upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
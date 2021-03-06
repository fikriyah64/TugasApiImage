# 6A/19090070/Fikriyah Khairunnisa
# 6A/19090097/Ika Bella Fitriani Putri

from flask import Flask, jsonify,request,flash,redirect
from itsdangerous import json
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Resource, Api
import glob

app = Flask(__name__)
UPLOAD_FOLDER = 'hasil_upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
db = SQLAlchemy(app)
CORS(app)
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db_img.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "XXXXXX"

class image_path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
  
db.create_all()

def allowed_file(filename):     
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#app.route("/uploadimage", methods=["POST"])
class index(Resource):
  def post(self):

    if 'image' not in request.files:
      flash('No file part')
      return jsonify({
            "pesan":"tidak ada form image"
          })
    file = request.files['image']
    if file.filename == '':
      return jsonify({
            "pesan":"tidak ada file image yang dipilih"
          })
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      path=("hasil_upload/"+filename)
      dataModel = image_path(path=path)
      db.session.add(dataModel)
      db.session.commit()

      return jsonify({
            "pesan":"gambar telah terupload",
            "path":path
          })
    else:
      return jsonify({
        "pesan":"bukan file image"
      })

api.add_resource(index, "/api/image", methods=["POST"])

if __name__ == '__main__':
  app.run(debug = True, port=4000)
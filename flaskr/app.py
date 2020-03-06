from flask import (
    Flask, render_template, request,
    jsonify)


from services import pre_process
# create the app
app = Flask(__name__)


@app.route('/')
def hello():

    return "Welcome to Interactive ML platform! Please create a project"
   #return render_template('template_name.html')


@app.route('/newproject',methods=['POST','GET'])
def newproject():
    if request.method == 'GET':
        return "Enter project Name and select the Dataset"

    if request.method == 'POST':
        datasetPath = request.form['path']
        proectName = request.form['project_name']
        return pre_process.main(datasetPath,proectName)


if __name__ == '__main__':
    app.run(debug=True)

from flask import (
    Flask, render_template, request
)

# create the app
app = Flask(__name__)

@app.route('/')
def hello():
   #return "Welcome to Interactive ML platform! Please create a project"
   return render_template('dashboard.html')
@app.route('/upload-csv',methods=['POST'])
def uplcsv():
	return render_template('upload-csv.html',Project_name=request.form.get('project_name'))
@app.route('/newproject',methods=['POST','GET'])
def newproject():
    if request.method == 'GET':
        return "Enter project Name and select the Dataset"
        #return render_template('template_name.html')
    if request.method == 'POST':
        """Check whether the file exists and whether it is in csv format
           Store the dataset if valid in fs
           If above conditions don't satisfy, show exception
           like 'The file format or the project name are invalid' (show a dialog box)
           If above conditions are statisfied, then create a new directory"""
        return "Validating Dataset"
        #return render_template('template_name.html,var1=value,var2=value)

@app.route('/preprocess',methods=['POST','GET'])
def preprocess():
    return "Enter project Name and select the Dataset"
    #return render_template('template_name.html',var1=value)

if __name__ == '__main__':
    app.run(debug=True)

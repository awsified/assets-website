A BASIC FLASK WEBSITE WITH DATABASE

Below is all the information needed to create a simple website with a database backend. This website uses Python's Flask and SQL Alchemy to communicate to a SQL Lite database, which can then be easily upgraded to a production MySQL app.

First create your file structure for your code repo. For typical project file structure see reference below:

my-flask-app
   ├── static/
   │   └── css/
   │       └── main.css
   ├── templates/
   │   ├── index.html
   │   └── student.html
   ├── data.py
   └── students.py

1) Navigate to my-flask-app folder and Create a virtual environment by using "python -m venv env" in windows CMD. Env can be named anything.
2) Activate environment "env\Scripts\activate"
3) Install Flask into environment "pip install flask"
4) Create a py file. All Flask apps begin with the same code. This imports the Flask class and creates a new object named app that it then assigns all the methods and properties associated with the Flask class. We call this an Instance of the class Flask. The part __name__ is called a dunder and references the name of the module it's in. Add code:

from flask import Flask
app = Flask(__name__)

5) When a request is sent to Flask it will respond based on the URL partial. For example the '/'  (as in 'www.google.com/") is the default URL of google. These partial URLs flask depends on are known as 'Routes'. We add a route next, let's tell Flask how to respond to the default url:

@app.route('/')
def hello():
    return 'Hello World!'

6) The @ portion is called a Decorator in Python. Decorators modify functions or methods. In this case it's modifying the method route() to use our path. Finally, in order to run the app directly from our environment we add two more lines of code:

if __name__ == '__main__':
    app.run(debug=True)

7) Typically __name__ represents the name of the module. When a module is ran via the command line such as a script, then __name__ is instead set to the string "__main__". So this if statement is checking to see if the name of the app running is this app. The practical use for this is we are checking to see if this app is being run as a stand-alone script or as an imported module.

8) You now have a functioning Flask app which can be ran by running the py file and browsing to 'localhost:5000'.

ADDING TEMPLATES AND STATIC FILES

Our templates folder is intended to contain special html files written to interact with Flask. These files contain a combination of html language for organization, as well as distinct syntax which jinja, Flask's templating engine, recognizes. The whole concept and goal behind Flask is to make our website modular and comprised of pieces we can reuse anywhere we want. Jinja is the magic that makes this happen.

1) To use a template you need to use 'from flask import render_template' to pull in the render_template module.

2) An example of a template .html file would look like this:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Template Title</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
</head>
<body>

<div>

    <h1>Hello, {{ name }}!</h1>

    <p>Example paragraph here.</p>

</div>

</body>
</html>

3) Note in the above template file the url_for portion. This is the partial URL syntax of how to point to a file within your Flask project.. Also note the {{ name }} portion. This is the syntax for calling your python variables into the html code.

** Syntax for a file inside a folder is different. Ex: 
scr="{{ url_for('static', filename='images/dog.jpg') }}"

4) Now that we have a template file and we've imported the module that we need in order to render it, let's use a route to call it.

5) coming soon









 

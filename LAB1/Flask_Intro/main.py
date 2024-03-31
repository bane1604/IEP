import json
from flask import Flask
from flask import jsonify
from flask import request



application = Flask( __name__ )

employees = []

class Employee:
    def __init__ ( self, first_name, last_name, email, gender, language, position ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.language = language
        self.position = position

    def __repr__ ( self ):
        return f"<Employee {self.first_name}, {self.last_name}, {self.email}, {self.gender}, {self.language}, {self.position}>"


@application.route("/", methods = ["GET"] )
def HelloWorld():
    return "<h1>Hello World!</h1>", 200

@application.route("/add", methods = ["POST"] ) 
def add():
    try:
        new_employee = Employee(
            request.json["first_name"],
            request.json["last_name"],
            request.json["email"],
            request.json["gender"],
            request.json["language"],
            request.json["position"]
        );
        employees.append(new_employee)
        return jsonify ( new_employee.__dict__ )
    except Exception as error:
        print( error )
        return "Invalid format.", 400

@application.route ( "/search", methods = ["GET"] )
def search ( ):
    result = employees
    criteria = ["first_name", "last_name", "email", "gender", "language", "position"]

    for criterium in criteria:
        if ( criterium in request.args ):
            result = [
                employee 
                for employee in result 
                if ( request.args[criterium] in getattr ( employee, criterium ) )
            ]

    return jsonify ( employees = [ employee.__dict__ for employee in result] )

@application.route ( "/upload", methods = ["POST"] )
def upload ( ):
    content = request.files["file"].stream.read ( ).decode ( )

    for line in content.split ( "\n" ):
        new_employee = Employee ( *line.split ( "," ) )
        employees.append ( new_employee )

    return jsonify ( employees = [ employee.__dict__ for employee in employees] )





if( __name__ == "__main__" ):
    application.run( debug=True ) 

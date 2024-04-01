
from flask import Flask, jsonify
from config import Configuration
from flask import request

from model import database
from model import Employee


app = Flask( __name__ )
app.config.from_object(Configuration)
database.init_app(app)

#with app.app_context():
#    database.drop_all()
#    database.create_all()

@app.route("/", methods = ["GET"] )
def hello_world():
    response = app.make_response("<h1>Hello World!</h1>")
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route("/add", methods = ["POST"] )
def add():
    try:
        new_employee = Employee(
            first_name= request.json["first_name"],
            last_name = request.json["last_name"],
            email = request.json["email"],
            gender = request.json["gender"],
            language = request.json["language"],
            position = request.json["position"]
        )

        database.session.add(new_employee)
        database.session.commit()
        #print( new_employee.dict() )
        return jsonify( new_employee.dict() ), 201
    except Exception as e:
        print(e)
        response = app.make_response("Failed.")
        response.headers['Content-Type'] = 'text/plain'
        response.status = 400
        return response
    
@app.route( "/all", methods = ["GET"] )
def all():
    try:
        result = Employee.query.all()
        return jsonify( [employee.dict() for employee in result] ), 200
    except Exception as e:
        print(e)
        return "Failed.", 400


@app.route( "/upload", methods = ["POST"] )
def upload():
    try:
        content = request.files["file"].stream.read().decode()
        for line in content.split("\n"):
            new_employee = Employee( *line.split(',') )
            database.session.add(new_employee)
        database.session.commit()
        return all()
    except Exception as e:
        print(e)
        return "Failed.", 400

@app.route("/search", methods = ["GET"])
def search():
    try:
        criteria = [ 'first_name', 'last_name', 'position', 'email', 'gender', 'language', 'position' ]
        filters = [ ] 
        for criterium in criteria:
            if ( criterium in request.args ):
                filters.append (
                    getattr ( Employee, criterium ).like ( f"%{request.args[criterium]}%" )
                )

        result = Employee.query.filter ( *filters ).all ( )

        return jsonify ( [employee.dict() for employee in result] )
    except Exception as e:
        print(e)
        return "Failed.", 400

if __name__ == "__main__":
    app.run( debug = True )


from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy ( )

class Employee ( database.Model ):
    id         = database.Column ( database.Integer, primary_key = True )
    first_name = database.Column ( database.String ( 64 ), nullable = False )
    last_name  = database.Column ( database.String ( 64 ), nullable = False )
    email      = database.Column ( database.String ( 64 ), nullable = False, unique = True )
    gender     = database.Column ( database.String ( 64 ), nullable = False )
    language   = database.Column ( database.String ( 64 ), nullable = False )
    position   = database.Column ( database.String ( 64 ), nullable = False )
    
    # added for migrate demo, has to be nullable
    dummy = database.Column ( database.Integer )

    def __init__ ( self, first_name, last_name, email, gender, language, position ):
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.gender     = gender
        self.language   = language
        self.position   = position
    def dict ( self ):
        return {
            "id": self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "email" : self.email,
            "gender" : self.gender,
            "language" : self.language,
            "position" : self.position
        }

    def __repr__ ( self ):
        return f"<Employee {self.first_name}, {self.last_name}, {self.email}, {self.gender}, {self.language}, {self.position}>"

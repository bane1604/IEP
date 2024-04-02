from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class City ( database.Model ):
    __tablename__ = "Mesto"

    id          = database.Column ( "IdMes", database.Integer, primary_key = True )
    postal_code = database.Column ( "PostBr", database.String ( 6 ), unique = True )
    name        = database.Column ( "Naziv", database.String ( 50 ) )

    # City<->HasSeatIn one-to-many
    has_seat_in_list = database.relationship ( "HasSeatIn", back_populates = "city" )

    # City<->Branch one-to-many
    branches = database.relationship ( "Branch", back_populates = "city" )

    def __repr__ ( self ):
        return f"City ( {self.id}, {self.postal_code}, {self.name} )"


class Client ( database.Model ):
    __tablename__ = "Komitent"

    id      = database.Column ( "IdKom", database.Integer, primary_key = True )
    name    = database.Column ( "Naziv", database.String ( 50 ) )
    address = database.Column ( "Adresa", database.String ( 50 ) )

    # Client<->HasSeatIn one-to-one
    has_seat_in = database.relationship ( "HasSeatIn", back_populates = "client", uselist = False )

    # Client<->Account many-to-one
    accounts = database.relationship ( "Account", back_populates = "client" )

    def __repr__ ( self ):
        return f"Client ( {self.id}, {self.name}, {self.address} )"
    def dict( self ):
        return {
            "id":self.id,
            "name":self.name,
            "address":self.address
        }


class HasSeatIn ( database.Model ):
    __tablename__ = "ImaSediste"

    client_id = database.Column ( "IdKom", database.ForeignKey ( Client.id ), primary_key = True )
    city_id   = database.Column ( "IdMes", database.ForeignKey ( City.id ) )

    # City<->HasSeatIn one-to-many
    city = database.relationship ( "City", back_populates = "has_seat_in_list" )

    # Client<->HasSeatIn one-to-one
    client = database.relationship ( "Client", back_populates = "has_seat_in" )

    def __repr__ ( self ):
        return f"HasSeatIn ( {self.client_id}, {self.city_id} )"

class Branch ( database.Model ):
    __tablename__ = "Filijala"

    id      = database.Column ( "IdFil", database.Integer, primary_key = True )
    name    = database.Column ( "Naziv", database.String ( 50 ) )
    address = database.Column ( "Adresa", database.String ( 50 ) )
    city_id = database.Column ( "IDMes", database.ForeignKey ( City.id ) )

    # City<->Branch one-to-many
    city = database.relationship ( "City", back_populates = "branches" )

    # Branch<->Account many-to-one
    accounts = database.relationship ( "Account", back_populates = "branch" )

    # Branch<->AccountItem many-to-one
    account_items = database.relationship ( "AccountItem", back_populates = "branch" )

    def __repr__ ( self ):
        return f"Branch ( {self.id}, {self.name}, {self.address}, {self.city_id} )"

class Account ( database.Model ):
    __tablename__ = "Racun"

    id                      = database.Column ( "IdRac", database.Integer, primary_key = True )
    status                  = database.Column ( "Status", database.String ( 1 ) )
    number_of_account_items = database.Column ( "BrojStavki", database.Integer )
    allowed_overdraft       = database.Column ( "DozvMinus", database.Integer )
    balance                 = database.Column ( "Stanje", database.Integer )
    branch_id               = database.Column ( "IdFil", database.ForeignKey ( Branch.id ) )
    client_id               = database.Column ( "IdKom", database.ForeignKey ( Client.id ) )

    # Branch<->Account many-to-on
    branch = database.relationship ( "Branch", back_populates = "accounts" )

    # Client<->Account many-to-one
    client = database.relationship ( "Client", back_populates = "accounts" )

    # Account<->AccountItem many-to-one
    account_items = database.relationship ( "AccountItem", back_populates = "account" )

    def __repr__ ( self ):
        return f"Account ( {self.id}, {self.status}, {self.number_of_account_items}, {self.allowed_overdraft}, {self.balance} )"
    def dict( self ):
        return {
            "id" : self.id,
            "status" : self.status,
            "number_of_account_items" : self.number_of_account_items,
            "allowed_overdraft" : self.allowed_overdraft,
            "balance" : self.balance,
            "Client" : self.client.dict()
        }
    
class AccountItem ( database.Model ):
    __tablename__ = "Stavka"

    id            = database.Column ( "IdSta", database.Integer, primary_key = True )
    serial_number = database.Column ( "RedBroj", database.Integer )
    date          = database.Column ( "Datum", database.Date )
    time          = database.Column ( "Vreme", database.Time )
    amount        = database.Column ( "Iznos", database.Integer )
    branch_id     = database.Column ( "IdFil", database.ForeignKey ( Branch.id ) )
    account_id    = database.Column ( "IdRac", database.ForeignKey ( Account.id ) )

    # Branch<->AccountItem many-to-one
    branch = database.relationship ( "Branch", back_populates = "account_items" )

    # Account<->AccountItem many-to-one
    account = database.relationship ( "Account", back_populates = "account_items" )

    # AccountItem<->Deposit one-to-one
    deposit = database.relationship ( "Deposit", back_populates = "account_item", uselist = False )

    # AccountItem<->Withdrawal one-to-one
    withdrawal = database.relationship ( "Withdrawal", back_populates = "account_item", uselist = False )

    def __repr__ ( self ):
        return f"AccountItem ( {self.id}, {self.serial_number}, {self.date}, {self.time}, {self.time} )"

class Deposit ( database.Model ):
    __tablename__ = "Uplata"

    account_item_id = database.Column ( "IdSta", database.ForeignKey ( AccountItem.id ), primary_key = True )
    basis           = database.Column ( "Osnov", database.String ( 10 ) )

    # AccountItem<->Deposit one-to-one
    account_item = database.relationship ( "AccountItem", back_populates = "deposit" )

    def __repr__ ( self ):
        return f"Deposit ( {self.account_item}, {self.basis} )"

class Withdrawal ( database.Model ):
    __tablename__ = "Isplata"

    account_item_id = database.Column ( "IdSta", database.ForeignKey ( AccountItem.id ), primary_key = True )
    commission      = database.Column ( "Provizija", database.Float )

    # AccountItem<->Withdrawal one-to-one
    account_item = database.relationship ( "AccountItem", back_populates = "withdrawal" )

    def __repr__ ( self ):
        return f"Withdrawal ( {self.account_item}, {self.commission} )"

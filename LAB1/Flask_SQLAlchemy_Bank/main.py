from sqlalchemy import and_, column, distinct, func, literal_column, null, select
from model import *
from flask import Flask, jsonify
from config import *

app = Flask( __name__ )
app.config.from_object(Configuration)
database.init_app( app )

#with app.app_context():
#    database.drop_all()
#    database.create_all()


@app.route("/", methods = ["GET"] )
def Hello_World():
    return "<h1>Hello World!</h1>",200

@app.route("/zadatak1", methods = ["GET"] )
def zadatak_1():
    clients = Client.query.all()
    return jsonify( [ client.dict() for client in clients ] )

@app.route( "/zadatak2", methods = ["GET"] )
def zadatak_2():
    racuni = Account.query.all()
    return jsonify( [ racun.dict() for racun in racuni ] )
    
@app.route("/zadatak3", methods = ["GET"] )
def zadatak_3():
    clients = database.session.query( Client.name ).all()
    retval = []
    for client in clients:
        retval.append( *client )
    return jsonify( retval )

@app.route("/zadatak4", methods = ["GET"] )
def zadatak_4():
    clients = database.session.query( Client.name, Client.address ).all()
    retval = []
    for client in clients:
        retval.append( {"adress" : client[1] , "name" : client[0] } )
    return jsonify( retval )

@app.route("/zadatak5", methods = ["GET"] )
def zadatak_5():
    clients = Client.query.order_by( Client.name ).all()
    return jsonify( [ client.dict() for client in clients ] )

@app.route("/zadatak9", methods = ["GET"] )
def zadatak_9():
    racuni = Account.query.where( Account.balance == -55000 ).all()
    return jsonify( [ racun.dict() for racun in racuni ] )

@app.route("/zadatak10", methods = ["GET"] )
def zadatak_10():
    racuni = Account.query.where( Account.balance > 0 ).all()
    return jsonify( [ racun.dict() for racun in racuni ] )

@app.route("/zadatak12", methods = ["GET"] )
def zadatak_12():
    racuni = Account.query.where( and_( Account.balance < -50000, Account.status == "B") ).all()
    return jsonify( [ racun.dict() for racun in racuni ] )

@app.route("/zadatak16", methods = ["GET"] )
def zadatak_16():
    racuni = database.session.query( Account.balance  ).add_columns( literal_column('3').label('Kamata')  ).add_columns( (Account.balance*-0.3).label('Sracunato') ).\
        where( Account.balance < 0 ).all()
    for racun in racuni:
        print( dict(racun._mapping) )
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak19", methods = ["GET"] )
def zadatak_19():
    stmt = select( Account.id.label("Id"), (Account.balance+Account.allowed_overdraft).label("Kolona1") ).\
           where( Account.balance > - Account.allowed_overdraft )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak20", methods = ["GET"] )
def zadatak_20():
    stmt = select( Client.name.distinct() )
    print( stmt )
    clients = database.session.execute(stmt).all()
    for client in clients:
        print( dict(client._mapping))
    return jsonify( [ dict(client._mapping) for client in clients ] )

@app.route("/zadatak21", methods = ["GET"] )
def zadatak_21():
    stmt = select( Account.id, Account.account_items, Account.balance ).\
           where( Account.balance == None )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak23", methods = ["GET"] )
def zadatak_23():
    stmt = select( func.sum( Account.balance ).label('Suma Stanja') )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak24", methods = ["GET"] )
def zadatak_24():
    stmt = select( func.min( Account.balance ).label('Minimum') ).where( Account.balance > 0 )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak26", methods = ["GET"] )
def zadatak_26():
    stmt = select( Account.balance.label('Stanje'), Client.name.label('Ime') )\
            .join( Account.client )
    print( stmt )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak27", methods = ["GET"] )
def zadatak_27():
    stmt = select( Branch.name.label('Naziv filijale'), AccountItem.amount, Account.id )\
            .join( AccountItem.branch ).join( AccountItem.account )
    print( stmt )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak29", methods = ["GET"] )
def zadatak_29():
    stmt = select( Branch.name.label('Naziv filijale'), AccountItem.amount.label('Iznos') )\
            .join(AccountItem.branch).join(AccountItem.deposit).where( Deposit.basis == "Uplata" )
    
    print( stmt.compile().params )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

@app.route("/zadatak32", methods = ["GET"] )
def zadatak_32():
    stmt = select( Client.name.label('ImeKomitenta'), func.sum( Account.balance ).label('Suma po racunima.'))\
            .join( Client.accounts ).group_by( Client.name, Client.id )
    
    print( stmt )
    racuni = database.session.execute(stmt).all()
    for racun in racuni:
        print( dict(racun._mapping))
    return jsonify( [ dict(racun._mapping) for racun in racuni ] )

if __name__ == '__main__':
    app.run( debug = True )
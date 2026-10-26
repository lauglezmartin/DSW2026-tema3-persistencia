from flask import Flask
from app.models import db, Producto
##importar base de datos, con el nombre de variable de la base de datos
#y el nombre de la tabla (clase)

app = Flask(__name__)
#para añadir formularios hay que añadir una contraseña
app.config["SECRET_KEY"] = "contraseña"

#configuracion de la base de datos (en local = sqlite)
#siempre es asi al usar sqlite, y despuesde las tres / se pone el nombre de la base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #si se modifican los datos
##que salga una noti si algo ta bien o no y otras advertencias

#vinculamos alchemy con nuestr aappp de flask
db.init_app(app)

with app.app_context():
    #crea las tablas en la base si no existieran
    db.create_all()
    print("<<<<<<<<<<<<<<<<<<")

    producto = Producto.query.first()
    print("Producto encontrado:", producto)

    if not Producto.query.first(): #si no hay un primer objeto, crea uno
        nuevo_producto = Producto(nombre="Teclado Mecanico RGB", precio=49.99)
        #y disponible esta por defecto true
        #ahora para añadirlo a la tabla
        print("prueba")
        db.session.add(nuevo_producto)
        db.session.commit()
        print(">>>> Producto de prueba insertadoe n la base de datos <<<<<")


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/test.db")
def test_db():
    productos = Producto.query.all()
    return f"Todos los productos: {productos}"


if __name__ == "__main__":
    app.run(debug=True)

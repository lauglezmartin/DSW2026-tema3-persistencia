import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, url_for
from app.models import db, Producto
from app.forms import ProductoForm  # Importamos el formulario para gestionar productos
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

# Configurar la carpeta destino para las imágenes
app.config["UPLOAD_FOLDER"]= os.path.join("app", "static", "img", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 # Limite de 2MB por seguridad

#vinculamos alchemy con nuestr aappp de flask
db.init_app(app)

with app.app_context():
    #crea las tablas en la base si no existieran
    db.create_all()
    print("<<<<<<<<<<<<<<<<<<")

    producto = Producto.query.first()
    print("Producto encontrado:", producto)

    # Si no hay ningún producto en la base de datos, creamos uno de prueba por defecto
    if not Producto.query.first(): #si no hay un primer objeto, crea uno
        nuevo_producto = Producto(
            nombre="Teclado Mecánico RGB", precio=49.99, disponible=True
        )
        #y disponible esta por defecto true
        #ahora para añadirlo a la tabla
        print("prueba")
        db.session.add(nuevo_producto)
        db.session.commit()
        print(">>>> Producto de prueba insertado en la base de datos <<<<<")


# Ruta raíz: Redirigimos directamente al catálogo principal en lugar de mostrar un "Hello, World!"
@app.route("/")
def home():
    # Redirigimos la raíz directamente al catálogo
    return redirect(url_for("mostrar_catalogo"))


# # Ruta de prueba opcional para ver los productos en formato texto plano
# @app.route("/test.db")
# def test_db():
#     productos = Producto.query.all()
#     return f"Todos los productos: {productos}"


# 1. READ: Mostrar todos los productos en la plantilla catalogo.html
@app.route("/catalogo")
def mostrar_catalogo():
    productos = Producto.query.all()
    return render_template("catalogo.html", lista_productos=productos)


# 2. CREATE: Mostrar formulario y guardar un nuevo producto en la BD
@app.route("/producto/nuevo", methods=["GET", "POST"])
def crear_producto():
    form = ProductoForm()
    # Llega con POST
    if form.validate_on_submit():
        #procesar el upload de la imagen si se ha subido una imagen porque el campo es opcional
        if form.imagen.data: # chequea si se ha subido una imagen
            archivo = form.imagen.data
            nombre_imagen = secure_filename(archivo.filename)

            #asegurar quela ruta existe 
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

            #guardar el fichero
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_imagen))
        
        nuevo_prod = Producto(
            nombre=form.nombre.data,
            precio=form.precio.data,
            disponible=form.disponible.data,
            imagen=nombre_imagen if form.imagen.data else None,
        )
        db.session.add(nuevo_prod)
        db.session.commit()
        # Patrón PRG: Redirigimos tras procesar el POST con éxito
        return redirect(url_for("mostrar_catalogo"))
    #Llega con GET
    return render_template("producto_form.html", form=form, titulo="Nuevo Producto")


# 3. UPDATE: Recuperar un producto existente, rellenar el formulario y guardar cambios
@app.route("/producto/<int:prod_id>/editar", methods=["GET", "POST"])
def editar_producto(prod_id):
    # Busca el producto por su clave primaria o lanza un error 404 si no existe
    producto = db.get_or_404(Producto, prod_id)

    # Al pasar obj=producto, en la petición GET los campos aparecen ya rellenos con los datos actuales
    form = ProductoForm(obj=producto)
    

    if form.validate_on_submit():
    # Procesar el upload de la imagen
        if form. imagen.data: # Chequea si se ha subido una imagen.
            archivo = form.imagen.data
            nombre_imagen = secure_filename (archivo.filename)

        # Asegurar que la ruta existe
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

            # Guardar el fichero
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_imagen))

        producto.nombre = form.nombre.data
        producto.precio = form.precio.data
        producto.disponible = form.disponible.data
        producto.imagen = nombre_imagen if form.imagen.data else form.imagen.data

        db.session.commit()
        return redirect(url_for("mostrar_catalogo"))

    return render_template("producto_form.html", form=form, titulo="Editar producto")



# 4. DELETE: Eliminar un producto de la BD (exclusivamente por POST)
@app.route("/producto/<int:prod_id>/eliminar", methods=["POST"])
# No usamos GET para eliminar, por seguridad y buenas prácticas, ya que si lo usaramos, 
# un simple enlace podría eliminar un producto sin confirmación.
def eliminar_producto(prod_id):
    producto = db.get_or_404(Producto, prod_id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("mostrar_catalogo"))


if __name__ == "__main__":
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

#CREAMOS UNA TABLA
class Producto(db.Model):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True) #con esto ya es auto incremen
    #en el mapped colum defines las restricciones

    nombre: Mapped[str] = mapped_column(db.String(100), nullable=False)
    #str es string, en las rest, se pone el limite de caracteres
    #y para que sea obligatorio ponemos nullable false

    precio: Mapped[float] = mapped_column(db.Float, nullable=False)

    #este es el equivalente boolenao
    disponible: Mapped[bool] = mapped_column(default = True)

    ##enlace a una imagen (en archivo, se pasa url) 
    # se pone none si no hay, o string(la url) si si hay
    imagen: Mapped[str | None] = mapped_column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Producto id={self.id}: {self.nombre} ({self.precio})"

    
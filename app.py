from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliente.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Producto
class Producto(db.Model):
    codigo_barras = db.Column(db.String(20), primary_key=True)
    nombre_producto = db.Column(db.String(255))
    categoria = db.Column(db.String(50))
    peso_promedio = db.Column(db.Float)
    material = db.Column(db.String(50))

# Modelo de Reciclaje
class Reciclaje(db.Model):
    id_reciclaje = db.Column(db.Integer, primary_key=True)
    codigo_barras = db.Column(db.String(20), db.ForeignKey('producto.codigo_barras'))
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

# Ruta principal
@app.route('/')
def index():
    return "Backend funcionando"

# Registrar código de barras
@app.route('/registrar_codigo', methods=['POST'])
def registrar_codigo():
    codigo = request.form.get('codigo_barras')
    if not codigo:
        return jsonify({"error": "Falta código"}), 400

    producto = Producto.query.get(codigo)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    nuevo_reciclaje = Reciclaje(codigo_barras=codigo)
    db.session.add(nuevo_reciclaje)
    db.session.commit()

    return jsonify({"mensaje": "Código registrado", "codigo": codigo})

# Ver todos los registros
@app.route('/ver_datos')
def ver_datos():
    registros = Reciclaje.query.all()
    resultado = [{"codigo": r.codigo_barras, "fecha": str(r.fecha)} for r in registros]
    return jsonify(resultado)

# Iniciar servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Insertar productos de prueba si no existen
        if not Producto.query.all():
            productos = [
                Producto(codigo_barras='7891000234567', nombre_producto='Agua Mineral 500ml',
                         categoria='Bebida', peso_promedio=25, material='Plástico PET'),
                Producto(codigo_barras='7891000345678', nombre_producto='Arroz 1kg',
                         categoria='Alimento', peso_promedio=15, material='Plástico HDPE'),
            ]
            db.session.bulk_save_objects(productos)
            db.session.commit()

    app.run(debug=True)
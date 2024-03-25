from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
swagger = Swagger(app)
 
# Modelo Empleados

class Empleados(db.Model):
    EmpleadoId = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    Clave = db.Column(db.String(100), nullable=True)

    def __init__(self, Nombre, Email, Clave):
        self.Nombre = Nombre
        self.Email = Email
        self.Clave = Clave

    def serialize(self):
        return {
            'EmpleadoId': self.EmpleadoId,
            'Nombre': self.Nombre,
            'Email': self.Email,
            'Clave': self.Clave
        }

# Modelo Tareas
class Tareas(db.Model):
    TareaId = db.Column(db.Integer, primary_key=True)
    EmpleadoId = db.Column(db.Integer, db.ForeignKey('empleados.EmpleadoId'), nullable=False)
    Descripcion = db.Column(db.String(100), nullable=True)
    Fecha = db.Column(db.String(10), nullable=True)
    Nombre = db.Column(db.String(100), nullable=True)
    Estado = db.Column(db.String(20), nullable=False)
    empleado = db.relationship('Empleados', backref=db.backref('tareas', lazy=True))

    def __init__(self, EmpleadoId, Descripcion, Fecha, Nombre, Estado):
        self.EmpleadoId = EmpleadoId
        self.Descripcion = Descripcion
        self.Fecha = Fecha
        self.Nombre = Nombre
        self.Estado = Estado

    def serialize(self):
        return {
            'TareaId': self.TareaId,
            'EmpleadoId': self.EmpleadoId,
            'Descripcion': self.Descripcion,
            'Fecha': self.Fecha,
            'Nombre': self.Nombre,
            'Estado': self.Estado
        }

# Rutas y controladores para Tareas
    

# Obtener todas las tareas
@app.route('/api/tareas', methods=['GET'])
def get_todas_las_tareas():
    todas_las_tareas = Tareas.query.all()
    return jsonify([tarea.serialize() for tarea in todas_las_tareas])

# Obtener una tarea por su ID
@app.route('/api/tareas/<int:id>', methods=['GET'])
def get_tarea_por_id(id):
    tarea = Tareas.query.get_or_404(id)
    return jsonify(tarea.serialize())

# Crear una nueva tarea
@app.route('/api/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()
    nueva_tarea = Tareas(**data)
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify(nueva_tarea.serialize()), 201

# Actualizar una tarea por su ID
@app.route('/api/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = Tareas.query.get_or_404(id)
    data = request.get_json()
    tarea.Descripcion = data['Descripcion']
    tarea.Fecha = data['Fecha']
    tarea.Nombre = data['Nombre']
    tarea.Estado = data['Estado']
    db.session.commit()
    return jsonify(tarea.serialize())

# Eliminar una tarea por su ID
@app.route('/api/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tarea = Tareas.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada correctamente'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

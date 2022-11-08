"""
- API Quiniela CCN 
- Version: 1.0
- Created for: WOL Media & Digital Division (soportedev@wol.group)
- License: Wol Media Copyrighted Software
- Author: Oscar E. Morales (oscarmoralesgt.com)

- Rights reserved, This program and code is issued for the purposes that the interested party deems appropriate.
"""

from datetime import datetime, timedelta
import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from functools import wraps
from jwt import encode, decode
from sqlalchemy.orm import Session

import pathlib

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()

host = "/quiniela"
app = Flask(__name__)
CORS(app)
url = "mysql+pymysql://vf"
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "QUINIELAWOL20222"


db = SQLAlchemy(app)
ma = Marshmallow(app)
base = db.Model.metadata.reflect(db.engine)

session = Session(db.engine, future=True)

""" 
Modelos y Esquemas
"""

# Modelo de Usuarios
class Usuarios(db.Model):
    __table__ = db.Model.metadata.tables["usuarios"]

    def __init__(
        self,
        usuario,
        nombre,
        apellido,
        cedula,
        correo,
        telefono,
        departamento,
        ip_adress,
        fecha_registro,
        token,
        ultimo_log,
        estado,
        correo_activo,
        id_seleccion,
    ):
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.correo = correo
        self.telefono = telefono
        self.departamento = departamento
        self.ip_adress = ip_adress
        self.fecha_registro = fecha_registro
        self.token = token
        self.ultimo_log = ultimo_log
        self.estado = estado
        self.correo_activo = correo_activo
        self.id_seleccion = id_seleccion

    def __repr__(self):
        return self.usuario


# Modelo de Selecciones
class Selecciones(db.Model):
    __table__ = db.Model.metadata.tables["selecciones"]

    def __init__(self, id, nombre, bandera, grupo, estado):
        self.id = id
        self.nombre = nombre
        self.bandera = bandera
        self.grupo = grupo
        self.estado = estado


class Partidos(db.Model):
    __table__ = db.Model.metadata.tables["partidos"]

    def __init__(
        self,
        id,
        id_equipo_a,
        id_equipo_b,
        goles_equipo_a,
        goles_equipo_b,
        id_equipo_ganador,
        fase,
        fecha,
        estado,
    ):
        self.id = id
        self.id_equipo_a = id_equipo_a
        self.id_equipo_b = id_equipo_b
        self.goles_equipo_a = goles_equipo_a
        self.goles_equipo_b = goles_equipo_b
        self.id_equipo_ganador = id_equipo_ganador
        self.fase = fase
        self.fecha = fecha
        self.estado = estado


# Modelo de Quiniela
class Quiniela(db.Model):
    __table__ = db.Model.metadata.tables["quiniela"]

    def __init__(
        self,
        id_usuario,
        id_partido,
        goles_equipo_a,
        goles_equipo_b,
        id_equipo_ganador,
        id_primer_gol,
        puntos,
        fecha_registro,
        estado,
    ):
        self.id_usuario = id_usuario
        self.id_partido = id_partido
        self.goles_equipo_a = goles_equipo_a
        self.goles_equipo_b = goles_equipo_b
        self.id_equipo_ganador = id_equipo_ganador
        self.id_primer_gol = id_primer_gol
        self.puntos = puntos
        self.fecha_registro = fecha_registro
        self.estado = estado

db.create_all()
db.session.commit()

# Esquema de Usuarios
class Usuarios_Schema(ma.Schema):
    class Meta:
        fields = (
            "usuario",
            "nombre",
            "apellido",
            "cedula",
            "correo",
            "telefono",
            "departamento",
            "ip_adress",
            "fecha_registro",
            "token",
            "ultimo_log",
            "estado",
            "correo_activo",
            "id_seleccion",
        )


usuario_schema = Usuarios_Schema()
usuarios_schema = Usuarios_Schema(many=True)

# Esquema de Equipos
class Equipos_Schema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "bandera", "grupo", "estado")


equipo_Schema = Equipos_Schema()
equipos_Schema = Equipos_Schema(many=True)


# Esquema de Partidos
class Partidos_Schema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "id_equipo_a",
            "id_equipo_b",
            "goles_equipo_a",
            "goles_equipo_b",
            "id_equipo_ganador",
            "fase",
            "fecha",
            "estado",
        )


partido_schema = Partidos_Schema()
partido_schemas = Partidos_Schema(many=True)


class Partidos_Fases(ma.Schema):
    class Meta:
        fields = (
            "id",
            "id_equipo_a",
            "id_equipo_b",
            "grupo",
            "fecha",
            "estado",
        )


partido_fases_schemas = Partidos_Fases(many=True)




# Esquema de Quiniela
class Quiniela_Schema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "id_usuario",
            "id_partido",
            "goles_equipo_a",
            "goles_equipo_b",
            "id_equipo_ganador",
            "id_primer_gol",
            "puntos",
            "fecha_registro",
            "estado",
        )


quiniela_schema = Quiniela_Schema()
quiniela_schemas = Quiniela_Schema(many=True)


""" 
Funciones del Token y JWT
"""

# Expirar token
def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


# Escribir Token
def write_token(data: dict):
    token = encode(
        payload={**data, "exp": expire_date(1)},
        key=app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return token


# Endpoint para verificar si un token esta activo y/o valido
@app.route(host + "/active/<token>", methods=["GET"])
def is_active(token):
    try:
        data = decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        current_user = Usuarios.query.filter_by(id=data["id"]).first()
        experation = datetime.fromtimestamp(data["exp"]).strftime("%Y-%m-%d %H:%M:%S")
        datos = {
            "id": current_user.id,
            "usuario": current_user.usuario,
            "nombre": current_user.nombre,
            "apellido": current_user.apellido,
            "correo": current_user.correo,
            "telefono": current_user.telefono,
            "estado": current_user.estado,
            "correo_activo": current_user.correo_activo,
            "active_session": True,
            "expiration": experation,
        }
        return datos
    except:
        return jsonify({"message": "Token no valido"}), 401


# decorator para verificar el JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return {"message": "Token no existente"}, 401
        try:
            data = decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = Usuarios.query.filter_by(id=data["id"]).first()
        except:
            return jsonify({"message": "El token no es valido!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def validar_creacion_usuario(usuario, cedula, telefono, correo):
    user = Usuarios.query.filter(
        (Usuarios.cedula == cedula)
        | (Usuarios.usuario == usuario)
        | (Usuarios.correo == correo)
    ).first()
    if user:
        return False  # El usuario ya existe, no pasa la validacion
    return True  # El usuario no existe, pasa la validacion


def validar_datos_quiniela(usuario, partido):
    user = Quiniela.query.filter(
        (Quiniela.id_usuario == usuario)
        &  (Quiniela.id_partido == partido)
    ).first()
    if user:
        return False  # El usuario ya registró este partido
    return True  # El usuario no ha registrado este partido en la quniiela



""" 
Funciones de Usuarios (Login, register)
"""


@app.route(host + "/ip", methods=["GET"])
def get_my_ip():
    return str(request.environ["REMOTE_ADDR"])


def validar_dato(dato, tipo):
    if tipo == "nombre":
        newdato = re.sub(r"[^A-Za-z-ÁáÉéÍíÓóÚú ]+", "", dato).upper()
    if tipo == "cedula":
        newdato = re.sub(r"[^A-Za-z-0-9]+", "", dato).upper()
    if tipo == "numerico":
        newdato = re.sub(r"     ", "", str(dato))
    return newdato


@app.route(host + "/register", methods=["POST"])
def nuevo_usuario():
    try:
        usuario = str(request.json["usuario"]).lower()
        nombre = str(validar_dato(request.json["nombre"], "nombre")).upper()
        apellido = str(validar_dato(request.json["apellido"], "nombre")).upper()
        cedula = validar_dato(request.json["cedula"], "cedula")
        correo = str(request.json["correo"]).lower()
        telefono = int(validar_dato(request.json["telefono"], "numerico"))
        departamento = request.json["departamento"]
        ip_adress = get_my_ip()
        fecha_registro = datetime.now()
        token = 0
        ultimo_log = fecha_registro
        estado = 1
        correo_activo = 0
        id_seleccion = int(validar_dato(request.json["id_seleccion"], "numerico"))

        if validar_creacion_usuario(usuario, cedula, telefono, correo):
            nuevo_usurio = Usuarios(
                usuario,
                nombre,
                apellido,
                cedula,
                correo,
                telefono,
                departamento,
                ip_adress,
                fecha_registro,
                token,
                ultimo_log,
                estado,
                correo_activo,
                id_seleccion,
            )

            db.session.add(nuevo_usurio)
            db.session.commit()

            data = {
                "id": nuevo_usurio.id,
                "usuario": usuario,
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "telefono": telefono,
                "estado": estado,
                "correo_activo": correo_activo,
            }
            token_final = str(write_token(data))
            response = jsonify({"token": token_final})
            response.status_code = 201
            return response
        else:
            response = jsonify(
                {"error": "El registro no pudo ser completado, usuario existente"}
            )
            response.status_code = 409
            return response
    except KeyError as e:
        response = jsonify(
            {
                "error": "El registro no pudo ser completado, hace falta el campo "
                + str(e)
            }
        )
        response.status_code = 400
        return response
    except:
        response = jsonify(
            {"error": "El registro no pudo ser completado, intenta nuevamente"}
        )
        response.status_code = 500
        return response


@app.route(host + "/login", methods=["POST"])
def login():
    cedula = request.json["cedula"]
    correo = request.json["correo"]
    user = Usuarios.query.filter_by(cedula=cedula, correo=correo).first()
    if user:
        data = {
            "id": user.id,
            "usuario": user.usuario,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "correo": user.correo,
            "telefono": user.telefono,
            "estado": user.estado,
            "correo_activo": user.correo_activo,
        }
        print(data)
        token_final = str(write_token(data))
        user.ultimo_log = datetime.now()
        user.token = token_final
        db.session.commit()
        return {"token": token_final}
    else:
        response = jsonify({"message": "El usuario no fue encontrado"})
        response.status_code = 404
        return response


# Activar correo electronico:
@app.route(host + "/activarcorreo", methods=["POST"])
def activar_correo_de_usuario():
    usuario = request.json["usuario"]
    correo = request.json["correo"]
    usrs = Usuarios.query.filter_by(usuario=usuario, correo=correo).first()
    if usrs:
        if usrs.correo_activo != 0:
            return (
                "El correo del usuario "
                + str(usuario)
                + " ya fue validado anteriormente",
                401,
            )
        usrs.correo_activo = 1
        db.session.commit()
        return (
            "El correo del usuario " + str(usuario) + " fue validado exitosamente",
            200,
        )
    return "El usuario no existe", 404


# Obtener listado de Usuarios:
@app.route(host + "/usuarios", methods=["GET"])
def get_usuarios():
    usrs = Usuarios.query.all()
    if usrs:
        return usuarios_schema.jsonify(usrs), 200
    return "No hay resultados", 404


# Obtener listado de equipos por id:
@app.route(host + "/equipos/<id_equipo>", methods=["GET"])
def get_equipo_por_id(id_equipo):
    equipo = Selecciones.query.filter(Selecciones.id == id_equipo).first()
    if equipo:
        return equipo_Schema.jsonify(equipo), 200
    return "No hay resultados", 404


# Obtener listado de equipos:
@app.route(host + "/equipos", methods=["GET"])
def get_equipos():
    equipos = Selecciones.query.all()
    if equipos:
        return equipos_Schema.jsonify(equipos), 200
    return "No hay resultados", 404


# Obtener listado de partidos:
@app.route(host + "/partidos", methods=["GET"])
def get_partidos():
    partidos = (
        Partidos.query.filter(Partidos.estado == 1)
        .filter(Selecciones.id == Partidos.id_equipo_a)
        .filter(Selecciones.estado == 1)
        .add_columns(
            Partidos.id_equipo_a,
            Partidos.id_equipo_b,
            Partidos.fecha,
            Partidos.estado,
            Partidos.id,
            Selecciones.grupo,
        )
    )
    if partidos:
        return partido_fases_schemas.jsonify(partidos), 200
    return "No hay resultados", 404


# Obtener listado de partidos por grupo:
@app.route(host + "/partidos/<grupo>", methods=["GET"])
def get_partidos_por_grupos(grupo):
    partidos = (
        Partidos.query.filter(Partidos.estado == 1)
        .filter(Selecciones.id == Partidos.id_equipo_a)
        .filter(Selecciones.grupo == grupo)
        .add_columns(
            Partidos.id_equipo_a,
            Partidos.id_equipo_b,
            Partidos.fecha,
            Partidos.estado,
            Partidos.id,
            Selecciones.grupo,
        )
        .all()
    )
    if partidos:
        return partido_fases_schemas.jsonify(partidos), 200
    return "No hay resultados", 404



# Obtener listado de quinielas:
@app.route(host + "/quiniela", methods=["GET"])
def get_quinielas():
    quinielas = Quiniela.query.all()
    if quinielas:
        return quiniela_schemas.jsonify(quinielas), 200
    return "No hay resultados", 404

# Obtener listado de quinielas por user ID:
@app.route(host + "/quiniela/<userid>", methods=["GET"])
def get_quinielas_por_id_user(userid):
    quinielas = Quiniela.query.filter(Quiniela.id_usuario == userid).all()
    if quinielas:
        return quiniela_schemas.jsonify(quinielas), 200
    return "No hay resultados", 404



@app.route(host + "/quiniela", methods=["POST"])
@token_required
def ingresar_quiniela(current_user):
    try:
        id_usuario = current_user.id
        id_partido = int(validar_dato(request.json["id_partido"], "numerico"))
        goles_equipo_a = int(validar_dato(request.json["goles_equipo_a"], "numerico"))
        goles_equipo_b = int(validar_dato(request.json["goles_equipo_b"], "numerico"))
        partido_ganador = Partidos.query.filter(Partidos.id == id_partido).first()
        id_primer_gol = int(validar_dato(request.json["id_primer_gol"], "numerico"))
        equipo_query = Partidos.query.filter(Partidos.id == id_partido).first()
        equipo_a = equipo_query.id_equipo_a
        equipo_b = equipo_query.id_equipo_b
        print(equipo_b == id_primer_gol)
        if id_primer_gol != equipo_a and id_primer_gol != equipo_b and id_primer_gol != 0:
            return jsonify({"error":  "El primer gol debe coindir con los equipos que estan jugando"}), 400
        if not partido_ganador:
            return jsonify({"error":  "El partido ingresado no existe"}), 404
        if goles_equipo_a > goles_equipo_b:
            id_equipo_ganador = equipo_a
        elif goles_equipo_a < goles_equipo_b:
            id_equipo_ganador = equipo_b
        else:
            id_equipo_ganador = None
            id_primer_gol = None
        puntos = 0
        fecha_registro = datetime.now()
        estado = 1

        if validar_datos_quiniela(id_usuario, id_partido):
            nueva_quiniela = Quiniela(id_usuario, id_partido,goles_equipo_a,goles_equipo_b,id_equipo_ganador,id_primer_gol,puntos,fecha_registro,estado)

            db.session.add(nueva_quiniela)
            db.session.commit()
            guide = Quiniela.query.filter(Quiniela.id == nueva_quiniela.id).first()
            return quiniela_schema.jsonify(guide), 200
        else:
            response = jsonify(
                {"error": "No se pudo registrar la quiniela, este usuario ya ingreso el partido"}
            )
            response.status_code = 409
            return response
    except KeyError as e:
        response = jsonify(
            {
                "error": "El registro de quiniela no pudo ser completado, hace falta el campo "
                + str(e)
            }
        )
        response.status_code = 400
        return response
    except:
        response = jsonify(
            {"error": "El registro no pudo ser completado, intenta nuevamente"}
        )
        response.status_code = 500
        return response


# Obtener listado de Usuarios:
@app.route("/", methods=["GET"])
def test_index():
    return "Api funcionando correctamente", 200


if __name__ == "__main__":
    app.run(debug=True, port=7000)

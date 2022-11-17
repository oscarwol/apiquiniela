# 🐍 Flask - Rest API Quiniela Frost


¡Importante!: Este proyecto ya se encuentra desplegado para sus pruebas, por lo que no es necesario que lo instales en tu equipo, puedes hacer las pruebas en el siguiente enlace:  https://quiniela-eight.vercel.app/quiniela/ por ejemplo https://quiniela-eight.vercel.app/quiniela/usuarios ,  para más información lee la documentación de 'Uso'

---
## 💻 Instalación

Recomiendo utilizar un entorno virtual (virtualenv) para ejecturar este proyecto y no tener problemas de dependencias.

Para ejecutar el proyecto, es necesario clonar el repositorio:

```
git clone https://github.com/oscarwol/apiquiniela/
cd apiquiniela
virtualenv -p python3 .
cd Scripts
activate
cd..
```

Despues, es necesario utilizar el gestor de paquetes de Python (PIP) [pip](https://pip.pypa.io/en/stable/) para instalar todas las dependencias y requerimientos necesarios para ejecutar el proyecto, estos se encuentran en el archivo "requirements.txt".

```
pip install -r requirements.txt
```

## 💾 Creando la Base de datos:
Para este proyecto se utilizo 'SQLAlchemy' un ORM desiñado para flask, por lo tanto; al ejecutar el proyecto todos los modelos serán migrados a la base de datos seleccionada.

No es necesario crear ninguna base de datos de manera manual, solo configurar la siguiente línea de código:

```
28. url = "mysql+pymysql://sql3506490:tb9TZcCU7W@sql3.freemysqlhosting.net/sql3506490"
```
Para configurar la base de datos, ver el ejemplo de arriba y seguir la nomenclatura de datos descrita a continuación:

Usuario: sql3506490
Contraseña: tb9TZcCU7W
Servidor: sql3.freemysqlhosting.net
Base de datos: sql3506490"


## 🚀 Iniciar el Proyecto
Una vez creado el entorno virtual, ejecutado e instaladas todas las dependencias y requerimientos, el proyecto puede ser ejecutado simplemente con la siguiente línea:
```
python app.py 
```


## ⚙️ Uso:
https://quiniela-eight.vercel.app/quiniela/
```
localhost:7000
```

| HTTP Type | Path | Used For |
| --- | --- | --- |
| `POST` | /login | Endpoint para autenticar y logear al usuario, una autenticación exitosa retornara un token|
| `POST` | /register | Nos permite registrar un nuevo usuario en el sistema, retorna un token |
| `GET` | /usuarios | Retorna la lista de usuarios registrados en el sistema (Esto será removido cuando terminen las pruebas) |
| `GET` | /equipos | Nos muestra el listado de todas las selecciones registradas en el sistema |
| `GET` | /equipos/EQUIPO_ID | Nos muestra los datos de un equipo con una ID específica |
| `GET` | /active/{TOKEN} | Nos muestra si un token específico esta activo o no y la información del mismo |
| `POST` | /enviarcorreo | Envía un correo que le permitirá al usuario activar su 'estado_correo = 1' (Se requiere de un token) |
| `POST` | /activarcorreo | Permite activar una cuenta con 'estado_correo = 0' (Manera Manual), solo usar en casos especiales |
| `GET` | /partidos | Nos muestra el listado de TODOS los partidos registrados dentro del sistema |
| `GET` | /partidos/GRUPO | Nos muestra el listado de partidos por grupo. Ej: /partidos/A : Grupo A. |
| `GET` | /quiniela | Nos muestra el listado de todas las quinielas registradas en el sistema |
| `GET` | /quiniela/usuario/USER_ID | Nos muestra el listado de todas las quinielas de un usuario en específico |
| `GET` | /quiniela/grupo/GRUPO | Nos muestra el listado de todas las quinielas de un grupo específico |
| `POST` | /quiniela | Permite crear una nueva quiniela (Se requiere de un token)|
| `POST` | /puntos | Obtiene el punteo y el porcentaje de avance de un usuario en específico (Se requiere de un token)|
| `POST` | /partidosusuario | Obtiene el listado de partidos por grupo y si un usuario específio ya los ingresó en la quiniela (Se requiere de un token)|

#### Endpoint Login [/login]
```http
  POST /login/
```

Ejemplos de datos a enviar:
```
{
    "correo": "oscar@gmail.com",
    "cedula": "123456789"
} 
```
---


### Endpoint Register: [/register]
```http
  POST /register/
```

Ejemplos de datos a enviar:
```
{
    "usuario": "ozk404",
    "nombre": "Oscar",
    "apellido": "Morales",
    "cedula": "123456789",
    "correo": "oscar@gmail.com",
    "telefono": "876543210",
    "departamento": "Guatemala",
    "id_seleccion": "1"
} 
```
---

#### Endpoint Enviar Correo de activación [/enviarcorreo]
```http
  POST /enviarcorreo
```

Ejemplos de datos a enviar:
```
{
    "token": "1202O0312O032103L1'21L3123",
}
```
---


#### Endpoint Activar Correo [/activarcorreo]
```http
  POST /activarcorreo
```

Ejemplos de datos a enviar:
```
{
    "token": "1202O0312O032103L1'21L3123",
}
```
---



### Endpoint 'Active' (Obtener el estado en tiempo real de un token): [/active/token]
Mediante la ejecución de un simple GET podemos obtener todos los datos correspondientes a un token, debe enviarse el token de la siguiente manera:
```http
  GET /active/TOKEN
```
---




### Endpoint Usuarios (Obtener Usuarios [/usuarios]
Mediante la ejecución de un simple GET podemos obtener todos los usuarios registrados en el sistema, no es necesario enviar ningun tipo de parametro.

```http
  GET /usuarios
```

---


### Endpoint Equipos (Obtener selecciones): [/equipos]
Mediante la ejecución de un simple GET podemos obtener todos las selecciones registradas, no es necesario enviar ningun tipo de parametro.
```http
  GET /equipos
```
---

### Endpoint Equipos por ID (Obtener seleccion por ID): [/equipos/Equipo_ID]
Mediante la ejecución de un simple GET podemos obtener todos las selecciones registradas.
```http
  GET /equipos/1
``` 
#### Obtendrá la información de la selección ID #1
---

### Endpoint Partidos (Obtener el listado total de partidos): [/partidos]
Mediante la ejecución de un simple GET podemos obtener todos los partidos registrados.
```http
  GET /partidos
```
---

### Endpoint Partidos por grupo (Obtener el listado total de partidos segun el grupo): [/partidos/GRUPO]
Mediante la ejecución de un simple GET podemos obtener todos los partidos registrados de un grupo específico.
```http
  GET /partidos/A
```
#### Obtendrá la información de todos los partidos correspondientes al grupo 'A'
---

### Endpoint Quiniela (Obtener todas las quinielas registradas): [/quiniela]
Mediante la ejecución de un simple GET podemos obtener todos las quinielas registradas en el sistema
```http
  GET /quiniela
```
---

### Endpoint Quiniela por ID de usuario (Obtener todas las quinielas de un usuario): [/quiniela/usuario/]
Mediante la ejecución de un simple GET podemos obtener todos las quinielas registradas en el sistema de un usuario específico
```http
  GET /quiniela/usuario/1
```
#### Obtendrá la información de todas las quinielas registradas por el usuario especificado
---

### Endpoint Quiniela por Grupo (Obtener todas las quinielas de un grupo): [/quiniela/grupo/]
Mediante la ejecución de un simple GET podemos obtener todos las quinielas registradas en el sistema de un usuario específico
```http
  GET /quiniela/grupo/A
```
#### Obtendrá la información de todas las quinielas registradas por el usuario especificado
---


### Endpoint Crear Quiniela: [/quiniela] (POST)
```http
  POST /quiniela
```
Es necesario enviar en el header el token en el campo 'x-access-token' Ejemplo:
```
  'x-access-token': ee4yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9w2342342342343
```

Ejemplos de datos a enviar:
```
{
    "id_partido": 1004,
    "goles_equipo_a": 1,
    "goles_equipo_b": 0,
    "id_primer_gol": 1
}   
```
---

### Endpoint 'Puntos' Obtiene el punteo total de un usuario [/puntos]

Ejemplos de datos a enviar:
```
{
  "token": "1234"
}   
```
---

### Endpoint 'Puntos' Obtiene el punteo total de un usuario [/puntos]

Ejemplos de datos a enviar:
```
{
  "token": "1234"
}   
```
---


### Endpoint 'partidosusuario' Retorna si un usuario ha completado todos los aprtidos de un grupo en específico [/partidosusuario]

Ejemplos de datos a enviar:
```
{
  "token": "1234",
  "grupo": "A"
}   
```
---

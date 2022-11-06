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

El sistema cuenta actualmente con 6 'end point' diferentes: 

| HTTP Type | Path | Used For |
| --- | --- | --- |
| `POST` | /login | Endpoint para autenticar y logear al usuario, una autenticación exitosa retornara un token|
| `POST` | /register | Nos permite registrar un nuevo usuario en el sistema, retorna un token |
| `GET` | /usuarios | Retorna la lista de usuarios registrados en el sistema (Esto será removido cuando terminen las pruebas) |
| `GET` | /equipos | Nos muestra el listado de todas las selecciones registradas en el sistema |
| `GET` | /active/{TOKEN} | Nos muestra si un token específico esta activo o no y la información del mismo |
| `POST` | /activarcorreo | Permite activar una cuenta con 'estado_correo = 0' |



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


#### Endpoint Activar Correo [/activarcorreo]
```http
  POST /activarcorreo/
```

Ejemplos de datos a enviar:
```
{
    "usuario": "ozk404",
    "correo": "ozk@gmail.com"
}
```
---



### Endpoint 'Active' (Obtener el estado en tiempo real de un token): [/active/token]
Mediante la ejecución de un simple GET podemos obtener todos los datos correspondientes a un token, debe enviarse el token de la siguiente manera:
```http
  GET /equipos/TOKEN
```
---


### Endpoint Equipos (Obtener selecciones): [/equipos]
Mediante la ejecución de un simple GET podemos obtener todos las selecciones registradas, no es necesario enviar ningun tipo de parametro.
```http
  GET /equipos
```
---

### Endpoint Usuarios (Obtener Usuarios [/usuarios]
Mediante la ejecución de un simple GET podemos obtener todos los usuarios registrados en el sistema, no es necesario enviar ningun tipo de parametro.

```http
  GET /usuarios
```

---


API_LOGIN_CONNECTION = "http://localhost:8080/users

def login(username, password):
    conexion = API_LOGIN_CONNECTION
    with conexion.cursor() as cursor:
        cursor.execute()
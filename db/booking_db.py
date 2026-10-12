from db.mysql_connector import conectare_mysql
import secrets
import string
import bcrypt


def create_user(username, password):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor()
    #1.Căutăm utilizatorul în baza de date după username
    query = "SELECT Id_user, password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    #2.Dacă utilizatorul există, oprim funcția
    if user:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Utilizator existent!"}

    #3.Criptam parola pentru user
    parola_simpla = password
    #Conversia parolei în bytes și generarea hash-ului
    parola_bytes = parola_simpla.encode('utf-8')
    salt = bcrypt.gensalt()
    parola_securizata = bcrypt.hashpw(parola_bytes, salt)

    # 4.Salvarea userului în baza de date
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    valori = (username, parola_securizata.decode('utf-8'))  # .decode() o transformă în string pentru MySQL
    cursor.execute(query, valori)
    conexiune.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexiune.close()
    return {"succes": True, "Id_user": user_id}


def verify_password(username_input, password_input):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    #1.Căutăm utilizatorul în baza de date după username
    query = "SELECT username, password FROM users WHERE username = %s"
    cursor.execute(query, (username_input,))
    user = cursor.fetchone()
    #2.Dacă utilizatorul nu există, oprim funcția
    if not user:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Utilizator inexistent!"}
    #3.Daca utilizatorul exista extragem datele găsite și verificăm parola criptată (bcrypt)
    parola_salvata_hash = user["password"]

    parola_valida = bcrypt.checkpw(
        password_input.encode("utf-8"), parola_salvata_hash.encode("utf-8")
    )
    if parola_valida:
        cursor.close()
        conexiune.close()
        return {"succes": True, "mesaj": "Parolă corecta!"}
    else:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Parolă incorecta!"}


def login_user(username_input,password_input):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    #1.Căutăm utilizatorul în baza de date după username
    query = "SELECT Id_user, password FROM users WHERE username = %s"
    cursor.execute(query, (username_input,))
    user = cursor.fetchone()

    #2.Dacă utilizatorul nu există, oprim funcția
    if not user:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Utilizator sau parolă incorectă!"}

    #3.Extragem datele găsite și verificăm parola criptată (bcrypt)
    user_id = user["Id_user"]
    parola_salvata_hash = user["password"]

    parola_valida = bcrypt.checkpw(
        password_input.encode("utf-8"), parola_salvata_hash.encode("utf-8")
    )

    #4.Dacă parola este greșită, oprim funcția
    if not parola_valida:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Parolă incorectă!"}

    #5.Daca parola este corectă generăm token-ul
    caractere_disponibile = string.digits + string.ascii_lowercase
    token_nou = "".join(secrets.choice(caractere_disponibile) for _ in range(15))

    #6.Inserăm sau suprascriem token-ul în tabelul tokens folosind user_id-ul extras la Pasul 3
    query_token = """
           INSERT INTO tokens (Id_user, token) 
           VALUES (%s, %s) 
           ON DUPLICATE KEY UPDATE token = VALUES(token)
       """

    try:
        cursor.execute(query_token, (user_id, token_nou))
        conexiune.commit()

        #Returnăm token-ul către API ca să-l trimită mai departe clientului (Frontend-ului)
        return {
            "succes": True,
            "mesaj": "Autentificare reușită!",
            "token": token_nou,
        }

    except Exception as e:
        print(f"Eroare la salvarea token-ului: {e}")
        return {"succes": False, "mesaj": "Eroare internă de server."}

    finally:
        cursor.close()
        conexiune.close()


def create_booking(username_input, password_input, firstname, lastname, totalprice,
                   depositpaid, date_checkin, date_checkout, additionalneeds):

    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)

    # 1.Căutăm utilizatorul în baza de date după username
    query = "SELECT Id_user, password FROM users WHERE username = %s"
    cursor.execute(query, (username_input,))
    user = cursor.fetchone()

    # 2.Dacă utilizatorul nu există, oprim funcția
    if not user:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Utilizator inexistent!"}

    # 3.Extragem datele găsite și verificăm parola criptată (bcrypt)
    user_id = user["Id_user"]
    parola_salvata_hash = user["password"]

    parola_valida = bcrypt.checkpw(
        password_input.encode("utf-8"), parola_salvata_hash.encode("utf-8")
    )

    # 4.Dacă parola este greșită, oprim funcția
    if not parola_valida:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Parolă incorectă!"}

    # 5. Daca parola este corecta verificam existenta tokenului asociat userului logat
    query = "SELECT u.username, t.token FROM tokens t INNER JOIN users u ON u.Id_user = t.Id_user WHERE u.username = %s"
    cursor.execute(query, (username_input,))
    token = cursor.fetchone()
    if not token:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Token inexistent!"}

    token_nou = token["token"]

    # 6. Introducerea datelor un tabela bookings
    query = ("INSERT INTO bookings (firstname, lastname, totalprice, depositpaid, date_checkin,"
             "date_checkout, additionalneeds, Id_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    try:
        cursor.execute(query, (firstname, lastname, totalprice, depositpaid, date_checkin,
                               date_checkout, additionalneeds, user_id))
        conexiune.commit()
        booking_id = cursor.lastrowid
        return {
            "succes": True,
            "mesaj": "O noua inregistrare a fost adaugata in tabelul bookings!",
            "Id_booking": booking_id
        }

    except Exception as e:
        print(f"Eroare la salvarea inregistrarii in tabelul bookings: {e}")
        return {"succes": False, "mesaj": "Eroare internă de server."}

    finally:
        cursor.close()
        conexiune.close()
        

def get_booking(username_input, password_input, Id_booking):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    result = login_user(username_input, password_input)
    if not result["succes"]:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": result["mesaj"]}
    query = "SELECT u.username, t.token FROM tokens t INNER JOIN users u ON u.Id_user = t.Id_user WHERE u.username = %s"
    cursor.execute(query, (username_input,))
    token = cursor.fetchone()
    if not token:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Token inexistent!"}
    token_salvat = token["token"]
    query1 = "SELECT b.* FROM bookings b INNER JOIN users u ON b.Id_user = u.Id_user INNER JOIN tokens t ON b.Id_user = t.Id_user WHERE b.Id_booking = %s AND t.token=%s"
    cursor.execute(query1, (Id_booking, token_salvat))
    booking = cursor.fetchone()
    if not booking:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Booking inexistent!"}
    cursor.close()
    conexiune.close()
    return {"succes": True, "mesaj": "Booking gasit!", "booking": booking}


def update_booking(username_input, password_input, Id_booking, firstname, lastname, totalprice,
                   depositpaid, date_checkin, date_checkout, additionalneeds):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    result = get_booking(username_input, password_input, Id_booking)
    if not result["succes"]:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": result["mesaj"]}
    query = ("UPDATE bookings SET firstname = %s, lastname= %s, totalprice= %s, depositpaid= %s, date_checkin= %s,"
            "date_checkout= %s, additionalneeds= %s WHERE Id_booking= %s")
    cursor.execute(query, (firstname, lastname, totalprice, depositpaid, date_checkin,
                           date_checkout, additionalneeds, Id_booking))
    conexiune.commit()
    update_booking = cursor.rowcount
    query1 = "SELECT b.* FROM bookings b INNER JOIN users u ON b.Id_user = u.Id_user WHERE b.Id_booking = %s"
    cursor.execute(query1, (Id_booking, ))
    booking = cursor.fetchone()
    if not booking:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Update-ul nu s-a realizat!"}
    cursor.close()
    conexiune.close()
    return {"succes": True, "mesaj": "Booking update OK!", "booking": booking}


def delete_booking(username_input, password_input, Id_booking):
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    result = get_booking(username_input, password_input, Id_booking)
    if not result["succes"]:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": result["mesaj"]}
    query = ("DELETE FROM bookings WHERE Id_booking = %s")
    cursor.execute(query, (Id_booking, ))
    conexiune.commit()
    deleted_booking = cursor.rowcount
    if not deleted_booking:
        cursor.close()
        conexiune.close()
        return {"succes": False, "mesaj": "Booking not deleted!"}
    cursor.close()
    conexiune.close()
    return {"succes": True, "mesaj": "Booking deleted!"}

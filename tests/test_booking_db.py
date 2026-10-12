from datetime import date
from db.mysql_connector import conectare_mysql
from db.booking_db import (create_user, verify_password, login_user, create_booking, get_booking,
    update_booking, delete_booking)


def test_create_user():
    # Test creere user existent in baza de date
    result = create_user("admin", "password123")

    assert result["succes"] is False
    assert result["mesaj"] == "Utilizator existent!"

    # Test creere user nouin baza de date
    result = create_user("test_user_nou", "parola1234")
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    query = "SELECT Id_user FROM users WHERE username = %s"
    cursor.execute(query, ("test_user_nou",))
    Id_user = cursor.fetchone()

    assert result["succes"] is True
    assert result["Id_user"] == Id_user["Id_user"]


def test_verify_password():
    # Test verificare parola corecta
    result = verify_password("admin", "password123")
    assert result["succes"] is True
    assert result["mesaj"] == "Parolă corecta!"

    #Test verificare parola gresita
    result = verify_password("admin", "parola12")
    assert result["succes"] is False
    assert result["mesaj"] == "Parolă incorecta!"


def test_login_user():
    # Test login user si parola corecta - generare token
    result = login_user("admin", "password123")
    assert result["mesaj"] == "Autentificare reușită!"
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    query = "SELECT u.username, t.token FROM tokens t INNER JOIN users u ON u.Id_user = t.Id_user WHERE u.username = %s"
    cursor.execute(query, ("admin",))
    token = cursor.fetchone()
    token_vechi = result["token"]
    assert result["token"] == token["token"]
    cursor.close()
    conexiune.close()

    # Test login cu parola incorecta - tokenul nu se genereaza
    result = login_user("admin", "parola1234")
    assert result["mesaj"] == "Parolă incorectă!"

    # Test login user si parola corecta - update token
    result = login_user("admin", "password123")
    assert result["mesaj"] == "Autentificare reușită!"
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    query = "SELECT u.username, t.token FROM tokens t INNER JOIN users u ON u.Id_user = t.Id_user WHERE u.username = %s"
    cursor.execute(query, ("admin",))
    token = cursor.fetchone()
    assert result["token"] == token["token"]
    assert result["token"] != token_vechi
    cursor.close()
    conexiune.close()


def test_create_booking():
    result = create_booking("admin", "password123", "Jim", "Brown", 111, True, "2018-01-01", "2019-01-01", "Breakfast")
    assert result["mesaj"] == "O noua inregistrare a fost adaugata in tabelul bookings!"
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    query = "SELECT * FROM bookings b INNER JOIN users u ON b.Id_user = u.Id_user WHERE u.username = %s AND b.Id_booking = %s"
    cursor.execute(query, ("admin", result["Id_booking"]))
    booking = cursor.fetchone()
    assert result["Id_booking"] == booking["Id_booking"]
    assert "Jim" == booking["firstname"]
    assert "Brown" == booking["lastname"]
    assert 111 == booking["totalprice"]
    assert True == booking["depositpaid"]
    assert date(2018, 1, 1) == booking["Date_checkin"]
    assert date(2019, 1, 1) == booking["Date_checkout"]
    assert "Breakfast" == booking["additionalneeds"]
    query = "SELECT u.Id_user FROM users u INNER JOIN bookings b ON u.Id_user = b.Id_user WHERE u.username = %s AND b.Id_booking = %s"
    cursor.execute(query, ("admin", result["Id_booking"]))
    user = cursor.fetchone()
    assert booking["Id_user"] == user["Id_user"]
    cursor.close()
    conexiune.close()


def test_get_booking():
    result = get_booking("admin", "password123", 1)
    assert result["succes"] is True
    assert result["booking"]["Id_booking"] == 1
    assert result["booking"]["firstname"] == "Jim"
    assert result["booking"]["lastname"] == "Brown"
    assert result["booking"]["totalprice"] == 111
    assert result["booking"]["depositpaid"] == 1
    assert result["booking"]["Date_checkin"] == date(2018, 1, 1)
    assert result["booking"]["Date_checkout"] == date(2019, 1, 1)
    assert result["booking"]["additionalneeds"] == "Breakfast"
     assert result["booking"]["Id_user"] == user["Id_user"]


def test_update_booking():
    result = update_booking("admin", "password123", 1, "Paul", "Allan", 113, False,
                            "2018-01-05", "2019-01-06", "Dinner")
    assert result["succes"] is True
    assert result["booking"]["Id_booking"] == 1
    assert result["booking"]["firstname"] == "Paul"
    assert result["booking"]["lastname"] == "Allan"
    assert result["booking"]["totalprice"] == 113
    assert result["booking"]["depositpaid"] == 0
    assert result["booking"]["Date_checkin"] == date(2018, 1, 5)
    assert result["booking"]["Date_checkout"] == date(2019, 1, 6)
    assert result["booking"]["additionalneeds"] == "Dinner"
     assert result["booking"]["Id_user"] == user["Id_user"]


def test_delete_booking():
    result = delete_booking("admin", "password123", 1)
    conexiune = conectare_mysql()
    cursor = conexiune.cursor(dictionary=True)
    query = "SELECT * FROM bookings WHERE Id_booking = %s"
    cursor.execute(query, (1,))
    booking = cursor.fetchone()
    assert result["succes"] is True
    assert booking is None
    cursor.close()
    conexiune.close()

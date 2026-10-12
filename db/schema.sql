-- Restful Booker - Python & MySQL Database Testing
-- Database schema
--
-- This script creates the booker database and its three tables.
-- It defines the schema only; it does not insert test or application data.

CREATE DATABASE IF NOT EXISTS booker;

USE booker;

CREATE TABLE IF NOT EXISTS users (
    Id_user INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    PRIMARY KEY (Id_user)
);

CREATE TABLE IF NOT EXISTS tokens (
    Id_user INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    PRIMARY KEY (Id_user),
    CONSTRAINT fk_tokens_users
        FOREIGN KEY (Id_user)
        REFERENCES users (Id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS bookings (
    Id_booking INT NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    totalprice INT,
    depositpaid TINYINT(1) DEFAULT 1,
    Date_checkin DATE,
    Date_checkout DATE,
    additionalneeds VARCHAR(255),
    Id_user INT NOT NULL,
    PRIMARY KEY (Id_booking),
    CONSTRAINT fk_bookings_users
        FOREIGN KEY (Id_user)
        REFERENCES users (Id_user)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

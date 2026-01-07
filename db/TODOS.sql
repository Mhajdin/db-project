CREATE TABLE mitglied (
    mitglied_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE,
    adresse VARCHAR(250),
    email VARCHAR(150),
    telefon VARCHAR(30),
    beitrittsdatum DATE,
    status VARCHAR(50), 
    notizen TEXT
);
CREATE TABLE abo (
    abo_id INT AUTO_INCREMENT PRIMARY KEY,
    mitglied_id INT NOT NULL,
    typ VARCHAR(100) NOT NULL,
    startdatum DATE NOT NULL,
    enddatum DATE,
    preis FLOAT,
    status VARCHAR(50),
    FOREIGN KEY (mitglied_id) REFERENCES mitglied(mitglied_id)
);
CREATE TABLE kurs (
    kurs_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    beschreibung VARCHAR(250),
    wochentag VARCHAR(30),
    startzeit TIME,
    dauer INT,
    raum VARCHAR(50),
    trainer VARCHAR(100),
    max_plaetze INT
);
CREATE TABLE trainingsplan (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    mitglied_id INT NOT NULL,
    titel VARCHAR(100) NOT NULL,
    startdatum DATE,
    erstellt_am DATE,
    FOREIGN KEY (mitglied_id) REFERENCES mitglied(mitglied_id)
);
CREATE TABLE uebung (
    uebung_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    satz INT,
    wiederholungen INT,
    gewicht FLOAT,
    FOREIGN KEY (plan_id) REFERENCES trainingsplan(plan_id)
);
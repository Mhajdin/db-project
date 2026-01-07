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

-- Insert sample data
-- Beachten Sie, dass die Primary Keys automatisch generiert werden
INSERT INTO mitglied (vorname, nachname, geburtsdatum, adresse, email, telefon, beitrittsdatum, status) VALUES
('Maxi', 'Künstel', '2007-03-12', 'Altersstrasse 1, 8000 Zürich', 'maxi@künstel.com', '0791111111', '2024-09-01', 'aktiv'),
('Noah', 'Schmid', '2006-11-28', 'Beispielweg 2, 8400 Winterthur', 'noah.schmid@example.ch', '0782223344', '2023-01-15', 'aktiv'),
('Sara', 'Keller', '2005-06-05', 'Hauptstrasse 10, 8050 Zürich', 'sara.keller@example.ch', '0773334455', '2022-05-20', 'inaktiv');
 
INSERT INTO abo (mitglied_id, typ, startdatum, enddatum, preis, status) VALUES
(1, 'Monatsabo', '2024-09-01', '2024-09-30', 59.90, 'abgelaufen'),
(1, 'Jahresabo', '2024-10-01', '2025-09-30', 599.00, 'aktiv'),
(2, 'Monatsabo', '2024-12-01', '2024-12-31', 59.90, 'aktiv');

INSERT INTO kurs (name, beschreibung, wochentag, startzeit, dauer, raum, trainer, max_plaetze) VALUES
('Yoga Flow', 'Mobilität und Balance', 'Montag', '18:00:00', 60, 'Studio 1', 'S. Frank', 20),
('HIIT', 'Intervalltraining mit hoher Intensität', 'Mittwoch', '19:00:00', 45, 'Studio 2', 'L. Frei', 18),
('Spinning', 'Cardio auf dem Bike', 'Freitag', '17:30:00', 50, 'Cycling Room', 'S. Baumann', 16);

INSERT INTO trainingsplan (mitglied_id, titel, startdatum, erstellt_am) VALUES
(1, 'Ganzkörper – Einsteiger', '2024-09-05', '2024-09-05'),
(2, 'Muskelaufbau – Oberkörper', '2024-11-10', '2024-11-10'),
(2, 'Muskelaufbau – Unterkörper', '2024-11-10', '2024-11-10');

INSERT INTO uebung (plan_id, name, satz, wiederholungen, gewicht) VALUES
(1, 'Kniebeuge', 3, 12, 20.0),
(1, 'Liegestütze', 3, 10, 0.0),
(2, 'Bankdrücken', 4, 8, 40.0);
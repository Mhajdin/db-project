CREATE TABLE mitglied (
    mitglied_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE,
    adresse VARCHAR(250),
    email VARCHAR(150),
    telefon VARCHAR(50),
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
    wochentag VARCHAR(40),
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
('Anna', 'Schmid', '2005-07-09', 'Seestrasse 12, 8700 Küsnacht', 'anna.schmid@example.ch', '0783334444', '2022-08-15', 'aktiv'),
('Jonas', 'Müller', '2004-11-22', 'Dorfweg 8, 8600 Dübendorf', 'jonas.mueller@example.ch', '0775556666', '2021-05-10', 'inaktiv'),
('Lea', 'Keller', '2007-01-30', 'Parkstrasse 20, 8050 Zürich', 'lea.keller2@example.ch', '0761112233', '2024-01-05', 'aktiv'),
('Tim', 'Weber', '2003-09-17', 'Industriestrasse 3, 8304 Wallisellen', 'tim.weber@example.ch', '0794445555', '2020-09-01', 'aktiv'),
('Sara', 'Fischer', '2006-06-06', 'Sonnenweg 14, 8400 Winterthur', 'sara.fischer@example.ch', '0786667777', '2023-02-20', 'aktiv'),
('Jan', 'Brunner', '2005-04-11', 'Wiesenstrasse 6, 9000 St. Gallen', 'jan.brunner@example.ch', '0778889999', '2022-11-01', 'aktiv'),
('Nina', 'Huber', '2004-12-03', 'Kirchweg 9, 6003 Luzern', 'nina.huber@example.ch', '0762223333', '2021-07-15', 'inaktiv'),
('Leon', 'Baumann', '2006-08-21', 'Bergstrasse 4, 5000 Aarau', 'leon.baumann@example.ch', '0799998888', '2023-04-01', 'aktiv'),
('Laura', 'Gerber', '2005-10-10', 'Feldweg 2, 4102 Binningen', 'laura.gerber@example.ch', '0781231234', '2022-06-10', 'aktiv'),

('David', 'Steiner', '2003-03-05', 'Hofstrasse 11, 3005 Bern', 'david.steiner@example.ch', '0773214321', '2020-01-20', 'aktiv'),
('Julia', 'Moser', '2006-05-18', 'Schulweg 7, 9500 Wil', 'julia.moser@example.ch', '0764545454', '2023-09-01', 'aktiv'),
('Elias', 'Arnold', '2004-07-27', 'Poststrasse 19, 8200 Schaffhausen', 'elias.arnold@example.ch', '0795656565', '2021-02-14', 'aktiv'),
('Mia', 'Schneider', '2007-02-02', 'Lindenweg 3, 5600 Lenzburg', 'mia.schneider@example.ch', '0786767676', '2024-02-01', 'aktiv'),
('Fabian', 'Zimmermann', '2005-12-19', 'Birkenstrasse 10, 3600 Thun', 'fabian.zimmermann@example.ch', '0777878787', '2022-10-01', 'aktiv'),
('Lena', 'Graf', '2006-09-01', 'Rosenweg 15, 8852 Altendorf', 'lena.graf@example.ch', '0768989898', '2023-05-15', 'aktiv'),
('Simon', 'Roth', '2004-01-25', 'Alpenstrasse 1, 6300 Zug', 'simon.roth@example.ch', '0799090909', '2021-03-01', 'inaktiv'),
('Alina', 'Suter', '2005-11-07', 'Neudorfstrasse 8, 5430 Wettingen', 'alina.suter@example.ch', '0781010101', '2022-12-01', 'aktiv'),
('Marco', 'Vogel', '2003-06-16', 'Talstrasse 22, 7000 Chur', 'marco.vogel@example.ch', '0771212121', '2020-06-01', 'aktiv'),
('Emma', 'Bieri', '2007-04-29', 'Obere Gasse 5, 5400 Baden', 'emma.bieri@example.ch', '0762323232', '2024-03-01', 'aktiv'),

('Kevin', 'Lutz', '2004-08-08', 'Unterdorf 9, 8610 Uster', 'kevin.lutz@example.ch', '0793434343', '2021-08-01', 'aktiv'),
('Melanie', 'Wyss', '2006-03-14', 'Hintere Gasse 4, 3432 Lützelflüh', 'melanie.wyss@example.ch', '0784545454', '2023-01-10', 'aktiv'),
('Patrick', 'Hauser', '2005-05-23', 'Aareweg 6, 5070 Frick', 'patrick.hauser@example.ch', '0775656565', '2022-04-01', 'aktiv'),
('Chiara', 'Gloor', '2007-07-07', 'Schlossweg 12, 5210 Windisch', 'chiara.gloor@example.ch', '0766767676', '2024-04-01', 'aktiv'),
('Daniel', 'Frei', '2003-10-30', 'Rainweg 18, 8048 Zürich', 'daniel.frei@example.ch', '0797878787', '2020-11-01', 'aktiv'),
('Vanessa', 'Bühler', '2005-02-12', 'Fabrikstrasse 7, 8604 Volketswil', 'vanessa.buehler@example.ch', '0788989898', '2022-02-01', 'aktiv'),
('Adrian', 'Ammann', '2004-09-19', 'Schützenstrasse 2, 4800 Zofingen', 'adrian.ammann@example.ch', '0779090909', '2021-09-01', 'aktiv'),
('Jasmin', 'Ott', '2006-12-05', 'Mühlestrasse 13, 8606 Greifensee', 'jasmin.ott@example.ch', '0760101010', '2023-10-01', 'aktiv'),
('Florian', 'Rüegg', '2005-01-17', 'Weiherweg 4, 8730 Uznach', 'florian.rueegg@example.ch', '0791212121', '2022-01-15', 'aktiv'),
('Selina', 'Ulrich', '2007-06-21', 'Haldenweg 9, 8125 Zollikerberg', 'selina.ulrich@example.ch', '0782323232', '2024-05-01', 'aktiv');

INSERT INTO abo (mitglied_id, typ, startdatum, enddatum, preis, status) VALUES
(1, 'Monatsabo', '2024-09-01', '2024-09-30', 59.90, 'abgelaufen'),
(1, 'Jahresabo', '2024-10-01', '2025-09-30', 599.00, 'aktiv'),
(2, 'Monatsabo', '2024-12-01', '2024-12-31', 59.90, 'aktiv');
(4, 'Monatsabo', '2024-10-01', '2024-10-31', 59.90, 'abgelaufen'),
(5, 'Jahresabo', '2024-01-01', '2024-12-31', 599.00, 'abgelaufen'),
(6, 'Monatsabo', '2025-01-01', '2025-01-31', 59.90, 'aktiv'),
(7, 'Jahresabo', '2024-03-01', '2025-02-28', 599.00, 'aktiv'),
(8, 'Monatsabo', '2025-02-01', '2025-02-28', 59.90, 'aktiv'),
(9, 'Jahresabo', '2024-04-01', '2025-03-31', 599.00, 'aktiv'),
(10, 'Monatsabo', '2025-01-15', '2025-02-14', 59.90, 'aktiv'),
(11, 'Jahresabo', '2024-09-01', '2025-08-31', 599.00, 'aktiv'),
(12, 'Monatsabo', '2025-02-10', '2025-03-09', 59.90, 'aktiv'),
(13, 'Jahresabo', '2024-11-01', '2025-10-31', 599.00, 'aktiv'),
(14, 'Monatsabo', '2025-01-01', '2025-01-31', 59.90, 'aktiv'),
(15, 'Jahresabo', '2024-06-01', '2025-05-31', 599.00, 'aktiv'),
(16, 'Monatsabo', '2025-03-01', '2025-03-31', 59.90, 'aktiv'),
(17, 'Jahresabo', '2024-02-01', '2025-01-31', 599.00, 'aktiv'),
(18, 'Monatsabo', '2025-02-01', '2025-02-28', 59.90, 'aktiv'),
(19, 'Jahresabo', '2024-07-01', '2025-06-30', 599.00, 'aktiv'),
(20, 'Monatsabo', '2025-01-01', '2025-01-31', 59.90, 'aktiv'),
(21, 'Jahresabo', '2024-05-01', '2025-04-30', 599.00, 'aktiv'),
(22, 'Monatsabo', '2025-02-01', '2025-02-28', 59.90, 'aktiv'),
(23, 'Jahresabo', '2024-08-01', '2025-07-31', 599.00, 'aktiv'),
(24, 'Monatsabo', '2025-01-01', '2025-01-31', 59.90, 'aktiv'),
(25, 'Jahresabo', '2024-09-01', '2025-08-31', 599.00, 'aktiv'),
(26, 'Monatsabo', '2025-02-01', '2025-02-28', 59.90, 'aktiv'),
(27, 'Jahresabo', '2024-10-01', '2025-09-30', 599.00, 'aktiv'),
(28, 'Monatsabo', '2025-03-01', '2025-03-31', 59.90, 'aktiv'),
(29, 'Jahresabo', '2024-11-01', '2025-10-31', 599.00, 'aktiv'),
(30, 'Monatsabo', '2025-01-01', '2025-01-31', 59.90, 'aktiv'),
(31, 'Jahresabo', '2024-12-01', '2025-11-30', 599.00, 'aktiv'),
(32, 'Monatsabo', '2025-02-01', '2025-02-28', 59.90, 'aktiv'),

INSERT INTO kurs (name, beschreibung, wochentag, startzeit, dauer, raum, trainer, max_plaetze) VALUES
('Yoga Flow', 'Mobilität und Balance', 'Montag', '18:00:00', 60, 'Studio 1', 'S. Frank', 20),
('HIIT', 'Intervalltraining mit hoher Intensität', 'Mittwoch', '19:00:00', 45, 'Studio 2', 'L. Frei', 18),
('Spinning', 'Cardio auf dem Bike', 'Freitag', '17:30:00', 50, 'Cycling Room', 'S. Baumann', 16);
('Spinning', 'Cardio auf dem Bike', 'Freitag', '17:30:00', 50, 'Cycling Room', 'S. Baumann', 16),
('Functional Training', 'Ganzkörper Eigengewicht', 'Dienstag', '18:30:00', 55, 'Studio 3', 'M. Keller', 15),
('Core & Balance', 'Rumpfstabilität', 'Donnerstag', '17:00:00', 45, 'Studio 1', 'A. Meier', 20);

INSERT INTO trainingsplan (mitglied_id, titel, startdatum, erstellt_am) VALUES
(1, 'Ganzkörper – Einsteiger', '2024-09-05', '2024-09-05'),
(2, 'Muskelaufbau – Oberkörper', '2024-11-10', '2024-11-10'),
(2, 'Muskelaufbau – Unterkörper', '2024-11-10', '2024-11-10');
(4, 'Ganzkörper Anfänger', '2024-10-05', '2024-10-05'),
(5, 'Muskelaufbau Oberkörper', '2024-09-10', '2024-09-10'),
(6, 'Cardio Ausdauer', '2025-01-02', '2025-01-02'),
(7, 'Krafttraining Fortgeschritten', '2024-11-01', '2024-11-01'),
(8, 'Functional Training', '2025-02-05', '2025-02-05'),
(9, 'Reha Mobilität', '2024-12-01', '2024-12-01'),
(10, 'Hypertrophie', '2025-01-18', '2025-01-18'),
(11, 'HIIT Programm', '2024-10-20', '2024-10-20'),
(12, 'Ganzkörper Intensiv', '2025-02-12', '2025-02-12'),
(13, 'Einsteiger Fitness', '2024-11-15', '2024-11-15'),
(14, 'Muskelaufbau Unterkörper', '2025-01-08', '2025-01-08'),
(15, 'Core Training', '2024-08-01', '2024-08-01'),
(16, 'Cardio Anfänger', '2025-03-03', '2025-03-03'),
(17, 'Kraft & Stabilität', '2024-09-05', '2024-09-05'),
(18, 'Functional Basic', '2025-02-06', '2025-02-06'),
(19, 'Ausdauer Lauftraining', '2024-10-10', '2024-10-10'),
(20, 'Ganzkörper Senior', '2025-01-04', '2025-01-04'),
(21, 'Bodyweight Training', '2024-07-12', '2024-07-12'),
(22, 'Mobilisation & Stretch', '2025-02-03', '2025-02-03'),
(23, 'Hypertrophie Advanced', '2024-08-20', '2024-08-20'),
(24, 'Krafttraining Basis', '2025-01-07', '2025-01-07'),
(25, 'Cardio & Core', '2024-09-22', '2024-09-22'),
(26, 'Ganzkörper Workout', '2025-02-10', '2025-02-10'),
(27, 'Strength Training', '2024-10-30', '2024-10-30'),
(28, 'HIIT & Cardio', '2025-03-05', '2025-03-05'),
(29, 'Reha Rücken', '2024-11-05', '2024-11-05'),
(30, 'Einsteiger Training', '2025-01-02', '2025-01-02'),
(31, 'Muskeldefinition', '2024-12-10', '2024-12-10'),
(32, 'Core & Balance', '2025-02-08', '2025-02-08'),
INSERT INTO uebung (plan_id, name, satz, wiederholungen, gewicht) VALUES
(1, 'Kniebeuge', 3, 12, 20.0),
(1, 'Liegestütze', 3, 10, 0.0),
(2, 'Bankdrücken', 4, 8, 40.0); 
(4, 'Kniebeuge', 3, 12, 20),
(4, 'Liegestütze', 3, 10, 0),
(5, 'Bankdrücken', 4, 8, 40),
(5, 'Schulterdrücken', 3, 10, 25),
(6, 'Laufband', 1, 1, 0),
(6, 'Crosstrainer', 1, 1, 0),
(7, 'Kreuzheben', 4, 6, 60),
(7, 'Klimmzüge', 3, 6, 0),
(8, 'Burpees', 3, 15, 0),
(8, 'Kettlebell Swing', 3, 20, 16),
(9, 'Dehnen Rücken', 1, 1, 0),
(9, 'Mobilisation Hüfte', 1, 1, 0),
(10, 'Bizepscurls', 3, 12, 12),
(10, 'Latziehen', 3, 10, 40),
(11, 'Jump Squats', 3, 20, 0),
(11, 'Mountain Climbers', 3, 30, 0),
(12, 'Ausfallschritte', 3, 16, 0),
(12, 'Plank', 3, 1, 0),
(13, 'Step Ups', 3, 12, 0),
(13, 'Crunches', 3, 20, 0);


CREATE SCHEMA IF NOT EXISTS sport_data;

USE sport_data;

# # # # # # # # # # # # # # # # # # #
# relazione ATLETA
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS `athlete` (
  `id_no` int NOT NULL, #cartellino
  `name` varchar(15) NOT NULL,
  `surname` varchar(15) NOT NULL,
  `telephone_no` int DEFAULT NULL,
  `email` varchar(30) NOT NULL,
  `category` varchar(15),
  `height` int NOT NULL,
  `weight` int NOT NULL,
  `position` varchar(20) DEFAULT NULL, #ruolo
  `adress` varchar(20) DEFAULT NULL,
  `injured` boolean DEFAULT false NOT NULL,
  PRIMARY KEY (`id_no`),
  CONSTRAINT `atleta_chk_1` CHECK (((`category` = _utf8mb4'U8') or (`category` = _utf8mb4'U10') or (`category` = _utf8mb4'U12') or (`category` = _utf8mb4'U14') or (`category` = _utf8mb4'U16') or (`category` = _utf8mb4'U18') or (`category` = _utf8mb4'Seniores')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# # # # # # # # # # # # # # # # # # #
# relazione CERTIFICATO MEDICO
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS medical_cert (
    id_no INT UNIQUE,
    date_of_emission DATE,
    PRIMARY KEY (id_no , date_of_emission),
    FOREIGN KEY (id_no)
        REFERENCES athlete (id_no)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione TEST
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS physical_test (
    id_no INT,
    jump FLOAT,
    sprint FLOAT,
    endurance FLOAT,
    CONSTRAINT PRIMARY KEY (id_no),
    FOREIGN KEY (id_no)
        REFERENCES athlete (id_no)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione ALLENATORE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS `coach` (
  `id_no` int NOT NULL, #cartellino
  `name` varchar(15) NOT NULL,
  `surname` varchar(15) NOT NULL,
  `telephone_no` int DEFAULT NULL,
  `email` varchar(30) NOT NULL,
  `category` varchar(15),
  PRIMARY KEY (`id_no`),
  CONSTRAINT `coach_chk_1` CHECK (((`category` = _utf8mb4'U8') or (`category` = _utf8mb4'U10') or (`category` = _utf8mb4'U12') or (`category` = _utf8mb4'U14') or (`category` = _utf8mb4'U16') or (`category` = _utf8mb4'U18') or (`category` = _utf8mb4'Seniores')))
);

# # # # # # # # # # # # # # # # # # #
# relazione CONTRATTO
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS contract (
    protocol_no INT AUTO_INCREMENT,
    starting_date DATE,
    expiry_date DATE,
    salary FLOAT,
    PRIMARY KEY (protocol_no)
);

# # # # # # # # # # # # # # # # # # #
# relazione ACCOMPAGNATORE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS `companion` (
    `id_no` INT NOT NULL,
    `name` VARCHAR(15) NOT NULL,
    `surname` VARCHAR(15) NOT NULL,
    `telephone_no` INT DEFAULT NULL,
    `email` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`id_no`)
);

# # # # # # # # # # # # # # # # # # #
# relazione VOLONTARIO
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS `volunteer` (
    `cf` VARCHAR(16),
    `name` VARCHAR(15) NOT NULL,
    `surname` VARCHAR(15) NOT NULL,
    `telephone_no` INT DEFAULT NULL,
    `email` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`cf`)
);

# # # # # # # # # # # # # # # # # # #
# relazione EVENTO
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS sport_event (
    event_date DATE,
    event_time TIME,
    kind VARCHAR(15),
    place VARCHAR(30),
    attendance INT,
    PRIMARY KEY (event_date , event_time , kind , place),
    CONSTRAINT CHECK (kind = 'partita' OR kind = 'sociale'
        OR kind = 'allenamento')
);

# # # # # # # # # # # # # # # # # # #
# relazione SOCIETA
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS club (
    id_no INT,
    club_name VARCHAR(20) NOT NULL,
    foundation_year INT NOT NULL,
    capital FLOAT,
    PRIMARY KEY (id_no)
);

# # # # # # # # # # # # # # # # # # #
# relazione AZIENDA
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS company (
    p_iva INT,
    company_name VARCHAR(20),
    telephone_no INT,
    email VARCHAR(30),
    PRIMARY KEY (p_iva)
);

# # # # # # # # # # # # # # # # # # #
# relazione PARTECIPAZIONE ATLETA
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS athlete_attendance (
    athlete INT,
    event_date DATE,
    event_time TIME,
    kind VARCHAR(15),
    place VARCHAR(30),
    PRIMARY KEY (athlete , event_date , event_time , kind , place),
    FOREIGN KEY (athlete)
        REFERENCES athlete (id_no)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_date , event_time , kind , place)
        REFERENCES sport_event (event_date , event_time , kind , place)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione PARTECIPAZIONE ACCOMPAGNATORE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS companion_attendance (
    companion INT,
    event_date DATE,
    event_time TIME,
    kind VARCHAR(15),
    place VARCHAR(30),
    PRIMARY KEY (companion , event_date , event_time , kind , place),
    FOREIGN KEY (companion)
        REFERENCES companion (id_no)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_date , event_time , kind , place)
        REFERENCES sport_event (event_date , event_time , kind , place)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione PARTECIPAZIONE VOLONATRIO
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS volunteer_attendance (
    volunteer VARCHAR(16),
    event_date DATE,
    event_time TIME,
    kind VARCHAR(15),
    place VARCHAR(30),
    PRIMARY KEY (volunteer , event_date , event_time , kind , place),
    FOREIGN KEY (volunteer)
        REFERENCES volunteer (cf)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_date , event_time , kind , place)
        REFERENCES sport_event (event_date , event_time , kind , place)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione PAGAMENTO SPONSOR
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS sponsor_payment (
    club INT,
    company INT,
    payment_date DATE,
    payment_time TIME,
    total FLOAT NOT NULL,
    PRIMARY KEY (club , company , payment_date , payment_time),
    FOREIGN KEY (club)
        REFERENCES club (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (company)
        REFERENCES company (p_iva)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione PAGAMENTO SPONSOR
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS athlete_payment (
    club INT,
    athlete INT,
    payment_date DATE,
    payment_time TIME,
    total FLOAT NOT NULL,
    PRIMARY KEY (club , athlete , payment_date , payment_time),
    FOREIGN KEY (club)
        REFERENCES club (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (athlete)
        REFERENCES athlete (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione PAGAMENTO SPONSOR
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS coach_payment (
    club INT,
    coach INT,
    payment_date DATE,
    payment_time TIME,
    total FLOAT NOT NULL,
    PRIMARY KEY (club , coach , payment_date , payment_time),
    FOREIGN KEY (club)
        REFERENCES club (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (coach)
        REFERENCES coach (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione SPONSORIZZAZIONE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS sponsorship (
    club INT,
    company INT,
    start_date DATE,
    end_date DATE,
    sponsor_value FLOAT,
    PRIMARY KEY (club , company , start_date),
    FOREIGN KEY (club)
        REFERENCES club (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (company)
        REFERENCES company (p_iva)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    CHECK (end_date > start_date)
);

# # # # # # # # # # # # # # # # # # #
# relazione STIPULAZIONE GIOCATORE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS stipulate_athlete (
    athlete INT,
    contract INT,
    PRIMARY KEY (athlete , contract),
    FOREIGN KEY (athlete)
        REFERENCES athlete (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (contract)
        REFERENCES contract (protocol_no)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# relazione STIPULAZIONE ALLENATORE
# # # # # # # # # # # # # # # # # # #

CREATE TABLE IF NOT EXISTS stipulate_coach (
    coach INT,
    contract INT,
    PRIMARY KEY (coach , contract),
    FOREIGN KEY (coach)
        REFERENCES coach (id_no)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (contract)
        REFERENCES contract (protocol_no)
        ON DELETE NO ACTION ON UPDATE CASCADE
);

# # # # # # # # # # # # # # # # # # #
# vista degli atleti infortunati
# # # # # # # # # # # # # # # # # # #

CREATE VIEW injured_athletes (id_no , name , surname , category , injured) AS
    SELECT 
        id_no, name, surname, category, injured
    FROM
        athlete
    WHERE
        (injured = TRUE);

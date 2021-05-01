


CREATE TABLE IF NOT EXISTS Artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NULL,
    age INTEGER NULL,
    CHECK(age>0)
);

CREATE TABLE IF NOT EXISTS Impressarios (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NULL,
    age INTEGER NULL,
    CHECK(age>0)
);

CREATE TABLE IF NOT EXISTS Artist_impressario (
    artist_id INT REFERENCES Artists(id) ON DELETE CASCADE,
    impressarios_id INT REFERENCES Impressarios(id)
);

CREATE TABLE IF NOT EXISTS Event_types (
    id serial PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Organizers (
    id serial PRIMARY KEY,
    name VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS infrastructure_types (
    id serial PRIMARY KEY,
    name VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS Specific_place (
    id serial PRIMARY KEY,
    type_id INT REFERENCES infrastructure_types(id),
    name VARCHAR(100),
    number_of_seats INT NOT NULL,
    open_air BOOLEAN DEFAULT 'no',
    free BOOLEAN DEFAULT 'no',
    address VARCHAR(100) NULL,
    internet_address VARCHAR(150) NULL
);


DROP TABLE Specific_event;

CREATE TABLE IF NOT EXISTS Specific_event (
    id serial PRIMARY KEY,
    type_id INT REFERENCES Event_types(id) ON DELETE CASCADE,
    place_id INT REFERENCES Specific_place(id) ON DELETE CASCADE,
    name VARCHAR(100),
    date TIMESTAMP,
    organizer_id INT REFERENCES Organizers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Genres (
    id serial PRIMARY KEY,
    name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Artist_genre (
    artist_id INT REFERENCES Artists(id) ON DELETE CASCADE,
    genre_id INT REFERENCES Genres(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS concurs_participants(
    id_concursor INT REFERENCES specific_event(id),
    id_participant INT REFERENCES artists(id),
    place INT NOT NULL
);

ALTER TABLE concurs_participants ADD CONSTRAINT unique_participant UNIQUE (id_concursor, id_participant, place)
ALTER TABLE concurs_participants ADD CONSTRAINT unique_concurs_place UNIQUE (id_concursor, place)

ALTER TABLE Impressarios ADD COLUMN genre_id INT REFERENCES Genres(id);

ALTER TABLE artist_genre ADD CONSTRAINT unique_record UNIQUE (artist_id, genre_id);
ALTER TABLE specific_place ADD CONSTRAINT unique_place_record UNIQUE (type_id, name);
ALTER TABLE artists ADD CONSTRAINT unique_artist_record UNIQUE (name);
ALTER TABLE impressarios ADD CONSTRAINT unique_impressario_record UNIQUE (name);
ALTER TABLE organizers ADD CONSTRAINT unique_organizator_record UNIQUE (name);


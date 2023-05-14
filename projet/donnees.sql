CREATE TABLE utilisateur
(
  utilisateur_id INTEGER PRIMARY KEY NOT NULL,
  courriel VARCHAR(200) NOT NULL,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  mdp VARCHAR(100) NOT NULL
);

CREATE TABLE tag
(
  tag_id INTEGER NOT NULL PRIMARY KEY,
  nom VARCHAR(100) NOT NULL
);

CREATE TABLE projet
(
  projet_id INTEGER PRIMARY KEY NOT NULL,
  nom VARCHAR(100) NOT NULL,
  description VARCHAR(100000) NOT NULL,
  tag_1 INTEGER,
  tag_2 INTEGER,
  tag_3 INTEGER,
  tag_4 INTEGER,
  tag_5 INTEGER,
  createur_id INTEGER NOT NULL,
  date_de_debut DATE NOT NULL,
  statut INTEGER NOT NULL,
  note_id INTEGER,
  FOREIGN KEY (note_id) REFERENCES note(note_id),
  FOREIGN KEY (tag_1) REFERENCES tag(tag_id), 
  FOREIGN KEY (tag_2) REFERENCES tag(tag_id),
  FOREIGN KEY (tag_3) REFERENCES tag(tag_id),
  FOREIGN KEY (tag_4) REFERENCES tag(tag_id),
  FOREIGN KEY (tag_5) REFERENCES tag(tag_id),  
  FOREIGN KEY (createur_id) REFERENCES utilisateur(utilisateur_id)
);

CREATE TABLE vote
(
  vote_id INTEGER NOT NULL PRIMARY KEY,
  projet_id INTEGER NOT NULL,
  votant_id INTEGER NOT NULL,
  commentaire VARCHAR(10000) NOT NULL,
  note_id INTEGER,
  FOREIGN KEY (note_id) REFERENCES note(note_id),
  FOREIGN KEY (projet_id) REFERENCES projet(projet_id),
  FOREIGN KEY (votant_id) REFERENCES utilisateur(utilisateur_id)
);

CREATE TABLE note
(
  note_id INTEGER NOT NULL PRIMARY KEY,
  valeur REAL NOT NULL
);

INSERT INTO utilisateur VALUES (1, 'aurelien.troncy@telecomnancy.eu', 'troncy', 'aurélien', 'admin');
INSERT INTO utilisateur VALUES (2, 'tanguy.bourra@telecomnancy.eu', 'bourra', 'tanguy', 'admin');
INSERT INTO utilisateur VALUES (3, 'thibault.boisseau@telecomnancy.eu', 'boisseau', 'thibault', 'admin');
INSERT INTO utilisateur VALUES (4, 'guillaume.bourgeon@telecomnancy.eu', 'bourgeon', 'guillaume', 'admin');
INSERT INTO utilisateur VALUES (5, 'telecomnancy@telecomnancy.eu', 'nancy', 'telecom', 'admin');
INSERT INTO utilisateur VALUES (6, 'mairie@gouv.fr', 'mairie', 'mairie', 'admin');

INSERT INTO tag VALUES (1, 'Mairie');
INSERT INTO tag VALUES (2, 'Citoyen');
INSERT INTO tag VALUES (3, 'Ecologie');
INSERT INTO tag VALUES (4, 'Sociale');
INSERT INTO tag VALUES (5, 'Informatique');
INSERT INTO tag VALUES (6, 'Voirie');
INSERT INTO tag VALUES (7, 'Associatif');
INSERT INTO tag VALUES (8, 'Caricatif');
INSERT INTO tag VALUES (9, 'Long terme');
INSERT INTO tag VALUES (10, 'Court terme');
INSERT INTO tag VALUES (11, 'Sport');
INSERT INTO tag VALUES (12, 'Cuisine');

INSERT INTO note VALUES (1, -8);

INSERT INTO projet VALUES (1, 'PPII', 'Porjet à rendre pour la rentrée', 1, 2, 5, 9, NULL, 5, "2021-12-26", 0, 801);



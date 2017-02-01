-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
    player_id serial PRIMARY KEY,
    player_name varchar(20)
);

CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    p1_id integer REFERENCES players,
    p2_id integer REFERENCES players,
    win_id integer REFERENCES players
);

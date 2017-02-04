-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

DROP TABLE players;
CREATE TABLE players (
    player_id serial PRIMARY KEY,
    player_name varchar(20)
);

DROP TABLE matches;
CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    lose_id integer REFERENCES players,
    win_id integer REFERENCES players
);

CREATE VIEW wins AS
    SELECT
    count(match_id) as ct,
    win_id
    FROM matches
    GROUP BY win_id;

CREATE VIEW loses AS
    SELECT
    count(match_id) as ct,
    lose_id
    FROM matches
    GROUP BY lose_id;

CREATE VIEW standing AS
    SELECT
    player_id id,
    player_name pname,
    COALESCE(wins.ct,0) wins,
    COALESCE(wins.ct,0)+COALESCE(loses.ct,0) as matches
    FROM players p
    LEFT JOIN loses
        ON p.player_id = loses.lose_id
    LEFT JOIN wins
        ON p.player_id = wins.win_id
    ORDER BY wins;








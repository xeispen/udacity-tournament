#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
# Other modules used to run a web server.
import time
import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    return DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    return DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    ct = c.fetchone()
    return ct[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    clean = bleach.clean(name)
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (player_name) VALUES (%s)", (clean,))
    DB.commit()
    return DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT
                p.player_id id,
                p.player_name pname,
                COALESCE(wins.ct,0) wins,
                COALESCE(mp1.ct,0)+COALESCE(mp2.ct,0) as matches
                FROM players p
                LEFT JOIN (
                    SELECT
                    count(match_id) as ct,
                    win_id
                    FROM matches
                    GROUP BY win_id) wins
                    ON p.player_id = wins.win_id
                LEFT JOIN (
                    SELECT
                    count(match_id) as ct,
                    p1_id
                    FROM matches
                    GROUP BY p1_id) mp1
                    ON p.player_id = mp1.p1_id
                LEFT JOIN (
                    SELECT
                    count(match_id) as ct,
                    p2_id
                    FROM matches
                    GROUP BY p2_id) mp2
                    ON p.player_id = mp2.p2_id
                ORDER BY wins;""")

    standings = c.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (p1_id, p2_id, win_id) VALUES (%s,%s,%s)", (winner, loser, winner,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pair_list = []
    standings = playerStandings()
    pairs = len(standings)
    i = 0
    while i < pairs:
        pair_list.append((standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1]))
        i += 2
    return pair_list

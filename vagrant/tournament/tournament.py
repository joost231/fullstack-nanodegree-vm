#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) AS num FROM players")
    result = c.fetchone()
    db.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT into players (name) values(%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()

    # Execute query which selects the players and their win record,
    # sorted by wins
    c.execute("""SELECT id, name, wins, SUM(wins+lost) AS matches FROM """
              """(SELECT p.id, p.name, COUNT(w.winner) AS wins, """
              """COUNT(l.loser) AS lost FROM players p """
              """LEFT JOIN matches w ON p.id = w.winner """
              """LEFT JOIN matches l ON p.id = l.loser """
              """GROUP BY p.id) AS matches """
              """GROUP BY id, name, wins ORDER BY wins DESC""")
    playerStandings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
                       for row in c.fetchall()
                       ]
    db.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT into matches (winner, loser) values(%s,%s)",
              (winner, loser))
    db.commit()
    db.close()


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

    # Get current playerstandings
    standings = playerStandings()

    # Initialize empty array
    SwissPairList = []

    # Create array foreach player with player-data
    players = [item[0:2] for item in standings]
    player_count = len(players)

    index = 0

    # Create array with player-pairs
    while (index < player_count):
        member = players[index] + players[index+1]
        SwissPairList.append(member)
        index = index + 2

    return SwissPairList

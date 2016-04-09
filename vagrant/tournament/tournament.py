#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Can't connect to the database.")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("SELECT count(*) AS num FROM players")
    result = cursor.fetchone()
    db.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("INSERT into players (name) values(%s)", (name,))
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
    db, cursor = connect()

    # Execute query which selects the players and their win record,
    # sorted by wins
    cursor.execute("""SELECT id, name, wins, SUM(wins+lost) AS matches FROM """
                   """player_results AS matches GROUP BY id, name, wins """
                   """ORDER BY wins DESC""")
    playerStandings = [(int(row[0]), str(row[1]), int(row[2]), int(row[3]))
                       for row in cursor.fetchall()
                       ]
    db.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    cursor.execute("INSERT into matches (winner, loser) values(%s,%s)",
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

    # Count players
    number_of_players = len(standings)

    # Check if the number of players is even
    if number_of_players % 2 != 0:
        print("Number of players is not even.")
        return false

    # Initialize empty array
    SwissPairList = []

    # Create array foreach player with player-data
    players = [item[0:2] for item in standings]

    index = 0

    # Create array with player-pairs
    while (index < number_of_players):
        member = players[index] + players[index+1]
        SwissPairList.append(member)
        index = index + 2

    return SwissPairList

-- Table definitions for the tournament project.

-- Drop database if exist
DROP DATABASE IF EXISTS tournament;

-- Create database
CREATE DATABASE tournament;

-- Connect to the database
\c tournament;

-- Create table for registering the players
CREATE TABLE players (
	id		serial PRIMARY KEY, 
	name 	text NOT NULL
);

-- Create table for registering the match-results
CREATE TABLE matches (
	id		serial PRIMARY KEY, 
	winner  integer REFERENCES players (id) ON DELETE CASCADE,
	loser	integer REFERENCES players (id) ON DELETE CASCADE,
    CHECK (winner <> loser)
);

-- Create view for fetching player results
CREATE VIEW player_results 
AS 
  	SELECT p.id, 
    	p.NAME, 
    	Count(w.winner) AS wins, 
    	Count(l.loser)  AS lost 
  	FROM players p 
    	LEFT JOIN matches w 
    		ON p.id = w.winner 
    	LEFT JOIN matches l 
        	ON p.id = l.loser 
	GROUP BY p.id
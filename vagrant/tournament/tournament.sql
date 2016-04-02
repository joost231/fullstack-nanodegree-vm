-- Table definitions for the tournament project.

-- Drop database if exist
DROP DATABASE IF EXISTS tournament;

-- Create database
CREATE DATABASE tournament;

-- Connect to the database
\c tournament;

-- Create table for registering the players
create table players (
	id		serial PRIMARY KEY, 
	name 	text 
);

-- Create table for registering the match-results
create table matches (
	id		serial PRIMARY KEY, 
	winner  integer REFERENCES players (id),
	loser	integer REFERENCES players (id)
);
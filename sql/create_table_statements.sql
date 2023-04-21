CREATE DATABASE IF NOT EXISTS nba_app;
USE nba_app;

CREATE TABLE IF NOT EXISTS user_table
(	username VARCHAR(20) PRIMARY KEY,
	first_name CHAR(20) NOT NULL,
    last_name CHAR(20) NOT NULL,
    password varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS season_table
(	seas_id int PRIMARY KEY,
	season int
);

CREATE TABLE IF NOT EXISTS team_table 
(	abbreviation CHAR(3) PRIMARY KEY,
	team text
);

CREATE TABLE IF NOT EXISTS player_table
(	player_id int primary key, 
	player text, 
    birth_year text, 
    hof text, 
    num_seasons int,
    first_seas int,
    last_seas int
);

CREATE TABLE IF NOT EXISTS player_stats 
(	seas_id int, 
	player_id int, 
	tm char(3), 
	pos	text, 
	age	int, 
	experience int,	
    g int, 
	mp	int,
	mp_per_game	double,
	fg	int, 
	fg_per_game	double,
    fga	int, 
    fga_per_game double,	
    fg_percent double,
    x3p	int,
    x3p_per_game double,
	x3pa int,
	x3pa_per_game double,
	x3p_percent	text,
    x2p	int,
    x2p_per_game double,
	x2pa int,
	x2pa_per_game double,
	x2p_percent	double, 
    e_fg_percent double,
	ft	int,
    ft_per_game double,
	fta int,
	fta_per_game double,
	ft_percent text,
	orb int,
	orb_per_game double,
	drb int,
	drb_per_game double,
	trb int,
	trb_per_game double,
	ast int,
	ast_per_game double,
	stl	int, 
    stl_per_game double,
	blk int, 
	blk_per_game double,
	tov int,
	tov_per_game double,
	pf	int, 
    pf_per_game double,
	pts int,
	pts_per_game double,
    PRIMARY KEY (player_id, seas_id, tm),
    FOREIGN KEY (player_id) REFERENCES player_table(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (seas_id) REFERENCES season_table(seas_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (tm) REFERENCES team_table(abbreviation) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS all_star_selections
(	player_id INT,
	seas_id	INT,
	team text, 
    PRIMARY KEY (player_id, seas_id),
    FOREIGN KEY (player_id) REFERENCES player_table(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (seas_id) REFERENCES season_table(seas_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS end_of_season_teams
(	type text,
	player_id int,
    seas_id int,
    PRIMARY KEY (player_id, seas_id),
    FOREIGN KEY (player_id) REFERENCES player_table(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (seas_id) REFERENCES season_table(seas_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS player_season_info
(	player_id int,
    seas_id int,
    team char(3),
    pos text,
    age int,
    experience int, 
    PRIMARY KEY (player_id, seas_id, team),
    FOREIGN KEY (player_id) REFERENCES player_table(player_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (seas_id) REFERENCES season_table(seas_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (team) REFERENCES team_table(abbreviation) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fantasy_teams
(username VARCHAR(20),
 team_name VARCHAR(20),
 players int,
 PRIMARY KEY (username, team_name),
 FOREIGN KEY (username) REFERENCES user_table(username) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (players) REFERENCES player_table(player_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE fantasy_players (
  username varchar(20) NOT NULL,
  team_name varchar(20) NOT NULL,
  players_id int NOT NULL,
  PRIMARY KEY (username, team_name, players_id),
  FOREIGN KEY(username, team_name) REFERENCES fantasy_teams (username, team_name) ON DELETE CASCADE ON UPDATE CASCADE
)
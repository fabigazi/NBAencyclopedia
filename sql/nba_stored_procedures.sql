CREATE DATABASE IF NOT EXISTS nba_app;
USE nba_app;

CREATE TABLE IF NOT EXISTS user_table
(	username VARCHAR(20) PRIMARY KEY,
	first_name CHAR(20) NOT NULL,
    last_name CHAR(20) NOT NULL,
    password varchar(20) NOT NULL
);


/* Procedure to create new user */
drop procedure if EXISTS create_username;
delimiter $$
create procedure create_username(username varchar(50), first_name char(50), last_name char(50), password varchar(50))

begin 
  
  INSERT INTO user_table VALUES (username, first_name, last_name, password);
    
end $$
delimiter ;

-- call create_username('test', 'test', 'test', 'test');

/* Function to check if user account exists 
	CURRENTLY NOT USING THIS IN CODE - KEEPING IN CASE WE DECIDE TO IMPLEMENT IT*/
drop FUNCTION if EXISTS check_user;
DELIMITER $$
CREATE FUNCTION check_user (username VARCHAR(20))
	RETURNS BOOL
    DETERMINISTIC READS SQL DATA
    BEGIN
		IF EXISTS (SELECT * FROM user_table WHERE username = username)
			THEN RETURN TRUE;
		ELSE
			RETURN FALSE;
		END IF;
    END$$
DELIMITER ;

-- player_search

drop procedure if EXISTS player_search;
DELIMITER ;;
CREATE PROCEDURE player_search (player_in varchar(50), season_in int, pos_in char(50), team_in varchar(50))
BEGIN
IF (season_in = 0 ) THEN
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	ORDER BY player, season;
ELSE
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	where
		season = season_in
	ORDER BY player, season;
END IF; 
end ;;
DELIMITER ;

drop procedure if EXISTS generic_player_search;
DELIMITER ;;
CREATE PROCEDURE generic_player_search ()
BEGIN
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	ORDER BY player, season;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year;
DELIMITER ;;
CREATE PROCEDURE player_search_year (season_in int)
BEGIN
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	where
		season = season_in
	ORDER BY player, season;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_pos;
DELIMITER ;;
CREATE PROCEDURE player_search_pos (pos_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	where
		pos = pos_in
	ORDER BY player;
end ;;
DELIMITER ;

CALL player_search_pos('PG');

drop procedure if EXISTS player_search_name;
DELIMITER ;;
CREATE PROCEDURE player_search_name (name_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	where
		player = name_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_team;
DELIMITER ;;
CREATE PROCEDURE player_search_team (team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	where
		tm = team_in
	ORDER BY season DESC, player;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year_pos;
DELIMITER ;;
CREATE PROCEDURE player_search_year_pos (season_in int, pos_in varchar(50))
BEGIN
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND pos = pos_in
	ORDER BY player;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year_name;
DELIMITER ;;
CREATE PROCEDURE player_search_year_name (season_in int, name_in varchar(50))
BEGIN
	SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND player = name_in
	ORDER BY player;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year_team;
DELIMITER ;;
CREATE PROCEDURE player_search_year_team (season_in int, team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND tm = team_in
	ORDER BY player DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_pos_name;
DELIMITER ;;
CREATE PROCEDURE player_search_pos_name (pos_in VARCHAR(50), name_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		pos = pos_in AND player = name_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_pos_team;
DELIMITER ;;
CREATE PROCEDURE player_search_pos_team (pos_in VARCHAR(50), team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		pos = pos_in AND tm = team_in
	ORDER BY player DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_name_team;
DELIMITER ;;
CREATE PROCEDURE player_search_name_team (name_in varchar(50), team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		player = name_in AND tm = team_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year_pos_name;
DELIMITER ;;
CREATE PROCEDURE player_search_year_pos_name (season_in int, pos_in VARCHAR(50), name_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND pos = pos_in AND player = name_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_year_pos_team;
DELIMITER ;;
CREATE PROCEDURE player_search_year_pos_team (season_in int, pos_in VARCHAR(50), team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND pos = pos_in AND tm = team_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_pos_name_team;
DELIMITER ;;
CREATE PROCEDURE player_search_pos_name_team (pos_in VARCHAR(50), name_in varchar(50), team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		pos = pos_in AND player = name_in AND tm = team_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_all;
DELIMITER ;;
CREATE PROCEDURE player_search_all (season_in int, pos_in VARCHAR(50), name_in varchar(50), team_in varchar(50))
BEGIN
SELECT 
		player.player, season.season, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	WHERE 
		season = season_in AND pos = pos_in AND player = name_in AND tm = team_in
	ORDER BY season DESC;
end ;;
DELIMITER ;

-- Populate player search drop downs

drop procedure if EXISTS player_search_years_drop_down;
DELIMITER ;;
CREATE PROCEDURE player_search_years_drop_down ()
BEGIN
	SELECT DISTINCT
		season
	FROM
		nba_app.season_table
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_position_drop_down;
DELIMITER ;;
CREATE PROCEDURE player_search_position_drop_down ()
BEGIN
SELECT 
		DISTINCT pos
	FROM
		nba_app.player_stats
	ORDER BY pos ASC;
end ;;
DELIMITER ;

drop procedure if EXISTS player_search_team_drop_down;
DELIMITER ;;
CREATE PROCEDURE player_search_team_drop_down ()
BEGIN
	SELECT Distinct abbreviation FROM nba_app.team_table
		ORDER BY abbreviation ASC;
end ;;
DELIMITER ;


-- fantasy team procedures

drop procedure if EXISTS fantasy_team_search;
DELIMITER ;;
CREATE PROCEDURE fantasy_team_search (username_in varchar(50))
BEGIN
	SELECT team_name, player_count FROM nba_app.fantasy_teams
    WHERE
    username = username_in
		ORDER BY team_name ASC;
end ;;
DELIMITER ;

drop procedure if EXISTS fantasy_team_add;
DELIMITER ;;
CREATE PROCEDURE fantasy_team_add (username_in varchar(50), team_name_in varchar(50))
BEGIN
	INSERT INTO nba_app.fantasy_teams (username, team_name, player_count)
	VALUES (username_in, team_name_in, 0);
end ;;
DELIMITER ;

drop procedure if EXISTS fantasy_team_delete;
DELIMITER ;;
CREATE PROCEDURE fantasy_team_delete (username_in varchar(50), team_name_in varchar(50))
BEGIN
	DELETE FROM nba_app.fantasy_teams WHERE username=username_in AND team_name = team_name_in;
end ;;
DELIMITER ;

-- fantasy player procedures

drop procedure if EXISTS fantasy_player_search;
DELIMITER ;;
CREATE PROCEDURE fantasy_player_search (username_in varchar(50), team_name_in varchar(50))
BEGIN
SELECT 
		player.player, stats.pos, stats.tm
	FROM
		nba_app.player_stats as stats
	JOIN 
		nba_app.player_table as player
	ON
		stats.player_id = player.player_id
	JOIN 
		nba_app.season_table as season
	ON 
		season.seas_id = stats.seas_id
	JOIN 
		nba_app.fantasy_players as fp
    ON
		fp.players = stats.player_id
    WHERE
		fp.username = username_in
    AND
		fp.team_name = team_name_in
	ORDER BY team_name ASC;
end ;;
DELIMITER ;

DROP TRIGGER If Exists after_player_add;
delimiter $$
CREATE TRIGGER  after_player_add AFTER INSERT ON fantasy_players
       FOR EACH ROW
       BEGIN
			UPDATE nba_app.fantasy_teams 
			SET 
				player_count = player_count + 1
			WHERE
				fantasy_teams.team_name = NEW.team_name
                AND 
                fantasy_teams.username = NEW.username;
       END;$$
delimiter ;


DROP TRIGGER If Exists after_player_deleted;
delimiter $$
CREATE TRIGGER  after_player_deleted AFTER DELETE ON fantasy_players
       FOR EACH ROW
       BEGIN
			UPDATE nba_app.fantasy_teams 
			SET 
				player_count = player_count - 1
			WHERE
				fantasy_teams.team_name = OLD.team_name
                AND 
                fantasy_teams.username = OLD.username;
       END;$$
delimiter ;

drop procedure if EXISTS fantasy_players_add;
DELIMITER ;;
CREATE PROCEDURE fantasy_players_add (username_in varchar(50), team_name_in varchar(50), player_id_in INT)
BEGIN
	INSERT INTO nba_app.fantasy_players (username, team_name, players)
	VALUES (username_in, team_name_in, player_id_in);
end ;;
DELIMITER ;

CALL fantasy_players_add ('test', 'test', 1);

drop procedure if EXISTS player_to_player_id;
DELIMITER ;;
CREATE PROCEDURE player_to_player_id (player_in varchar(50))
BEGIN
	Select
		player_id
	FROM
		player_table
	WHERE
		player_table.player = player_in;
end ;;
DELIMITER ;


drop procedure if EXISTS fantasy_team_all;
DELIMITER ;;
CREATE PROCEDURE fantasy_team_all ()
BEGIN
	SELECT 
		*
	FROM 
		fantasy_teams;    
end ;;
DELIMITER ;


-- end of season teams procedures

drop procedure if EXISTS end_of_season_team_drop_down;
DELIMITER ;;
CREATE PROCEDURE end_of_season_team_drop_down ()
BEGIN
	SELECT Distinct type FROM nba_app.end_of_season_teams
		ORDER BY type ASC;
end ;;
DELIMITER ;

drop procedure if EXISTS generic_eos_search;
DELIMITER ;;
CREATE PROCEDURE generic_eos_search()
BEGIN
	SELECT type, player, season
		FROM end_of_season_teams AS eos
			JOIN player_table AS pt ON eos.player_id = pt.player_id
            JOIN season_table AS st ON eos.seas_id = st.seas_id
            
	ORDER BY season DESC, type;
end ;;
DELIMITER ;

drop procedure if EXISTS eos_search_year;
DELIMITER ;;
CREATE PROCEDURE eos_search_year(season_in INT)
BEGIN
	SELECT type, player, season
		FROM end_of_season_teams AS eos
			JOIN player_table AS pt ON eos.player_id = pt.player_id
            JOIN season_table AS st ON eos.seas_id = st.seas_id
            
		WHERE season = season_in
            
	ORDER BY type;
end ;;
DELIMITER ;

drop procedure if EXISTS eos_search_team;
DELIMITER ;;
CREATE PROCEDURE eos_search_team(team_in VARCHAR(50))
BEGIN
	SELECT type, player, season
		FROM end_of_season_teams AS eos
			JOIN player_table AS pt ON eos.player_id = pt.player_id
            JOIN season_table AS st ON eos.seas_id = st.seas_id
            
		WHERE type = team_in
            
	ORDER BY season DESC;
end ;;
DELIMITER ;

drop procedure if EXISTS eos_search_year_team;
DELIMITER ;;
CREATE PROCEDURE eos_search_year_team(season_in INT, team_in VARCHAR(50))
BEGIN
	SELECT type, player, season
		FROM end_of_season_teams AS eos
			JOIN player_table AS pt ON eos.player_id = pt.player_id
            JOIN season_table AS st ON eos.seas_id = st.seas_id
            
		WHERE season = season_in AND type = team_in
            
	ORDER BY player;
end ;;
DELIMITER ;



    
    

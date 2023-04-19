CREATE DATABASE IF NOT EXISTS nba_app;
USE nba_app;

CREATE TABLE IF NOT EXISTS user_table
(	username VARCHAR(20) PRIMARY KEY,
	first_name CHAR(20) NOT NULL,
    last_name CHAR(20) NOT NULL,
    password varchar(20) NOT NULL
);


/* Procedure to create new user */
delimiter $$
create procedure create_username(username varchar(50), first_name char(50), last_name char(50), password varchar(50))

begin 
  
  INSERT INTO user_table VALUES (username, first_name, last_name, password);
    
end $$
delimiter ;

call create_username('test', 'test', 'test', 'test');

/* Function to check if user account exists 
	CURRENTLY NOT USING THIS IN CODE - KEEPING IN CASE WE DECIDE TO IMPLEMENT IT*/
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


DROP PROCEDURE player_search;
DELIMITER ;;
CREATE PROCEDURE player_search (player_in varchar(50), season_in int, pos_in char(50), team_in varchar(50))
BEGIN
IF (season_in = 0 ) THEN
	SELECT 
		player, season, pos, tm
	FROM
		nba_app.player_final
	ORDER BY player, season;
ELSE
	SELECT 
		player, season, pos, tm
	FROM
		nba_app.player_final
	WHERE
		season = season_in
	ORDER BY player, season;
END IF; 
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE generic_player_search ()
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		ORDER BY player, season;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year (season_in int)
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in
		ORDER BY player;
end ;;
DELIMITER ;

drop procedure player_search_pos;
DELIMITER ;;
CREATE PROCEDURE player_search_pos (pos_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE pos = pos_in
		ORDER BY player;
end ;;
DELIMITER ;

CALL player_search_pos('PG');

DELIMITER ;;
CREATE PROCEDURE player_search_name (name_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE player = name_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_team (team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE tm = team_in
		ORDER BY season DESC, player;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year_pos (season_in int, pos_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND pos = pos_in
		ORDER BY player;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year_name (season_in int, name_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND player = name_in
		ORDER BY player;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year_team (season_in int, team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND tm = team_in
		ORDER BY player DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_pos_name (pos_in VARCHAR(50), name_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE pos = pos_in AND player = name_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_pos_team (pos_in VARCHAR(50), team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE pos = pos_in AND tm = team_in
		ORDER BY player DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_name_team (name_in varchar(50), team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE player = name_in AND tm = team_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year_pos_name (season_in int, pos_in VARCHAR(50), name_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND pos = pos_in AND player = name_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_year_pos_team (season_in int, pos_in VARCHAR(50), team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND pos = pos_in AND tm = team_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_pos_name_team (pos_in VARCHAR(50), name_in varchar(50), team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE pos = pos_in AND player = name_in AND tm = team_in
		ORDER BY season DESC;
end ;;
DELIMITER ;

DELIMITER ;;
CREATE PROCEDURE player_search_all (season_in int, pos_in VARCHAR(50), name_in varchar(50), team_in varchar(50))
BEGIN
	SELECT player, season, pos, tm FROM nba_app.player_final
		WHERE season = season_in AND pos = pos_in AND player = name_in AND tm = team_in
		ORDER BY season DESC;
end ;;
DELIMITER ;
    
    

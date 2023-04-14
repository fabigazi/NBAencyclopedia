CREATE DATABASE IF NOT EXISTS nba_app;
USE nba_app;

CREATE TABLE user_table
(	username VARCHAR(20) PRIMARY KEY,
	first_name CHAR(20) NOT NULL,
    last_name CHAR(20) NOT NULL,
    password varchar(20) NOT NULL
);


/* Procedure to create new user */
drop procedure if exists create_username;
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
    
    

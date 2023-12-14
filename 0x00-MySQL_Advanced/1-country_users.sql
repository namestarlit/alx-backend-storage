-- Create a table users with 3 columns
CREATE TABLE IF NOT EXISTS users(
	id		INT PRIMARY KEY
			AUTO_INCREMENT			NOT NULL,
	email	VARCHAR(255) UNIQUE		NOT NULL,
	name	VARCHAR(255),
	country ENUM('US', 'CO', 'TN')	NOT NULL
);

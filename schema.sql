CREATE TABLE skills (
	id INTEGER PRIMARY KEY, 
	title CHAR(100) NOT NULL, 
	description CHAR(255) NOT NULL, 
	url CHAR(255) NOT NULL, 
	image_path CHAR(255) NOT NULL
);

CREATE TABLE challenges (
	id INTEGER PRIMARY KEY, 
	image_url CHAR(255) NOT NULL, 
	description CHAR(255) NOT NULL, 
	title CHAR(100) NOT NULL, 
	skill_id INTEGER NOT NULL, 
	FOREIGN KEY(skill_id) REFERENCES skills(id)
);

CREATE TABLE makers (
	id INTEGER PRIMARY KEY, 
	nickname CHAR(100) NOT NULL, 
	avatar CHAR(100) NOT NULL
);

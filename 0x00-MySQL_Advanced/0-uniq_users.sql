--We are all unique
--We are all unique
DROP TABLE IF EXIST users;
CREATE TABLE IF NOT EXIST users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
);
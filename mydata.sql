CREATE DATABASE mydata;

USE mydata;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE vaccination_center (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  working_hours VARCHAR(255) NOT NULL,
  dosage_count INT NOT NULL
);

CREATE TABLE vaccination_slot (
  id INT AUTO_INCREMENT PRIMARY KEY,
  center_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  age INT NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  FOREIGN KEY (center_id) REFERENCES vaccination_center (id)
);

INSERT INTO `admin`(`id`, `username`, `password`) VALUES ('1','admin1','abcdefg')





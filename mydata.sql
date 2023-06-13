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
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    working_hours VARCHAR(255) NOT NULL
);

CREATE TABLE vaccination_slot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    center_id INT NOT NULL,
    user_id INT NOT NULL,
    slot_date DATE NOT NULL,
    slot_time TIME NOT NULL
);

ALTER TABLE vaccination_slot ADD CONSTRAINT fk_center_id FOREIGN KEY (center_id) REFERENCES vaccination_center(id);
ALTER TABLE vaccination_slot ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user(id);

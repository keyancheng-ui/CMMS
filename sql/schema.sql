CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  ssn CHAR(9) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  gender VARCHAR(10),
  level VARCHAR(20),
  supervisor_id INT NULL
);

CREATE TABLE IF NOT EXISTS contractors (
  id INT PRIMARY KEY AUTO_INCREMENT,
  ssn CHAR(9) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  company VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS temp_employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  ssn CHAR(9) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  gender VARCHAR(10),
  company_id INT,
  supervisor_id INT
);

CREATE TABLE IF NOT EXISTS locations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  building VARCHAR(100),
  floor VARCHAR(20),
  room VARCHAR(20),
  UNIQUE KEY uniq_loc (building, floor, room)
);

CREATE TABLE IF NOT EXISTS activities (
  id INT PRIMARY KEY AUTO_INCREMENT,
  manager_id INT,
  location_id INT,
  activity_date DATE,
  activity_type VARCHAR(50),
  description VARCHAR(255),
  requires_chemical TINYINT DEFAULT 0,
  result VARCHAR(255),
  finish_time DATETIME
);

CREATE TABLE IF NOT EXISTS activity_employees (
  activity_id INT,
  employee_id INT,
  PRIMARY KEY (activity_id, employee_id)
);

CREATE TABLE IF NOT EXISTS activity_contractors (
  activity_id INT,
  contractor_id INT,
  PRIMARY KEY (activity_id, contractor_id)
);

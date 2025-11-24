CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS employees (
  ssn CHAR(9) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  level VARCHAR(20),
  supervisor_ssn CHAR(9) NULL,
  supervisee_ssn CHAR(9) NULL,
  office_location_id INT NULL
);

CREATE TABLE IF NOT EXISTS contractor_companies (
  name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS temp_employees (
  TempSsn CHAR(9) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  company VARCHAR(100) NOT NULL
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
  activity_date DATE,
  activity_type VARCHAR(50),
  description VARCHAR(255),
  requires_chemical TINYINT DEFAULT 0,
  result VARCHAR(255),
  finish_time DATETIME
);

CREATE TABLE IF NOT EXISTS activity_employees (
  activity_id INT,
  employee_ssn CHAR(9),
  PRIMARY KEY (activity_id, employee_ssn)
);



CREATE TABLE IF NOT EXISTS activity_temp_employees (
  activity_id INT,
  temp_employee_ssn CHAR(9),
  PRIMARY KEY (activity_id, temp_employee_ssn)
);

CREATE TABLE IF NOT EXISTS supervise (
  employee_id INT NOT NULL,
  supervisor_id INT NOT NULL,
  PRIMARY KEY (employee_id, supervisor_id),
  UNIQUE KEY uniq_employee (employee_id)
);

CREATE TABLE IF NOT EXISTS dependents (
  id INT PRIMARY KEY AUTO_INCREMENT,
  employee_id INT NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  relationship VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS activity_locations (
  activity_id INT NOT NULL,
  location_id INT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  PRIMARY KEY (activity_id, location_id)
);

ALTER TABLE employees
  ADD COLUMN office_location_id INT NULL,
  ADD CONSTRAINT fk_employees_office_loc FOREIGN KEY (office_location_id) REFERENCES locations(id);



ALTER TABLE temp_employees
  ADD CONSTRAINT fk_temp_employees_company FOREIGN KEY (company) REFERENCES contractor_companies(name);

ALTER TABLE activity_employees
  ADD CONSTRAINT fk_act_emp_activity FOREIGN KEY (activity_id) REFERENCES activities(id),
  ADD CONSTRAINT fk_act_emp_employee FOREIGN KEY (employee_ssn) REFERENCES employees(ssn);



ALTER TABLE activity_temp_employees
  ADD CONSTRAINT fk_act_temp_activity FOREIGN KEY (activity_id) REFERENCES activities(id),
  ADD CONSTRAINT fk_act_temp_temp FOREIGN KEY (temp_employee_ssn) REFERENCES temp_employees(TempSsn);

CREATE TABLE IF NOT EXISTS supervise_temp_employees (
  temp_employee_ssn CHAR(9) NOT NULL,
  supervisor_ssn CHAR(9) NOT NULL,
  PRIMARY KEY (temp_employee_ssn, supervisor_ssn),
  UNIQUE KEY uniq_temp (temp_employee_ssn)
);

CREATE TABLE IF NOT EXISTS supervise_contractor_companies (
  company_name VARCHAR(100) NOT NULL,
  supervisor_ssn CHAR(9) NOT NULL,
  PRIMARY KEY (company_name, supervisor_ssn),
  UNIQUE KEY uniq_company (company_name)
);

ALTER TABLE supervise_temp_employees
  ADD CONSTRAINT fk_sup_temp_emp FOREIGN KEY (temp_employee_ssn) REFERENCES temp_employees(TempSsn),
  ADD CONSTRAINT fk_sup_temp_sup FOREIGN KEY (supervisor_ssn) REFERENCES employees(ssn);

ALTER TABLE supervise_contractor_companies
  ADD CONSTRAINT fk_sup_cc_company FOREIGN KEY (company_name) REFERENCES contractor_companies(name),
  ADD CONSTRAINT fk_sup_cc_sup FOREIGN KEY (supervisor_ssn) REFERENCES employees(ssn);

ALTER TABLE supervise
  ADD CONSTRAINT fk_supervise_emp FOREIGN KEY (employee_id) REFERENCES employees(ssn),
  ADD CONSTRAINT fk_supervise_sup FOREIGN KEY (supervisor_id) REFERENCES employees(ssn);

ALTER TABLE dependents
  ADD CONSTRAINT fk_dependents_employee FOREIGN KEY (employee_id) REFERENCES employees(ssn);

ALTER TABLE activity_locations
  ADD CONSTRAINT fk_act_loc_activity FOREIGN KEY (activity_id) REFERENCES activities(id),
  ADD CONSTRAINT fk_act_loc_location FOREIGN KEY (location_id) REFERENCES locations(id);

-- application-level enforcement for one activity per location/date is implemented in ActivityDAO.add

ALTER TABLE employees ADD COLUMN supervisor_ssn CHAR(9) NULL;
ALTER TABLE employees ADD COLUMN supervisee_ssn CHAR(9) NULL;

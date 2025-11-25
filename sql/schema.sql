CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS Employee (
  Ssn CHAR(20) PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Emp_Level ENUM('executive officer', 'mid_level manager', 'base_level worker') NOT NULL
);

CREATE TABLE IF NOT EXISTS Office (
  OwnerSsn CHAR(20) NULL,
  Office_Building CHAR(20) NOT NULL,
  Office_Floor INT NOT NULL,
  Office_RoomNum INT NOT NULL,
  
  CONSTRAINT fk_office_owner FOREIGN KEY (OwnerSsn)
  REFERENCES Employee(Ssn)
  ON DELETE SET NULL
  ON UPDATE CASCADE,

  CONSTRAINT fk_office_location FOREIGN KEY (Office_Building, Office_Floor, Office_RoomNum)
  REFERENCES Location(Building, Floor, Room_number)
  ON UPDATE CASCADE,

  PRIMARY KEY (Office_Building, Office_Floor, Office_RoomNum)
  
);

CREATE TABLE IF NOT EXISTS  Location (
  
  Building CHAR(20) NOT NULL,
  Floor INT NOT NULL,
  Room_number INT NOT NULL,
  PRIMARY KEY (Building, Floor, Room_number)
  
);

CREATE TABLE IF NOT EXISTS Employee_Supervision (
  
  Supervisor_Ssn CHAR(20) NOT NULL,
  CONSTRAINT fk_supervisor_relation FOREIGN KEY (Supervisor_Ssn, Supervisee_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE，

  Supervisee_Ssn CHAR(20) NOT NULL,
  CONSTRAINT fk_supervision_relation FOREIGN KEY (Supervisor_Ssn, Supervisee_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE，

  PRIMARY KEY (Supervisor_Ssn, Supervisee_Ssn),
  CONSTRAINT chk_no_self_supervision CHECK (Supervisor_Ssn != Supervisee_Ssn)
);

CREATE TABLE IF NOT EXISTS TempSupervise (
  Supervisor_Ssn_midlevel_manager CHAR(20) NOT NULL,
  CONSTRAINT fk_temp_supervisor FOREIGN KEY (Supervisor_Ssn_midlevel_manager)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,
  
  Supervisee_Ssn_temp_employee CHAR(20) NOT NULL,
  CONSTRAINT fk_temp_supervisor FOREIGN KEY (Supervisee_Ssn_temp_employee)
  REFERENCES Temporary_Employee(TempSsn)
  ON UPDATE CASCADE,

  PRIMARY KEY (temp_employee_ssn, supervisor_ssn)
  
);

CREATE TABLE IF NOT EXISTS Temporary_Employee (
  TempSsn CHAR(20) PRIMARY KEY,
  Company_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Contractor_Company (
  Temp_Employee_Ssn CHAR(20) PRIMARY KEY,
  
  CONSTRAINT fk_temp_employee_company FOREIGN KEY (Temp_Employee_Ssn)
  REFERENCES Temporary_Employee(TempSsn)
  ON UPDATE CASCADE,
  
  name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Activity (
  
  Activity_Time DATE NOT NULL,
  Activity_Type ENUM('daily campus cleaning', 'campus ageing', 'weather-related issues') NOT NULL
  Require_Chemical TINYINT DEFAULT 0,

  Activity_Building CHAR(20) NOT NULL,
  Activity_Floor INT NOT NULL,
  Activity_RoomNum INT NOT NULL,

  CONSTRAINT fk_activity_location FOREIGN KEY (Activity_Building, Activity_Floor, Activity_RoomNum)
  REFERENCES Location(Building, Floor, Room_number)
  ON UPDATE CASCADE,

  PRIMARY KEY (Activity_Time, Activity_Building, Activity_Floor, Activity_RoomNum)
  
);

CREATE TABLE IF NOT EXISTS Mid_Level_Manage_Activity (
  Manager_Ssn CHAR(20),
  
  CONSTRAINT fk_activity_manager FOREIGN KEY (Manager_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,

  CONSTRAINT chk_manager_level CHECK (
    Manager_Ssn IN (SELECT Ssn 
                    FROM Employee 
                    WHERE Emp_Level = 'mid_level manager')
  ),


  Manage_Activity_Building CHAR(20) NOT NULL,
  Manage_Activity_Floor INT NOT NULL,
  Manage_Activity_RoomNum INT NOT NULL,

  Manage_Activity_Time DATE NOT NULL,

  CONSTRAINT fk_manage_activity_location_and_time FOREIGN KEY (Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
  REFERENCES Activity (Activity_Building, Activity_Floor, Activity_RoomNum, Activity_Time)
  ON UPDATE CASCADE,

  PRIMARY KEY ( Activity_Building, Activity_Floor, Activity_RoomNum, Activity_Time)
);











CREATE TABLE IF NOT EXISTS temp_employees (
  TempSsn CHAR(9) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  company VARCHAR(100) NOT NULL
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

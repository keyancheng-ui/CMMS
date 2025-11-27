CREATE DATABASE IF NOT EXISTS appdb;
USE appdb;

CREATE TABLE IF NOT EXISTS Employee (
  Ssn CHAR(20) PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Emp_Level ENUM('executive officer', 'mid_level manager', 'base_level worker') NOT NULL
);

CREATE TABLE IF NOT EXISTS Temporary_Employee (
  TempSsn CHAR(20) PRIMARY KEY,
  Company_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS  Location (
  
  Building CHAR(20) NOT NULL,
  Floor INT NOT NULL,
  Room_number INT NOT NULL,
  PRIMARY KEY (Building, Floor, Room_number)
  
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


CREATE TABLE IF NOT EXISTS Employee_Supervision (
  
  Supervisor_Ssn CHAR(20) NOT NULL,
  CONSTRAINT fk_supervisor_relation FOREIGN KEY (Supervisor_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,

  Supervisee_Ssn CHAR(20) NOT NULL,
  CONSTRAINT fk_supervision_relation FOREIGN KEY (Supervisee_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,

  PRIMARY KEY (Supervisor_Ssn, Supervisee_Ssn)
  -- CONSTRAINT chk_no_self_supervision CHECK (Supervisor_Ssn != Supervisee_Ssn)
);

CREATE TABLE IF NOT EXISTS TempSupervise (
  Supervisor_Ssn_midlevel_manager CHAR(20) NOT NULL,
  CONSTRAINT fk_temp_supervisor FOREIGN KEY (Supervisor_Ssn_midlevel_manager)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,
  
  Supervisee_Ssn_temp_employee CHAR(20) NOT NULL,
  CONSTRAINT fk_temp_employee FOREIGN KEY (Supervisee_Ssn_temp_employee)
  REFERENCES Temporary_Employee(TempSsn)
  ON UPDATE CASCADE,

  PRIMARY KEY (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
  
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
  Activity_Type ENUM('daily campus cleaning', 'campus ageing', 'weather-related issues') NOT NULL,
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
  Manager_Ssn CHAR(20) NOT NULL,
  
  CONSTRAINT fk_activity_manager FOREIGN KEY (Manager_Ssn)
  REFERENCES Employee(Ssn)
  ON UPDATE CASCADE,

  -- CONSTRAINT chk_manager_level CHECK (
  --  Manager_Ssn IN (SELECT Ssn
  --                  FROM Employee
  --                  WHERE Emp_Level = 'mid_level manager')
  -- ),


  Manage_Activity_Building CHAR(20) NOT NULL,
  Manage_Activity_Floor INT NOT NULL,
  Manage_Activity_RoomNum INT NOT NULL,

  Manage_Activity_Time DATE NOT NULL,

  CONSTRAINT fk_manage_activity_location_and_time FOREIGN KEY (Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
  REFERENCES Activity (Activity_Building, Activity_Floor, Activity_RoomNum, Activity_Time)
  ON UPDATE CASCADE,

  PRIMARY KEY ( Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
);

CREATE TABLE IF NOT EXISTS Employee_Work_On (
  
  Working_Time DATE NOT NULL,
  Working_Building CHAR(20) NOT NULL,
  Working_Floor INT NOT NULL,
  Working_Room_number INT NOT NULL,

  
  Working_Worker_Ssn CHAR(20) NOT NULL,
  -- CONSTRAINT working_worker_level CHECK (
  --   Working_Worker_Ssn IN (SELECT Ssn
  --                         FROM Employee
  --                         WHERE Emp_Level = 'base_level worker')
  -- ),

  
  PRIMARY KEY (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn),
  
  CONSTRAINT fk_working_activity_location FOREIGN KEY ( Working_Building,  Working_Floor,  Working_Room_number)
  REFERENCES Activity (Activity_Building, Activity_Floor, Activity_RoomNum)
  ON UPDATE CASCADE,

  CONSTRAINT fk_working_activity_time FOREIGN KEY ( Working_Time)
  REFERENCES Activity (Activity_Time)
  ON UPDATE CASCADE,

  CONSTRAINT fk_working_employee_Ssn FOREIGN KEY ( Working_Worker_Ssn)
  REFERENCES Employee (Ssn)
  ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS Temp_Employee_Work_On (
  
  Temp_Working_Time DATE NOT NULL,
  Temp_Working_Building CHAR(20) NOT NULL,
  Temp_Working_Floor INT NOT NULL,
  Temp_Working_Room_number INT NOT NULL,

  
  Temp_Working_Worker_Ssn CHAR(20) NOT NULL,
    
  PRIMARY KEY (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn),
  
  CONSTRAINT fk_temp_working_activity_location FOREIGN KEY ( Temp_Working_Building,  Temp_Working_Floor,  Temp_Working_Room_number)
  REFERENCES Activity (Activity_Building, Activity_Floor, Activity_RoomNum)
  ON UPDATE CASCADE,

  CONSTRAINT fk_temp_working_activity_time FOREIGN KEY ( Temp_Working_Time)
  REFERENCES Activity (Activity_Time)
  ON UPDATE CASCADE,

  CONSTRAINT fk_temp_working_employee_Ssn FOREIGN KEY ( Temp_Working_Worker_Ssn)
  REFERENCES Temporary_Employee (TempSsn)
  ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS Applied_To (

  Applied_Time DATE NOT NULL,
  Applied_Building CHAR(20) NOT NULL,
  Applied_Floor INT NOT NULL,
  Applied_Room_number INT NOT NULL,
  Applied_Reason CHAR(100) NOT NULL,
    
  PRIMARY KEY (Applied_Time, Applied_Building,  Applied_Floor,  Applied_Room_number),
  
  CONSTRAINT fk_applied_location FOREIGN KEY (Applied_Building,  Applied_Floor,  Applied_Room_number)
  REFERENCES Location (Building, Floor, Room_number)
  ON UPDATE CASCADE,

  CONSTRAINT fk_applied_time FOREIGN KEY ( Applied_Time)
  REFERENCES Activity (Activity_Time)
  ON UPDATE CASCADE
);




















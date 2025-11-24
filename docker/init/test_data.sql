USE appdb;
INSERT INTO locations (name) VALUES ('HQ'), ('Remote');
INSERT INTO employees (name, role, location_id) VALUES
('Alice', 'Engineer', 1),
('Bob', 'Manager', 1),
('Carol', 'Analyst', 2);
INSERT INTO activities (employee_id, description, activity_time) VALUES
(1, 'Deployed new feature', NOW()),
(2, 'Reviewed quarterly report', NOW()),
(3, 'Built dashboard', NOW());

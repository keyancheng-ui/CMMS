USE appdb;

INSERT INTO locations (building, floor, room) VALUES
('Main', '1', '101'),
('B', 'G', 'P1');

INSERT INTO employees (ssn, name, gender, level) VALUES
('111111111', 'Alice', 'F', 'middle'),
('222222222', 'Bob', 'M', 'high'),
('333333333', 'Carol', 'F', 'basic');

INSERT INTO activities (manager_id, location_id, activity_date, activity_type, description, requires_chemical)
VALUES
((SELECT id FROM employees WHERE ssn='222222222'), 1, '2025-11-24', 'cleaning', 'Lobby daily', 0),
((SELECT id FROM employees WHERE ssn='222222222'), 2, '2025-11-24', 'maintenance', 'Parking ventilation check', 0);

INSERT INTO activity_employees (activity_id, employee_id)
SELECT 1, (SELECT id FROM employees WHERE ssn='111111111');

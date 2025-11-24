USE appdb;
SELECT id, name, role FROM employees ORDER BY id;
SELECT e.name, COUNT(a.id) AS activity_count FROM employees e LEFT JOIN activities a ON a.employee_id=e.id GROUP BY e.id ORDER BY activity_count DESC;

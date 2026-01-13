USE appdb;




-- 1. Location (主键: Building, Floor, Room_number)
INSERT INTO Location (Building, Floor, Room_number)
SELECT * FROM (
    VALUES
    ROW('Main_Building', 1, 101),
    ROW('Main_Building', 1, 102),
    ROW('Main_Building', 2, 201),
    ROW('Main_Building', 3, 301),
    ROW('Tech_Building', 1, 103),
    ROW('Tech_Building', 2, 204),
    ROW('Tech_Building', 3, 305),
    ROW('Admin_Building', 1, 106),
    ROW('Admin_Building', 2, 207),
    ROW('Admin_Building', 3, 308),
    ROW('Service_Building', 1, 109),
    ROW('Service_Building', 2, 210),
    ROW('FrontGate', 0, 0),
    ROW('BackGate', 0, 0),
    ROW('Square', 0, 0)
) AS new_vals (Building, Floor, Room_number)
WHERE NOT EXISTS (
    SELECT 1 FROM Location l
    WHERE l.Building = new_vals.Building
      AND l.Floor = new_vals.Floor
      AND l.Room_number = new_vals.Room_number
);

-- 2. Employee (主键: Ssn)
INSERT INTO Employee (Ssn, Name, Emp_Level)
SELECT * FROM (
    VALUES
    ROW('1', '张三', 'executive officer'),
    ROW('2', '李四', 'mid_level manager'),
    ROW('3', '王五', 'mid_level manager'),
    ROW('4', '赵六', 'base_level worker'),
    ROW('5', '孙七', 'base_level worker'),
    ROW('6', '周八', 'base_level worker'),
    ROW('7', '吴九', 'mid_level manager'),
    ROW('8', '郑十', 'base_level worker'),
    ROW('9', '钱十一', 'base_level worker'),
    ROW('10', '冯十二', 'executive officer'),
    ROW('11', '陈十三', 'base_level worker'),
    ROW('12', '褚十四', 'base_level worker'),
    ROW('99999', '褚十四', 'base_level worker')
) AS new_vals (Ssn, Name, Emp_Level)
WHERE NOT EXISTS (
    SELECT 1 FROM Employee e WHERE e.Ssn = new_vals.Ssn
);

-- 3. Office (主键: Office_Building, Office_Floor, Office_RoomNum)
INSERT INTO Office (OwnerSsn, Office_Building, Office_Floor, Office_RoomNum)
SELECT * FROM (
    VALUES
    ROW('1', 'Admin_Building', 3, 308),
    ROW('2', 'Main_Building', 1, 101),
    ROW('3', 'Tech_Building', 2, 204),
    ROW('7', 'Tech_Building', 3, 305),
    ROW('10', 'Admin_Building', 2, 207),
    ROW(NULL, 'Main_Building', 1, 102),
    ROW(NULL, 'Main_Building', 2, 201),
    ROW(NULL, 'Tech_Building', 1, 103),
    ROW(NULL, 'Admin_Building', 1, 106),
    ROW(NULL, 'Service_Building', 1, 109),
    ROW('2', 'Service_Building', 2, 210),
    ROW('3', 'Main_Building', 3, 301)
) AS new_vals (OwnerSsn, Office_Building, Office_Floor, Office_RoomNum)
WHERE NOT EXISTS (
    SELECT 1 FROM Office o
    WHERE o.Office_Building = new_vals.Office_Building
      AND o.Office_Floor = new_vals.Office_Floor
      AND o.Office_RoomNum = new_vals.Office_RoomNum
);

-- 4. Employee_Supervision (主键: Supervisor_Ssn, Supervisee_Ssn)
INSERT INTO Employee_Supervision (Supervisor_Ssn, Supervisee_Ssn)
SELECT * FROM (
    VALUES
    ROW('1', '2'),
    ROW('1', '3'),
    ROW('1', '7'),
    ROW('10', '2'),
    ROW('10', '3'),
    ROW('10', '7'),
    ROW('2', '4'),
    ROW('2', '5'),
    ROW('2', '8'),
    ROW('3', '6'),
    ROW('3', '9'),
    ROW('7', '11'),
    ROW('7', '12'),
    ROW('2', '12'),
    ROW('3', '8')
) AS new_vals (Supervisor_Ssn, Supervisee_Ssn)
WHERE NOT EXISTS (
    SELECT 1 FROM Employee_Supervision es
    WHERE es.Supervisor_Ssn = new_vals.Supervisor_Ssn
      AND es.Supervisee_Ssn = new_vals.Supervisee_Ssn
);

-- 5. Temporary_Employee (主键: TempSsn)
INSERT INTO Temporary_Employee (TempSsn, Company_name)
SELECT * FROM (
    VALUES
    ROW('T200000001', '保洁服务有限公司'),
    ROW('T200000002', '维修服务外包公司'),
    ROW('T200000003', '绿化养护合作公司'),
    ROW('T200000004', '设备检测外包公司'),
    ROW('T200000005', '水电维修服务公司'),
    ROW('T200000006', '外墙清洁服务公司'),
    ROW('T200000007', '垃圾清运合作公司'),
    ROW('T200000008', '空调维护外包公司'),
    ROW('T200000009', '消防检查服务公司'),
    ROW('T200000010', '电梯维保外包公司'),
    ROW('T200000011', '管道疏通服务公司'),
    ROW('T200000012', '地毯清洁服务公司'),
    ROW('T200000013', '门窗维修外包公司'),
    ROW('T200000014', '灯具更换服务公司'),
    ROW('T200000015', '墙面翻新服务公司')
) AS new_vals (TempSsn, Company_name)
WHERE NOT EXISTS (
    SELECT 1 FROM Temporary_Employee te WHERE te.TempSsn = new_vals.TempSsn
);

-- 6. TempSupervise (主键: Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
INSERT INTO TempSupervise (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
SELECT * FROM (
    VALUES
    ROW('2', 'T200000001'),
    ROW('2', 'T200000002'),
    ROW('3', 'T200000003'),
    ROW('3', 'T200000004'),
    ROW('7', 'T200000005'),
    ROW('7', 'T200000006'),
    ROW('2', 'T200000007'),
    ROW('3', 'T200000008'),
    ROW('7', 'T200000009'),
    ROW('2', 'T200000010'),
    ROW('3', 'T200000011'),
    ROW('7', 'T200000012'),
    ROW('2', 'T200000013'),
    ROW('3', 'T200000014'),
    ROW('7', 'T200000015')
) AS new_vals (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
WHERE NOT EXISTS (
    SELECT 1 FROM TempSupervise ts
    WHERE ts.Supervisor_Ssn_midlevel_manager = new_vals.Supervisor_Ssn_midlevel_manager
      AND ts.Supervisee_Ssn_temp_employee = new_vals.Supervisee_Ssn_temp_employee
);

-- 7. Contractor_Company (主键: Temp_Employee_Ssn)
INSERT INTO Contractor_Company (Temp_Employee_Ssn, name)
SELECT * FROM (
    VALUES
    ROW('T200000001', '保洁服务有限公司'),
    ROW('T200000002', '维修服务外包公司'),
    ROW('T200000003', '绿化养护合作公司'),
    ROW('T200000004', '设备检测外包公司'),
    ROW('T200000005', '水电维修服务公司'),
    ROW('T200000006', '外墙清洁服务公司'),
    ROW('T200000007', '垃圾清运合作公司'),
    ROW('T200000008', '空调维护外包公司'),
    ROW('T200000009', '消防检查服务公司'),
    ROW('T200000010', '电梯维保外包公司'),
    ROW('T200000011', '管道疏通服务公司'),
    ROW('T200000012', '地毯清洁服务公司'),
    ROW('T200000013', '门窗维修外包公司'),
    ROW('T200000014', '灯具更换服务公司'),
    ROW('T200000015', '墙面翻新服务公司')
) AS new_vals (Temp_Employee_Ssn, name)
WHERE NOT EXISTS (
    SELECT 1 FROM Contractor_Company cc WHERE cc.Temp_Employee_Ssn = new_vals.Temp_Employee_Ssn
);

-- 8. Activity (主键: Activity_Time, Activity_Building, Activity_Floor, Activity_RoomNum)
INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum)
SELECT * FROM (
    VALUES
    ROW('2025-11-20', 'daily campus cleaning', 1, 'Main_Building', 1, 101),
    ROW('2025-11-20', 'daily campus cleaning', 0, 'Main_Building', 1, 102),
    ROW('2025-11-21', 'campus ageing', 0, 'Tech_Building', 2, 204),
    ROW('2025-11-21', 'weather-related issues', 1, 'Admin_Building', 3, 308),
    ROW('2025-11-22', 'daily campus cleaning', 1, 'Main_Building', 2, 201),
    ROW('2025-11-22', 'campus ageing', 0, 'Tech_Building', 3, 305),
    ROW('2025-11-23', 'weather-related issues', 0, 'Service_Building', 1, 109),
    ROW('2025-11-23', 'daily campus cleaning', 1, 'Admin_Building', 1, 106),
    ROW('2025-11-24', 'campus ageing', 1, 'Main_Building', 3, 301),
    ROW('2025-11-24', 'daily campus cleaning', 0, 'Tech_Building', 1, 103),
    ROW('2025-11-25', 'weather-related issues', 1, 'Service_Building', 2, 210),
    ROW('2025-11-25', 'daily campus cleaning', 1, 'Main_Building', 1, 101),
    ROW('2025-11-26', 'campus ageing', 0, 'Admin_Building', 2, 207),
    ROW('2025-11-26', 'daily campus cleaning', 0, 'Tech_Building', 2, 204),
    ROW('2025-11-27', 'weather-related issues', 0, 'Main_Building', 2, 201)
) AS new_vals (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum)
WHERE NOT EXISTS (
    SELECT 1 FROM Activity a
    WHERE a.Activity_Time = new_vals.Activity_Time
      AND a.Activity_Building = new_vals.Activity_Building
      AND a.Activity_Floor = new_vals.Activity_Floor
      AND a.Activity_RoomNum = new_vals.Activity_RoomNum
);

-- 9. Mid_Level_Manage_Activity (主键: Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
SELECT * FROM (
    VALUES
    ROW('2', 'Main_Building', 1, 101, '2025-11-20'),
    ROW('2', 'Main_Building', 1, 102, '2025-11-20'),
    ROW('3', 'Tech_Building', 2, 204, '2025-11-21'),
    ROW('3', 'Admin_Building', 3, 308, '2025-11-21'),
    ROW('7', 'Main_Building', 2, 201, '2025-11-22'),
    ROW('7', 'Tech_Building', 3, 305, '2025-11-22'),
    ROW('2', 'Service_Building', 1, 109, '2025-11-23'),
    ROW('2', 'Admin_Building', 1, 106, '2025-11-23'),
    ROW('3', 'Main_Building', 3, 301, '2025-11-24'),
    ROW('3', 'Tech_Building', 1, 103, '2025-11-24'),
    ROW('7', 'Service_Building', 2, 210, '2025-11-25'),
    ROW('7', 'Main_Building', 1, 101, '2025-11-25'),
    ROW('2', 'Admin_Building', 2, 207, '2025-11-26'),
    ROW('2', 'Tech_Building', 2, 204, '2025-11-26'),
    ROW('3', 'Main_Building', 2, 201, '2025-11-27')
) AS new_vals (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
WHERE NOT EXISTS (
    SELECT 1 FROM Mid_Level_Manage_Activity m
    WHERE m.Manager_Ssn = new_vals.Manager_Ssn
      AND m.Manage_Activity_Building = new_vals.Manage_Activity_Building
      AND m.Manage_Activity_Floor = new_vals.Manage_Activity_Floor
      AND m.Manage_Activity_RoomNum = new_vals.Manage_Activity_RoomNum
      AND m.Manage_Activity_Time = new_vals.Manage_Activity_Time
);

-- 10. Employee_Work_On (主键: Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn)
INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn)
SELECT * FROM (
    VALUES
    ROW('2025-11-20', 'Main_Building', 1, 101, '4'),
    ROW('2025-11-20', 'Main_Building', 1, 102, '5'),
    ROW('2025-11-21', 'Tech_Building', 2, 204, '6'),
    ROW('2025-11-21', 'Admin_Building', 3, 308, '8'),
    ROW('2025-11-22', 'Main_Building', 2, 201, '9'),
    ROW('2025-11-22', 'Tech_Building', 3, 305, '11'),
    ROW('2025-11-23', 'Service_Building', 1, 109, '12'),
    ROW('2025-11-23', 'Admin_Building', 1, 106, '4'),
    ROW('2025-11-24', 'Main_Building', 3, 301, '5'),
    ROW('2025-11-24', 'Tech_Building', 1, 103, '6'),
    ROW('2025-11-25', 'Service_Building', 2, 210, '8'),
    ROW('2025-11-25', 'Main_Building', 1, 101, '9'),
    ROW('2025-11-26', 'Admin_Building', 2, 207, '11'),
    ROW('2025-11-26', 'Tech_Building', 2, 204, '12'),
    ROW('2025-11-27', 'Main_Building', 2, 201, '4')
) AS new_vals (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn)
WHERE NOT EXISTS (
    SELECT 1 FROM Employee_Work_On ewo
    WHERE ewo.Working_Time = new_vals.Working_Time
      AND ewo.Working_Building = new_vals.Working_Building
      AND ewo.Working_Floor = new_vals.Working_Floor
      AND ewo.Working_Room_number = new_vals.Working_Room_number
      AND ewo.Working_Worker_Ssn = new_vals.Working_Worker_Ssn
);

-- 11. Temp_Employee_Work_On (主键: Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
SELECT * FROM (
    VALUES
    ROW('2025-11-20', 'Main_Building', 1, 101, 'T200000001'),
    ROW('2025-11-20', 'Main_Building', 1, 102, 'T200000002'),
    ROW('2025-11-21', 'Tech_Building', 2, 204, 'T200000003'),
    ROW('2025-11-21', 'Admin_Building', 3, 308, 'T200000004'),
    ROW('2025-11-22', 'Main_Building', 2, 201, 'T200000005'),
    ROW('2025-11-22', 'Tech_Building', 3, 305, 'T200000006'),
    ROW('2025-11-23', 'Service_Building', 1, 109, 'T200000007'),
    ROW('2025-11-23', 'Admin_Building', 1, 106, 'T200000008'),
    ROW('2025-11-24', 'Main_Building', 3, 301, 'T200000009'),
    ROW('2025-11-24', 'Tech_Building', 1, 103, 'T200000010'),
    ROW('2025-11-25', 'Service_Building', 2, 210, 'T200000011'),
    ROW('2025-11-25', 'Main_Building', 1, 101, 'T200000012'),
    ROW('2025-11-26', 'Admin_Building', 2, 207, 'T200000013'),
    ROW('2025-11-26', 'Tech_Building', 2, 204, 'T200000014'),
    ROW('2025-11-27', 'Main_Building', 2, 201, 'T200000015')
) AS new_vals (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
WHERE NOT EXISTS (
    SELECT 1 FROM Temp_Employee_Work_On te
    WHERE te.Temp_Working_Time = new_vals.Temp_Working_Time
      AND te.Temp_Working_Building = new_vals.Temp_Working_Building
      AND te.Temp_Working_Floor = new_vals.Temp_Working_Floor
      AND te.Temp_Working_Room_number = new_vals.Temp_Working_Room_number
      AND te.Temp_Working_Worker_Ssn = new_vals.Temp_Working_Worker_Ssn
);

-- 12. Applied_To (主键: Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number)
INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason)
SELECT * FROM (
    VALUES
    ROW('2025-11-20', 'Main_Building', 1, 101, '日常清洁需中性清洁剂申请'),
    ROW('2025-11-20', 'Main_Building', 1, 102, '维修工具借用申请（螺丝刀套装）'),
    ROW('2025-11-21', 'Tech_Building', 2, 204, '绿化肥料采购申请（有机营养液）'),
    ROW('2025-11-21', 'Admin_Building', 3, 308, '设备检测仪器租赁申请（温湿度计）'),
    ROW('2025-11-22', 'Main_Building', 2, 201, '水电维修材料申请（水管接头）'),
    ROW('2025-11-22', 'Tech_Building', 3, 305, '外墙清洁安全绳申请（高空作业）'),
    ROW('2025-11-23', 'Service_Building', 1, 109, '垃圾清运车辆调度申请（密闭式货车）'),
    ROW('2025-11-23', 'Admin_Building', 1, 106, '空调制冷剂补充申请（R410A）'),
    ROW('2025-11-24', 'Main_Building', 3, 301, '消防灭火器年检申请（ABC干粉型）'),
    ROW('2025-11-24', 'Tech_Building', 1, 103, '电梯维保配件申请（门机板）'),
    ROW('2025-11-25', 'Service_Building', 2, 210, '管道疏通药剂申请（生物酶制剂）'),
    ROW('2025-11-25', 'Main_Building', 1, 101, '地毯除渍剂申请（中性去污剂）'),
    ROW('2025-11-26', 'Admin_Building', 2, 207, '门窗密封条更换申请（硅胶条）'),
    ROW('2025-11-26', 'Tech_Building', 2, 204, 'LED灯具采购申请（3000K暖光）'),
    ROW('2025-11-27', 'Main_Building', 2, 201, '墙面翻新涂料申请（环保乳胶漆）')
) AS new_vals (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason)
WHERE NOT EXISTS (
    SELECT 1 FROM Applied_To a
    WHERE a.Applied_Time = new_vals.Applied_Time
      AND a.Applied_Building = new_vals.Applied_Building
      AND a.Applied_Floor = new_vals.Applied_Floor
      AND a.Applied_Room_number = new_vals.Applied_Room_number
);
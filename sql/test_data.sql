-- 切换到目标数据库
USE appdb;

-- 清空已有数据（按外键依赖逆序删除）
DELETE FROM Applied_To;
DELETE FROM Temp_Employee_Work_On;
DELETE FROM Employee_Work_On;
DELETE FROM Mid_Level_Manage_Activity;
DELETE FROM Activity;
DELETE FROM Contractor_Company;
DELETE FROM TempSupervise;
DELETE FROM Temporary_Employee;
DELETE FROM Employee_Supervision;
DELETE FROM Office;
DELETE FROM Employee;
DELETE FROM Location;

-- 1. Location 表（12条数据）
INSERT INTO Location (Building, Floor, Room_number)
VALUES
('Main_Building', 1, 101),
('Main_Building', 1, 102),
('Main_Building', 2, 201),
('Main_Building', 3, 301),
('Tech_Building', 1, 103),
('Tech_Building', 2, 204),
('Tech_Building', 3, 305),
('Admin_Building', 1, 106),
('Admin_Building', 2, 207),
('Admin_Building', 3, 308),
('Service_Building', 1, 109),
('Service_Building', 2, 210);

-- 2. Employee 表（12条数据）
INSERT INTO Employee (Ssn, Name, Emp_Level)
VALUES
('1', '张三', 'executive officer'),
('2', '李四', 'mid_level manager'),
('3', '王五', 'mid_level manager'),
('4', '赵六', 'base_level worker'),
('5', '孙七', 'base_level worker'),
('6', '周八', 'base_level worker'),
('7', '吴九', 'mid_level manager'),
('8', '郑十', 'base_level worker'),
('9', '钱十一', 'base_level worker'),
('10', '冯十二', 'executive officer'),
('11', '陈十三', 'base_level worker'),
('12', '褚十四', 'base_level worker');

-- 3. Office 表（12条数据）- 修正 OwnerSsn 引用
INSERT INTO Office (OwnerSsn, Office_Building, Office_Floor, Office_RoomNum)
VALUES
('1', 'Admin_Building', 3, 308),
('2', 'Main_Building', 1, 101),
('3', 'Tech_Building', 2, 204),
('7', 'Tech_Building', 3, 305),
('10', 'Admin_Building', 2, 207),
(NULL, 'Main_Building', 1, 102),
(NULL, 'Main_Building', 2, 201),
(NULL, 'Tech_Building', 1, 103),
(NULL, 'Admin_Building', 1, 106),
(NULL, 'Service_Building', 1, 109),
('2', 'Service_Building', 2, 210),
('3', 'Main_Building', 3, 301);

-- 4. Employee_Supervision 表（15条数据）- 取消注释并修正 Ssn 引用
INSERT INTO Employee_Supervision (Supervisor_Ssn, Supervisee_Ssn)
VALUES
('1', '2'),
('1', '3'),
('1', '7'),
('10', '2'),
('10', '3'),
('10', '7'),
('2', '4'),
('2', '5'),
('2', '8'),
('3', '6'),
('3', '9'),
('7', '11'),
('7', '12'),
('2', '12'),
('3', '8');

-- 5. Temporary_Employee 表（15条数据）
INSERT INTO Temporary_Employee (TempSsn, Company_name)
VALUES
('T200000001', '保洁服务有限公司'),
('T200000002', '维修服务外包公司'),
('T200000003', '绿化养护合作公司'),
('T200000004', '设备检测外包公司'),
('T200000005', '水电维修服务公司'),
('T200000006', '外墙清洁服务公司'),
('T200000007', '垃圾清运合作公司'),
('T200000008', '空调维护外包公司'),
('T200000009', '消防检查服务公司'),
('T200000010', '电梯维保外包公司'),
('T200000011', '管道疏通服务公司'),
('T200000012', '地毯清洁服务公司'),
('T200000013', '门窗维修外包公司'),
('T200000014', '灯具更换服务公司'),
('T200000015', '墙面翻新服务公司');

-- 6. TempSupervise 表（15条数据）- 修正 Ssn 引用
INSERT INTO TempSupervise (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
VALUES
('2', 'T200000001'),
('2', 'T200000002'),
('3', 'T200000003'),
('3', 'T200000004'),
('7', 'T200000005'),
('7', 'T200000006'),
('2', 'T200000007'),
('3', 'T200000008'),
('7', 'T200000009'),
('2', 'T200000010'),
('3', 'T200000011'),
('7', 'T200000012'),
('2', 'T200000013'),
('3', 'T200000014'),
('7', 'T200000015');

-- 7. Contractor_Company 表（15条数据）
INSERT INTO Contractor_Company (Temp_Employee_Ssn, name)
VALUES
('T200000001', '保洁服务有限公司'),
('T200000002', '维修服务外包公司'),
('T200000003', '绿化养护合作公司'),
('T200000004', '设备检测外包公司'),
('T200000005', '水电维修服务公司'),
('T200000006', '外墙清洁服务公司'),
('T200000007', '垃圾清运合作公司'),
('T200000008', '空调维护外包公司'),
('T200000009', '消防检查服务公司'),
('T200000010', '电梯维保外包公司'),
('T200000011', '管道疏通服务公司'),
('T200000012', '地毯清洁服务公司'),
('T200000013', '门窗维修外包公司'),
('T200000014', '灯具更换服务公司'),
('T200000015', '墙面翻新服务公司');

-- 8. Activity 表（15条数据）
INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum)
VALUES
('2025-11-20', 'daily campus cleaning', 1, 'Main_Building', 1, 101),
('2025-11-20', 'daily campus cleaning', 0, 'Main_Building', 1, 102),
('2025-11-21', 'campus ageing', 0, 'Tech_Building', 2, 204),
('2025-11-21', 'weather-related issues', 1, 'Admin_Building', 3, 308),
('2025-11-22', 'daily campus cleaning', 1, 'Main_Building', 2, 201),
('2025-11-22', 'campus ageing', 0, 'Tech_Building', 3, 305),
('2025-11-23', 'weather-related issues', 0, 'Service_Building', 1, 109),
('2025-11-23', 'daily campus cleaning', 1, 'Admin_Building', 1, 106),
('2025-11-24', 'campus ageing', 1, 'Main_Building', 3, 301),
('2025-11-24', 'daily campus cleaning', 0, 'Tech_Building', 1, 103),
('2025-11-25', 'weather-related issues', 1, 'Service_Building', 2, 210),
('2025-11-25', 'daily campus cleaning', 1, 'Main_Building', 1, 101),
('2025-11-26', 'campus ageing', 0, 'Admin_Building', 2, 207),
('2025-11-26', 'daily campus cleaning', 0, 'Tech_Building', 2, 204),
('2025-11-27', 'weather-related issues', 0, 'Main_Building', 2, 201);

-- 9. Mid_Level_Manage_Activity 表（15条数据）- 修正 Ssn 引用
INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
VALUES
('2', 'Main_Building', 1, 101, '2025-11-20'),
('2', 'Main_Building', 1, 102, '2025-11-20'),
('3', 'Tech_Building', 2, 204, '2025-11-21'),
('3', 'Admin_Building', 3, 308, '2025-11-21'),
('7', 'Main_Building', 2, 201, '2025-11-22'),
('7', 'Tech_Building', 3, 305, '2025-11-22'),
('2', 'Service_Building', 1, 109, '2025-11-23'),
('2', 'Admin_Building', 1, 106, '2025-11-23'),
('3', 'Main_Building', 3, 301, '2025-11-24'),
('3', 'Tech_Building', 1, 103, '2025-11-24'),
('7', 'Service_Building', 2, 210, '2025-11-25'),
('7', 'Main_Building', 1, 101, '2025-11-25'),
('2', 'Admin_Building', 2, 207, '2025-11-26'),
('2', 'Tech_Building', 2, 204, '2025-11-26'),
('3', 'Main_Building', 2, 201, '2025-11-27');

-- 10. Employee_Work_On 表（15条数据）- 修正 Ssn 引用
INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn)
VALUES
('2025-11-20', 'Main_Building', 1, 101, '4'),
('2025-11-20', 'Main_Building', 1, 102, '5'),
('2025-11-21', 'Tech_Building', 2, 204, '6'),
('2025-11-21', 'Admin_Building', 3, 308, '8'),
('2025-11-22', 'Main_Building', 2, 201, '9'),
('2025-11-22', 'Tech_Building', 3, 305, '11'),
('2025-11-23', 'Service_Building', 1, 109, '12'),
('2025-11-23', 'Admin_Building', 1, 106, '4'),
('2025-11-24', 'Main_Building', 3, 301, '5'),
('2025-11-24', 'Tech_Building', 1, 103, '6'),
('2025-11-25', 'Service_Building', 2, 210, '8'),
('2025-11-25', 'Main_Building', 1, 101, '9'),
('2025-11-26', 'Admin_Building', 2, 207, '11'),
('2025-11-26', 'Tech_Building', 2, 204, '12'),
('2025-11-27', 'Main_Building', 2, 201, '4');

-- 11. Temp_Employee_Work_On 表（15条数据）
INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
VALUES
('2025-11-20', 'Main_Building', 1, 101, 'T200000001'),
('2025-11-20', 'Main_Building', 1, 102, 'T200000002'),
('2025-11-21', 'Tech_Building', 2, 204, 'T200000003'),
('2025-11-21', 'Admin_Building', 3, 308, 'T200000004'),
('2025-11-22', 'Main_Building', 2, 201, 'T200000005'),
('2025-11-22', 'Tech_Building', 3, 305, 'T200000006'),
('2025-11-23', 'Service_Building', 1, 109, 'T200000007'),
('2025-11-23', 'Admin_Building', 1, 106, 'T200000008'),
('2025-11-24', 'Main_Building', 3, 301, 'T200000009'),
('2025-11-24', 'Tech_Building', 1, 103, 'T200000010'),
('2025-11-25', 'Service_Building', 2, 210, 'T200000011'),
('2025-11-25', 'Main_Building', 1, 101, 'T200000012'),
('2025-11-26', 'Admin_Building', 2, 207, 'T200000013'),
('2025-11-26', 'Tech_Building', 2, 204, 'T200000014'),
('2025-11-27', 'Main_Building', 2, 201, 'T200000015');

-- 12. Applied_To 表（15条数据）
INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason)
VALUES
('2025-11-20', 'Main_Building', 1, 101, '日常清洁需中性清洁剂申请'),
('2025-11-20', 'Main_Building', 1, 102, '维修工具借用申请（螺丝刀套装）'),
('2025-11-21', 'Tech_Building', 2, 204, '绿化肥料采购申请（有机营养液）'),
('2025-11-21', 'Admin_Building', 3, 308, '设备检测仪器租赁申请（温湿度计）'),
('2025-11-22', 'Main_Building', 2, 201, '水电维修材料申请（水管接头）'),
('2025-11-22', 'Tech_Building', 3, 305, '外墙清洁安全绳申请（高空作业）'),
('2025-11-23', 'Service_Building', 1, 109, '垃圾清运车辆调度申请（密闭式货车）'),
('2025-11-23', 'Admin_Building', 1, 106, '空调制冷剂补充申请（R410A）'),
('2025-11-24', 'Main_Building', 3, 301, '消防灭火器年检申请（ABC干粉型）'),
('2025-11-24', 'Tech_Building', 1, 103, '电梯维保配件申请（门机板）'),
('2025-11-25', 'Service_Building', 2, 210, '管道疏通药剂申请（生物酶制剂）'),
('2025-11-25', 'Main_Building', 1, 101, '地毯除渍剂申请（中性去污剂）'),
('2025-11-26', 'Admin_Building', 2, 207, '门窗密封条更换申请（硅胶条）'),
('2025-11-26', 'Tech_Building', 2, 204, 'LED灯具采购申请（3000K暖光）'),
('2025-11-27', 'Main_Building', 2, 201, '墙面翻新涂料申请（环保乳胶漆）');
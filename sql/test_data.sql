-- 切换到目标数据库（确保先执行 schema.sql 建表成功）
USE appdb;

-- 清空已有数据（避免重复插入报错，按外键依赖逆序删除）
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

-- 1. Location 表（12条数据）- 无外键依赖，优先插入
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

-- 2. Employee 表（12条数据）- 无外键依赖
INSERT INTO Employee (Ssn, Name, Emp_Level)
VALUES
('1000000001', '张三', 'executive officer'),  -- 高管
('1000000002', '李四', 'mid_level manager'),  -- 中层经理
('1000000003', '王五', 'mid_level manager'),  -- 中层经理
('1000000004', '赵六', 'base_level worker'),  -- 基层员工
('1000000005', '孙七', 'base_level worker'),  -- 基层员工
('1000000006', '周八', 'base_level worker'),  -- 基层员工
('1000000007', '吴九', 'mid_level manager'),  -- 中层经理
('1000000008', '郑十', 'base_level worker'),  -- 基层员工
('1000000009', '钱十一', 'base_level worker'),-- 基层员工
('1000000010', '冯十二', 'executive officer'),-- 高管
('1000000011', '陈十三', 'base_level worker'),-- 基层员工
('1000000012', '褚十四', 'base_level worker');-- 基层员工

-- 3. Office 表（12条数据）- 依赖 Location + Employee
INSERT INTO Office (OwnerSsn, Office_Building, Office_Floor, Office_RoomNum)
VALUES
('1000000001', 'Admin_Building', 3, 308),    -- 高管张三办公室
('1000000002', 'Main_Building', 1, 101),     -- 中层李四办公室
('1000000003', 'Tech_Building', 2, 204),     -- 中层王五办公室
('1000000007', 'Tech_Building', 3, 305),     -- 中层吴九办公室
('1000000010', 'Admin_Building', 2, 207),    -- 高管冯十二办公室
(NULL, 'Main_Building', 1, 102),               -- 无归属人办公室
(NULL, 'Main_Building', 2, 201),               -- 无归属人办公室
(NULL, 'Tech_Building', 1, 103),               -- 无归属人办公室
(NULL, 'Admin_Building', 1, 106),              -- 无归属人办公室
(NULL, 'Service_Building', 1, 109),            -- 无归属人办公室
('1000000002', 'Service_Building', 2, 210),  -- 中层李四备用办公室
('1000000003', 'Main_Building', 3, 301);     -- 中层王五备用办公室

-- 4. Employee_Supervision 表（15条数据）- 依赖 Employee
INSERT INTO Employee_Supervision (Supervisor_Ssn, Supervisee_Ssn)
VALUES
('1000000001', '1000000002'),  -- 高管张三 → 中层李四
('1000000001', '1000000003'),  -- 高管张三 → 中层王五
('1000000001', '1000000007'),  -- 高管张三 → 中层吴九
('1000000010', '1000000002'),  -- 高管冯十二 → 中层李四
('1000000010', '1000000003'),  -- 高管冯十二 → 中层王五
('1000000010', '1000000007'),  -- 高管冯十二 → 中层吴九
('1000000002', '1000000004'),  -- 中层李四 → 基层赵六
('1000000002', '1000000005'),  -- 中层李四 → 基层孙七
('1000000002', '1000000008'),  -- 中层李四 → 基层郑十
('1000000003', '1000000006'),  -- 中层王五 → 基层周八
('1000000003', '1000000009'),  -- 中层王五 → 基层钱十一
('1000000007', '1000000011'),  -- 中层吴九 → 基层陈十三
('1000000007', '1000000012'),  -- 中层吴九 → 基层褚十四
('1000000002', '1000000012'),  -- 中层李四 → 基层褚十四
('1000000003', '1000000008');  -- 中层王五 → 基层郑十

-- 5. Temporary_Employee 表（15条数据）- 无外键依赖
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

-- 6. TempSupervise 表（15条数据）- 依赖 Employee + Temporary_Employee
INSERT INTO TempSupervise (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee)
VALUES
('1000000002', 'T200000001'),  -- 中层李四 → 临时保洁
('1000000002', 'T200000002'),  -- 中层李四 → 临时维修
('1000000003', 'T200000003'),  -- 中层王五 → 临时绿化
('1000000003', 'T200000004'),  -- 中层王五 → 临时设备检测
('1000000007', 'T200000005'),  -- 中层吴九 → 临时水电维修
('1000000007', 'T200000006'),  -- 中层吴九 → 临时外墙清洁
('1000000002', 'T200000007'),  -- 中层李四 → 临时垃圾清运
('1000000003', 'T200000008'),  -- 中层王五 → 临时空调维护
('1000000007', 'T200000009'),  -- 中层吴九 → 临时消防检查
('1000000002', 'T200000010'),  -- 中层李四 → 临时电梯维保
('1000000003', 'T200000011'),  -- 中层王五 → 临时管道疏通
('1000000007', 'T200000012'),  -- 中层吴九 → 临时地毯清洁
('1000000002', 'T200000013'),  -- 中层李四 → 临时门窗维修
('1000000003', 'T200000014'),  -- 中层王五 → 临时灯具更换
('1000000007', 'T200000015');  -- 中层吴九 → 临时墙面翻新

-- 7. Contractor_Company 表（15条数据）- 依赖 Temporary_Employee
INSERT INTO Contractor_Company (Temp_Employee_Ssn, Company_name)
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

-- 8. Activity 表（15条数据）- 依赖 Location
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

-- 9. Mid_Level_Manage_Activity 表（15条数据）- 依赖 Employee + Activity
INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
VALUES
('1000000002', 'Main_Building', 1, 101, '2025-11-20'),
('1000000002', 'Main_Building', 1, 102, '2025-11-20'),
('1000000003', 'Tech_Building', 2, 204, '2025-11-21'),
('1000000003', 'Admin_Building', 3, 308, '2025-11-21'),
('1000000007', 'Main_Building', 2, 201, '2025-11-22'),
('1000000007', 'Tech_Building', 3, 305, '2025-11-22'),
('1000000002', 'Service_Building', 1, 109, '2025-11-23'),
('1000000002', 'Admin_Building', 1, 106, '2025-11-23'),
('1000000003', 'Main_Building', 3, 301, '2025-11-24'),
('1000000003', 'Tech_Building', 1, 103, '2025-11-24'),
('1000000007', 'Service_Building', 2, 210, '2025-11-25'),
('1000000007', 'Main_Building', 1, 101, '2025-11-25'),
('1000000002', 'Admin_Building', 2, 207, '2025-11-26'),
('1000000002', 'Tech_Building', 2, 204, '2025-11-26'),
('1000000003', 'Main_Building', 2, 201, '2025-11-27');

-- 10. Employee_Work_On 表（15条数据）- 依赖 Employee + Activity
INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn)
VALUES
('2025-11-20', 'Main_Building', 1, 101, '1000000004'),  -- 赵六 → 主楼101清洁
('2025-11-20', 'Main_Building', 1, 102, '1000000005'),  -- 孙七 → 主楼102清洁
('2025-11-21', 'Tech_Building', 2, 204, '1000000006'),  -- 周八 → 科技楼204老化维护
('2025-11-21', 'Admin_Building', 3, 308, '1000000008'),  -- 郑十 → 行政楼308天气维修
('2025-11-22', 'Main_Building', 2, 201, '1000000009'),  -- 钱十一 → 主楼201清洁
('2025-11-22', 'Tech_Building', 3, 305, '1000000011'),  -- 陈十三 → 科技楼305老化维护
('2025-11-23', 'Service_Building', 1, 109, '1000000012'),-- 褚十四 → 服务楼109天气维修
('2025-11-23', 'Admin_Building', 1, 106, '1000000004'),  -- 赵六 → 行政楼106清洁
('2025-11-24', 'Main_Building', 3, 301, '1000000005'),  -- 孙七 → 主楼301老化维护
('2025-11-24', 'Tech_Building', 1, 103, '1000000006'),  -- 周八 → 科技楼103清洁
('2025-11-25', 'Service_Building', 2, 210, '1000000008'),-- 郑十 → 服务楼210天气维修
('2025-11-25', 'Main_Building', 1, 101, '1000000009'),  -- 钱十一 → 主楼101清洁
('2025-11-26', 'Admin_Building', 2, 207, '1000000011'),  -- 陈十三 → 行政楼207清洁
('2025-11-26', 'Tech_Building', 2, 204, '1000000012'),  -- 褚十四 → 科技楼204清洁
('2025-11-27', 'Main_Building', 2, 201, '1000000004');  -- 赵六 → 主楼201天气维修

-- 11. Temp_Employee_Work_On 表（15条数据）- 依赖 Temporary_Employee + Activity
INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
VALUES
('2025-11-20', 'Main_Building', 1, 101, 'T200000001'),  -- 临时保洁 → 主楼101清洁
('2025-11-20', 'Main_Building', 1, 102, 'T200000002'),  -- 临时维修 → 主楼102维修
('2025-11-21', 'Tech_Building', 2, 204, 'T200000003'),  -- 临时绿化 → 科技楼204绿化
('2025-11-21', 'Admin_Building', 3, 308, 'T200000004'),  -- 临时设备检测 → 行政楼308检测
('2025-11-22', 'Main_Building', 2, 201, 'T200000005'),  -- 临时水电 → 主楼201水电维修
('2025-11-22', 'Tech_Building', 3, 305, 'T200000006'),  -- 临时外墙清洁 → 科技楼305外墙
('2025-11-23', 'Service_Building', 1, 109, 'T200000007'),-- 临时垃圾清运 → 服务楼109清运
('2025-11-23', 'Admin_Building', 1, 106, 'T200000008'),  -- 临时空调维护 → 行政楼106空调
('2025-11-24', 'Main_Building', 3, 301, 'T200000009'),  -- 临时消防检查 → 主楼301消防
('2025-11-24', 'Tech_Building', 1, 103, 'T200000010'),  -- 临时电梯维保 → 科技楼103电梯
('2025-11-25', 'Service_Building', 2, 210, 'T200000011'),-- 临时管道疏通 → 服务楼210管道
('2025-11-25', 'Main_Building', 1, 101, 'T200000012'),  -- 临时地毯清洁 → 主楼101地毯
('2025-11-26', 'Admin_Building', 2, 207, 'T200000013'),  -- 临时门窗维修 → 行政楼207门窗
('2025-11-26', 'Tech_Building', 2, 204, 'T200000014'),  -- 临时灯具更换 → 科技楼204灯具
('2025-11-27', 'Main_Building', 2, 201, 'T200000015');  -- 临时墙面翻新 → 主楼201墙面

-- 12. Applied_To 表（15条数据）- 依赖 Location + Activity
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

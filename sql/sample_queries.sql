USE appdb;

-- 1. 查询所有中层经理的姓名、工号及所属办公室信息（联表查询：Employee + Office）
-- 用途：快速获取中层管理人员的办公位置
SELECT 
  e.Ssn AS 经理工号,
  e.Name AS 经理姓名,
  o.Office_Building AS 办公楼,
  o.Office_Floor AS 楼层,
  o.Office_RoomNum AS 房间号
FROM Employee e
LEFT JOIN Office o ON e.Ssn = o.OwnerSsn  -- 左连接保留无办公室的经理
WHERE e.Emp_Level = 'mid_level manager'  -- 过滤中层经理
ORDER BY o.Office_Building, o.Office_Floor;

-- 2. 查询2025年11月20日-2025年11月25日期间的所有清洁活动（单表过滤+日期范围）
-- 用途：筛选特定时间段的目标类型活动
SELECT 
  Activity_Time AS 活动日期,
  Activity_Building AS 办公楼,
  Activity_Floor AS 楼层,
  Activity_RoomNum AS 房间号,
  Require_Chemical AS 是否需要化学用品（1=是/0=否）
FROM Activity
WHERE 
  Activity_Type = 'daily campus cleaning'  -- 只看清洁活动
  AND Activity_Time BETWEEN '2025-11-20' AND '2025-11-25'  -- 日期范围
ORDER BY Activity_Time, Activity_Building;

-- 3. 查询每个中层经理管理的活动数量（分组统计：Mid_Level_Manage_Activity + Employee）
-- 用途：统计管理人员的工作负载
SELECT 
  e.Name AS 经理姓名,
  e.Ssn AS 经理工号,
  COUNT(m.Manage_Activity_Time) AS 管理活动数量
FROM Mid_Level_Manage_Activity m
JOIN Employee e ON m.Manager_Ssn = e.Ssn  -- 关联经理信息
GROUP BY e.Ssn, e.Name  -- 按经理分组
ORDER BY 管理活动数量 DESC;  -- 按活动数量降序排列

-- 4. 查询参与「科技楼」2025年11月21日活动的所有正式员工姓名及工号（联表：Employee_Work_On + Employee）
-- 用途：定位特定活动的参与员工
SELECT 
  e.Ssn AS 员工工号,
  e.Name AS 员工姓名,
  w.Working_Building AS 办公楼,
  w.Working_Floor AS 楼层,
  w.Working_Room_number AS 房间号
FROM Employee_Work_On w
JOIN Employee e ON w.Working_Worker_Ssn = e.Ssn  -- 关联员工信息
WHERE 
  w.Working_Building = 'Tech_Building'  -- 限定科技楼
  AND w.Working_Time = '2025-11-21';  -- 限定日期

-- 5. 查询所有需要化学用品的活动及对应的申请理由（联表：Activity + Applied_To）
-- 用途：关联活动需求与申请记录
SELECT 
  a.Activity_Time AS 活动日期,
  a.Activity_Building AS 办公楼,
  a.Activity_Floor AS 楼层,
  a.Activity_RoomNum AS 房间号,
  a.Activity_Type AS 活动类型,
  t.Applied_Reason AS 申请理由
FROM Activity a
JOIN Applied_To t ON 
  a.Activity_Time = t.Applied_Time 
  AND a.Activity_Building = t.Applied_Building 
  AND a.Activity_Floor = t.Applied_Floor 
  AND a.Activity_RoomNum = t.Applied_Room_number  -- 多字段关联活动与申请
WHERE a.Require_Chemical = 1;  -- 只看需要化学用品的活动

-- 6. 查询每个外包公司的临时员工数量及对应的监督经理（多表联查：Temporary_Employee + TempSupervise + Employee）
-- 用途：统计外包公司规模及对应负责人
SELECT 
  te.Company_name AS 外包公司名称,
  COUNT(te.TempSsn) AS 临时员工数量,
  GROUP_CONCAT(DISTINCT e.Name SEPARATOR '、') AS 监督经理姓名  -- 合并多个经理
FROM Temporary_Employee te
JOIN TempSupervise ts ON te.TempSsn = ts.Supervisee_Ssn_temp_employee
JOIN Employee e ON ts.Supervisor_Ssn_midlevel_manager = e.Ssn
GROUP BY te.Company_name  -- 按外包公司分组
ORDER BY 临时员工数量 DESC;

-- 7. 查询无归属人的办公室分布（单表查询：Office）
-- 用途：统计闲置办公室资源
SELECT 
  Office_Building AS 办公楼,
  Office_Floor AS 楼层,
  COUNT(Office_RoomNum) AS 无归属人办公室数量
FROM Office
WHERE OwnerSsn IS NULL  -- 过滤无归属人的办公室
GROUP BY Office_Building, Office_Floor  -- 按办公楼+楼层分组
ORDER BY Office_Building, Office_Floor;

-- 8. 查询2025年11月参与「天气相关维修」的临时员工及所属公司（联表：Temp_Employee_Work_On + Temporary_Employee + Activity）
-- 用途：定位特定类型活动的临时参与人员
SELECT 
  te.TempSsn AS 临时员工工号,
  te.Company_name AS 所属外包公司,
  tww.Temp_Working_Time AS 工作日期,
  tww.Temp_Working_Building AS 办公楼,
  tww.Temp_Working_Floor AS 楼层
FROM Temp_Employee_Work_On tww
JOIN Temporary_Employee te ON tww.Temp_Working_Worker_Ssn = te.TempSsn
JOIN Activity a ON 
  tww.Temp_Working_Time = a.Activity_Time 
  AND tww.Temp_Working_Building = a.Activity_Building 
  AND tww.Temp_Working_Floor = a.Activity_Floor 
  AND tww.Temp_Working_Room_number = a.Activity_RoomNum
WHERE 
  a.Activity_Type = 'weather-related issues'  -- 限定天气相关维修
  AND a.Activity_Time LIKE '2025-11-%';  -- 限定2025年11月

-- 9. 查询每个正式员工的直接上级姓名及层级（联表：Employee_Supervision + Employee）
-- 用途：展示员工-上级的汇报关系
SELECT 
  s.Name AS 上级姓名,
  s.Emp_Level AS 上级层级,
  se.Name AS 下属姓名,
  se.Emp_Level AS 下属层级,
  se.Ssn AS 下属工号
FROM Employee_Supervision es
JOIN Employee s ON es.Supervisor_Ssn = s.Ssn  -- 关联上级信息
JOIN Employee se ON es.Supervisee_Ssn = se.Ssn  -- 关联下属信息
ORDER BY s.Emp_Level DESC, s.Name;  -- 按上级层级降序排列

-- 10. 查询行政楼（Admin_Building）所有房间的活动记录数（分组统计：Activity + Location）
-- 用途：统计特定楼宇的活动频次
SELECT 
  a.Activity_Building AS 办公楼,
  a.Activity_Floor AS 楼层,
  a.Activity_RoomNum AS 房间号,
  COUNT(a.Activity_Time) AS 活动记录数,
  GROUP_CONCAT(DISTINCT a.Activity_Type SEPARATOR '、') AS 涉及活动类型
FROM Activity a
JOIN Location l ON 
  a.Activity_Building = l.Building 
  AND a.Activity_Floor = l.Floor 
  AND a.Activity_RoomNum = l.Room_number
WHERE a.Activity_Building = 'Admin_Building'  -- 限定行政楼
GROUP BY a.Activity_Building, a.Activity_Floor, a.Activity_RoomNum
ORDER BY a.Activity_Floor, a.Activity_RoomNum;

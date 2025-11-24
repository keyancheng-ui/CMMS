# 2411project

## 数据库（本地 MySQL）

- 使用本机 MySQL（例如 Workbench/命令行），确保可以连接 `localhost:3306`
- 初始化最小表结构：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-bootstrap`
- 从 SQL 文件导入：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-init --schema sql/schema.sql --data sql/test_data.sql`

## Python CLI

- 安装依赖：`pip install -r requirements.txt`
- 运行：`python src/main.py list-employees`
- 打开 GUI：`python src/main.py gui`

## 目录结构

### 项目根
- `.env`：数据库连接配置（`MYSQL_HOST/PORT/USER/PASSWORD/DATABASE`），默认由程序读取，可被 CLI/GUI 参数覆盖
- `.gitignore`：忽略不应入库的文件（如 `.env`、`__pycache__/` 等）
- `requirements.txt`：Python 依赖（`mysql-connector-python`、`python-dotenv`）
- `README.md`：使用说明、命令参考与目录介绍

### sql
- `schema.sql`：MySQL 基础表结构（`employees`、`contractors`、`temp_employees`、`locations`、`activities`、`activity_employees`、`activity_contractors`）
- `test_data.sql`：示例数据（地点、员工、活动与人员分配）
- `sample_queries.sql`：示例查询（员工与活动统计）

### src
- `main.py`：程序入口
  - `python src/main.py gui` 启动图形界面
  - 不带 `gui` 时为命令行模式

- `db/` 数据访问与基础设施
  - `connection.py`：数据库连接与连接池；`get_connection()`、`get_connection_no_db()`、`ping()`
  - `validators.py`：通用校验（日期格式与系统创建日、非空校验、ID 不相等）
  - `employee_dao.py`：员工 CRUD、按 SSN 查询、设置监督关系
  - `contractor_dao.py`：承包商新增与查询
  - `temp_employee_dao.py`：临时员工新增与查询
  - `supervision_dao.py`：监督关系建立与查询下属
  - `location_dao.py`：地点查询与新增（`building/floor/room` 复合唯一）
  - `activity_dao.py`：新增活动（日期校验、同日同地冲突检查、化学品标记）、分配员工/承包商、筛选查询、完成标记、按员工列出活动
  - `report_dao.py`：员工活动汇总报表（基于 `activity_employees`）

- `logic/` 业务服务层
  - `employee_service.py`：员工业务封装
  - `activity_service.py`：活动业务封装
  - `report_service.py`：报表业务封装
  - `contractor_service.py`：承包商业务封装
  - `temp_employee_service.py`：临时员工业务封装
  - `location_service.py`：地点业务封装
  - `supervision_service.py`：监督关系业务封装

- `ui/` 用户界面
  - `cli.py`：命令行接口，支持全局连接参数（`--host --port --user --password --database`）与以下子命令：
    - `db-ping`、`db-bootstrap`、`db-init`
    - `list-employees`、`add-employee <ssn> <name> <gender> <level>`
    - `set-supervisor <employee_id> <supervisor_id>`、`list-subordinates <supervisor_id>`
    - `add-activity <manager_id> <location_id> <date> <type> <desc> [--requires_chemical]`
    - `assign-employee <activity_id> <employee_id>`、`assign-contractor <activity_id> <contractor_id>`
    - `list-activities <employee_id>`、`report-employee-activity`
    - 承包商：`list-contractors`、`add-contractor <ssn> <name> <company>`
    - 临时员工：`list-temp-employees`、`add-temp-employee <ssn> <name> <gender> <company_id> <supervisor_id>`
    - 地点：`list-locations`、`add-location <building> <floor> <room>`
    - 交互主菜单：`menu`
  - `gui.py`：Tkinter 图形界面，包含连接配置与七个功能页（员工、监督、活动、承包商、临时员工、地点、报表）

### docs
- `UserGuide.pdf`、`AnalysisReport.pdf`、`Presentation.pptx`：阶段性文档与展示占位

### demo
- `demo_video.mp4`：演示视频占位

## 运行方法

- 安装依赖：
  - `pip install -r requirements.txt`

- 初始化数据库（本地 MySQL，任选其一）：
  - 最小结构引导：
    - `python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-bootstrap`
  - 从 SQL 导入：
    - `python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-init --schema sql/schema.sql --data sql/test_data.sql`

- 运行命令行（全局连接参数需放在子命令之前）：
  - 列员工：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb list-employees`
  - 新增员工：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb add-employee 123456789 Alice F middle`
  - 建立监督：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb set-supervisor <emp_id> <sup_id>`
  - 新增活动：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb add-activity <manager_id> <location_id> 2025-11-24 cleaning "Lobby daily"`
  - 分配人员：`assign-employee <activity_id> <employee_id>`、`assign-contractor <activity_id> <contractor_id>`
  - 查询与报表：`list-activities <employee_id>`、`report-employee-activity`
  - 主菜单：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb menu`

- 启动图形界面：
  - `python src/main.py gui`
  - 顶部填写 `host/port/user/password/database`，点击 `Apply` 应用或 `Test` 测试连通性
  - 使用各标签页进行列表/新增/分配/监督/报表等操作

- 环境变量与覆盖：
  - `.env` 中的 `MYSQL_HOST/PORT/USER/PASSWORD/DATABASE` 会被程序读取
  - CLI 与 GUI 的连接参数可以覆盖 `.env` 的默认值

## 命令参考

### 交互式（自然语言）
- 启动：`python src/main.py`（按提示输入 `username/password/port`）
- 示例指令（不区分大小写）：
  - `List locations`
  - `List employees`
  - `List contractors`
  - `List activities 2`
  - `Add location Main 2 201`
  - `Add employee 123456789 Alice F middle`
  - `Set supervisor 2 1`
  - `Add contractor 999999999 ACME ACME`
  - `Add activity 3 1 2025-11-30 cleaning "Hall daily"`
  - `Assign employee 5 2`
  - `Assign contractor 5 1`
  - `Report employee activity`
  - `Exit` / `Quit`

### 参数化命令模式（可选）
- 全局连接参数（必须在子命令之前）：`--host <host>`、`--port <port>`、`--user <user>`、`--password <pass>`、`--database <db>`
- 初始化与测试：
  - `python src/main.py --host localhost --port 3306 --user <u> --password <p> --database appdb db-ping`
  - `python src/main.py --host localhost --port 3306 --user <u> --password <p> --database appdb db-bootstrap`
  - `python src/main.py --host localhost --port 3306 --user <u> --password <p> --database appdb db-init --schema sql/schema.sql --data sql/test_data.sql`
- 常用命令：
  - `list-employees`、`add-employee <ssn> <name> <gender> <level>`
  - `set-supervisor <employee_id> <supervisor_id>`、`list-subordinates <supervisor_id>`
  - `add-activity <manager_id> <location_id> <date> <type> <desc> [--requires_chemical]`
  - `assign-employee <activity_id> <employee_id>`、`assign-contractor <activity_id> <contractor_id>`
  - `list-activities <employee_id>`、`report-employee-activity`
  - `list-contractors`、`add-contractor <ssn> <name> <company>`
  - `list-temp-employees`、`add-temp-employee <ssn> <name> <gender> <company_id> <supervisor_id>`
  - `list-locations`、`add-location <building> <floor> <room>`
  - 主菜单：`python src/main.py --host ... --user ... --password ... --database ... menu`
  - 图形界面：`python src/main.py gui`

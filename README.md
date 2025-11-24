# 2411project

## 数据库（本地 MySQL）

- 使用本机 MySQL（例如 Workbench/命令行），确保可以连接 `localhost:3306`
- 初始化最小表结构：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-bootstrap`
- 从 SQL 文件导入：`python src/main.py --host localhost --port 3306 --user <user> --password <pass> --database appdb db-init --schema sql/schema.sql --data sql/test_data.sql`

## Python CLI

- 安装依赖：`pip install -r requirements.txt`
- 运行：`python src/main.py list-employees`

## 目录结构

- sql/: schema 与示例数据
- src/: 代码（db、logic、ui）
- sql/: 示例查询
- docs/: 文档占位
- demo/: 演示占位

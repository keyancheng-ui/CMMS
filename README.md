# 2411project

## 运行 Docker MySQL

- 在项目根执行：`"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" compose -f docker/docker-compose.yml up -d`
- 首次启动会导入 `docker/init/*.sql`

## Python CLI

- 安装依赖：`pip install -r requirements.txt`
- 运行：`python src/main.py list-employees`

## 目录结构

- docker/: Compose 与初始化 SQL
- src/: 代码（db、logic、ui）
- sql/: 示例查询
- docs/: 文档占位
- demo/: 演示占位

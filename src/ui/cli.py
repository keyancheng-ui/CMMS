import argparse
from db.connection import get_connection
from db.employee_dao import EmployeeDAO
from db.activity_dao import ActivityDAO
from db.report_dao import ReportDAO
from db.contractor_dao import ContractorDAO
from db.temp_employee_dao import TempEmployeeDAO
from db.location_dao import LocationDAO
from db.supervision_dao import SupervisionDAO
from logic.employee_service import EmployeeService
from logic.activity_service import ActivityService
from logic.report_service import ReportService
from logic.contractor_service import ContractorService
from logic.temp_employee_service import TempEmployeeService
from logic.location_service import LocationService
from logic.supervision_service import SupervisionService

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--database")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-employees")

    p_add_emp = sub.add_parser("add-employee")
    p_add_emp.add_argument("ssn")
    p_add_emp.add_argument("name")
    p_add_emp.add_argument("gender")
    p_add_emp.add_argument("level")

    p_set_sup = sub.add_parser("set-supervisor")
    p_set_sup.add_argument("employee_id", type=int)
    p_set_sup.add_argument("supervisor_id", type=int)

    p_list_sub = sub.add_parser("list-subordinates")
    p_list_sub.add_argument("supervisor_id", type=int)

    p_act = sub.add_parser("list-activities")
    p_act.add_argument("employee_id", type=int)

    p_add_act = sub.add_parser("add-activity")
    p_add_act.add_argument("manager_id", type=int)
    p_add_act.add_argument("location_id", type=int)
    p_add_act.add_argument("date")
    p_add_act.add_argument("activity_type")
    p_add_act.add_argument("description")
    p_add_act.add_argument("--requires_chemical", action="store_true")

    p_assign_emp = sub.add_parser("assign-employee")
    p_assign_emp.add_argument("activity_id", type=int)
    p_assign_emp.add_argument("employee_id", type=int)

    p_assign_con = sub.add_parser("assign-contractor")
    p_assign_con.add_argument("activity_id", type=int)
    p_assign_con.add_argument("contractor_id", type=int)

    p_list_con = sub.add_parser("list-contractors")
    p_add_con = sub.add_parser("add-contractor")
    p_add_con.add_argument("ssn")
    p_add_con.add_argument("name")
    p_add_con.add_argument("company")

    p_list_temp = sub.add_parser("list-temp-employees")
    p_add_temp = sub.add_parser("add-temp-employee")
    p_add_temp.add_argument("ssn")
    p_add_temp.add_argument("name")
    p_add_temp.add_argument("gender")
    p_add_temp.add_argument("company_id", type=int)
    p_add_temp.add_argument("supervisor_id", type=int)

    p_list_loc = sub.add_parser("list-locations")
    p_add_loc = sub.add_parser("add-location")
    p_add_loc.add_argument("building")
    p_add_loc.add_argument("floor")
    p_add_loc.add_argument("room")

    sub.add_parser("menu")

    sub.add_parser("report-employee-activity")
    sub.add_parser("db-ping")

    p_init = sub.add_parser("db-init")
    p_init.add_argument("--schema", default="sql/schema.sql")
    p_init.add_argument("--data", default="sql/test_data.sql")

    sub.add_parser("db-bootstrap")

    args = parser.parse_args()
    import os
    if args.host:
        os.environ["MYSQL_HOST"] = str(args.host)
    if args.port:
        os.environ["MYSQL_PORT"] = str(args.port)
    if args.user:
        os.environ["MYSQL_USER"] = str(args.user)
    if args.password:
        os.environ["MYSQL_PASSWORD"] = str(args.password)
    if args.database:
        os.environ["MYSQL_DATABASE"] = str(args.database)

    if args.cmd == "list-employees":
        conn = get_connection()
        svc = EmployeeService(EmployeeDAO(conn))
        rows = svc.list_all()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-employee":
        from db.validators import ensure_not_empty
        ensure_not_empty(args.ssn)
        conn = get_connection()
        dao = EmployeeDAO(conn)
        dao.add(args.ssn, args.name, args.gender, args.level)
        conn.close()
        print("OK")
    elif args.cmd == "set-supervisor":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        ssvc.set_supervision(args.employee_id, args.supervisor_id)
        conn.close()
        print("OK")
    elif args.cmd == "list-subordinates":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        rows = ssvc.list_subordinates(args.supervisor_id)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "list-activities":
        conn = get_connection()
        svc = ActivityService(ActivityDAO(conn))
        rows = svc.list_by_employee(args.employee_id)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-activity":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.add(args.manager_id, args.location_id, args.date, args.activity_type, args.description, args.requires_chemical)
        conn.close()
        print("OK")
    elif args.cmd == "assign-employee":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.assign_employee(args.activity_id, args.employee_id)
        conn.close()
        print("OK")
    elif args.cmd == "assign-contractor":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.assign_contractor(args.activity_id, args.contractor_id)
        conn.close()
        print("OK")
    elif args.cmd == "list-contractors":
        conn = get_connection()
        csvc = ContractorService(ContractorDAO(conn))
        rows = csvc.list_all()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-contractor":
        conn = get_connection()
        csvc = ContractorService(ContractorDAO(conn))
        csvc.add(args.ssn, args.name, args.company)
        conn.close()
        print("OK")
    elif args.cmd == "list-temp-employees":
        conn = get_connection()
        tsvc = TempEmployeeService(TempEmployeeDAO(conn))
        rows = tsvc.list_all()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-temp-employee":
        conn = get_connection()
        tsvc = TempEmployeeService(TempEmployeeDAO(conn))
        tsvc.add(args.ssn, args.name, args.gender, args.company_id, args.supervisor_id)
        conn.close()
        print("OK")
    elif args.cmd == "list-locations":
        conn = get_connection()
        lsvc = LocationService(LocationDAO(conn))
        rows = lsvc.list_all()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-location":
        conn = get_connection()
        lsvc = LocationService(LocationDAO(conn))
        lsvc.add(args.building, args.floor, args.room)
        conn.close()
        print("OK")
    elif args.cmd == "report-employee-activity":
        conn = get_connection()
        svc = ReportService(ReportDAO(conn))
        rows = svc.employee_activity_summary()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "db-ping":
        from db.connection import ping
        ping()
        print("OK")
    elif args.cmd == "db-init":
        from db.connection import get_connection_no_db
        conn = get_connection_no_db()
        cur = conn.cursor()
        dbname = os.getenv("MYSQL_DATABASE")
        if dbname:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
            cur.execute(f"USE `{dbname}`")
        for fp in [args.schema, args.data]:
            if not fp:
                continue
            with open(fp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            buf = []
            in_block = False
            for line in lines:
                t = line.strip()
                if not t:
                    continue
                if in_block:
                    if "*/" in t:
                        in_block = False
                    continue
                if t.startswith("/*"):
                    in_block = True
                    if "*/" in t:
                        in_block = False
                    continue
                if t.startswith("--"):
                    continue
                buf.append(t)
                if t.endswith(";"):
                    stmt = " ".join(buf).rstrip(";")
                    cur.execute(stmt)
                    buf = []
            if buf:
                stmt = " ".join(buf)
                if stmt:
                    cur.execute(stmt)
        conn.commit()
        cur.close()
        conn.close()
        print("OK")
    elif args.cmd == "menu":
        while True:
            print("1) list-employees")
            print("2) add-employee")
            print("3) set-supervisor")
            print("4) list-contractors")
            print("5) add-contractor")
            print("6) list-temp-employees")
            print("7) add-temp-employee")
            print("8) list-locations")
            print("9) add-location")
            print("10) add-activity")
            print("11) assign-employee")
            print("12) assign-contractor")
            print("13) list-activities")
            print("14) report-employee-activity")
            print("0) exit")
            sel = input().strip()
            if sel == "0":
                break
            if sel == "1":
                print("cmd: list-employees")
            elif sel == "2":
                ssn = input().strip(); name = input().strip(); gender = input().strip(); level = input().strip()
                conn = get_connection(); dao = EmployeeDAO(conn); dao.add(ssn, name, gender, level); conn.close(); print("OK")
            elif sel == "3":
                eid = int(input().strip()); sid = int(input().strip())
                conn = get_connection(); ssvc = SupervisionService(SupervisionDAO(conn)); ssvc.set_supervision(eid, sid); conn.close(); print("OK")
            elif sel == "4":
                conn = get_connection(); csvc = ContractorService(ContractorDAO(conn)); rows = csvc.list_all(); [print(r) for r in rows]; conn.close()
            elif sel == "5":
                ssn = input().strip(); name = input().strip(); company = input().strip()
                conn = get_connection(); csvc = ContractorService(ContractorDAO(conn)); csvc.add(ssn, name, company); conn.close(); print("OK")
            elif sel == "6":
                conn = get_connection(); tsvc = TempEmployeeService(TempEmployeeDAO(conn)); rows = tsvc.list_all(); [print(r) for r in rows]; conn.close()
            elif sel == "7":
                ssn = input().strip(); name = input().strip(); gender = input().strip(); cid = int(input().strip()); sid = int(input().strip())
                conn = get_connection(); tsvc = TempEmployeeService(TempEmployeeDAO(conn)); tsvc.add(ssn, name, gender, cid, sid); conn.close(); print("OK")
            elif sel == "8":
                conn = get_connection(); lsvc = LocationService(LocationDAO(conn)); rows = lsvc.list_all(); [print(r) for r in rows]; conn.close()
            elif sel == "9":
                building = input().strip(); floor = input().strip(); room = input().strip()
                conn = get_connection(); lsvc = LocationService(LocationDAO(conn)); lsvc.add(building, floor, room); conn.close(); print("OK")
            elif sel == "10":
                mid = int(input().strip()); lid = int(input().strip()); date = input().strip(); atype = input().strip(); desc = input().strip()
                conn = get_connection(); dao = ActivityDAO(conn); dao.add(mid, lid, date, atype, desc); conn.close(); print("OK")
            elif sel == "11":
                aid = int(input().strip()); eid = int(input().strip())
                conn = get_connection(); dao = ActivityDAO(conn); dao.assign_employee(aid, eid); conn.close(); print("OK")
            elif sel == "12":
                aid = int(input().strip()); cid = int(input().strip())
                conn = get_connection(); dao = ActivityDAO(conn); dao.assign_contractor(aid, cid); conn.close(); print("OK")
            elif sel == "13":
                eid = int(input().strip()); conn = get_connection(); svc = ActivityService(ActivityDAO(conn)); rows = svc.list_by_employee(eid); [print(r) for r in rows]; conn.close()
            elif sel == "14":
                conn = get_connection(); svc = ReportService(ReportDAO(conn)); rows = svc.employee_activity_summary(); [print(r) for r in rows]; conn.close()
    elif args.cmd == "db-bootstrap":
        from db.connection import get_connection_no_db
        dbname = os.getenv("MYSQL_DATABASE")
        conn = get_connection_no_db()
        cur = conn.cursor()
        if dbname:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}`")
            cur.execute(f"USE `{dbname}`")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
          id INT PRIMARY KEY AUTO_INCREMENT,
          ssn CHAR(9) NOT NULL UNIQUE,
          name VARCHAR(100) NOT NULL,
          gender VARCHAR(10),
          level VARCHAR(20),
          supervisor_id INT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS contractors (
          id INT PRIMARY KEY AUTO_INCREMENT,
          ssn CHAR(9) NOT NULL UNIQUE,
          name VARCHAR(100) NOT NULL,
          company VARCHAR(100) NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS temp_employees (
          id INT PRIMARY KEY AUTO_INCREMENT,
          ssn CHAR(9) NOT NULL UNIQUE,
          name VARCHAR(100) NOT NULL,
          gender VARCHAR(10),
          company_id INT,
          supervisor_id INT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
          id INT PRIMARY KEY AUTO_INCREMENT,
          building VARCHAR(100),
          floor VARCHAR(20),
          room VARCHAR(20),
          UNIQUE KEY uniq_loc (building, floor, room)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
          id INT PRIMARY KEY AUTO_INCREMENT,
          manager_id INT,
          location_id INT,
          activity_date DATE,
          activity_type VARCHAR(50),
          description VARCHAR(255),
          requires_chemical TINYINT DEFAULT 0,
          result VARCHAR(255),
          finish_time DATETIME
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_employees (
          activity_id INT,
          employee_id INT,
          PRIMARY KEY (activity_id, employee_id)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_contractors (
          activity_id INT,
          contractor_id INT,
          PRIMARY KEY (activity_id, contractor_id)
        )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("OK")

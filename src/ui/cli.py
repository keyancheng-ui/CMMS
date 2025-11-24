import argparse
import os
import shlex
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
    p_add_emp.add_argument("level")

    p_set_sup = sub.add_parser("set-supervisor")
    p_set_sup.add_argument("employee_ssn")
    p_set_sup.add_argument("supervisor_ssn")

    p_list_sub = sub.add_parser("list-subordinates")
    p_list_sub.add_argument("supervisor_ssn")

    p_act = sub.add_parser("list-activities")
    p_act.add_argument("employee_ssn")

    p_add_act = sub.add_parser("add-activity")
    p_add_act.add_argument("manager_id", type=int)
    p_add_act.add_argument("location_id", type=int)
    p_add_act.add_argument("date")
    p_add_act.add_argument("activity_type")
    p_add_act.add_argument("description")
    p_add_act.add_argument("--requires_chemical", action="store_true")

    p_assign_emp = sub.add_parser("assign-employee")
    p_assign_emp.add_argument("activity_id", type=int)
    p_assign_emp.add_argument("employee_ssn")

    p_assign_con = sub.add_parser("assign-contractor")
    p_assign_con.add_argument("activity_id", type=int)
    p_assign_con.add_argument("contractor_id", type=int)

    p_unassign_emp = sub.add_parser("unassign-employee")
    p_unassign_emp.add_argument("activity_id", type=int)
    p_unassign_emp.add_argument("employee_id", type=int)

    p_unassign_con = sub.add_parser("unassign-contractor")
    p_unassign_con.add_argument("activity_id", type=int)
    p_unassign_con.add_argument("contractor_id", type=int)

    p_assign_temp = sub.add_parser("assign-temp-employee")
    p_assign_temp.add_argument("activity_id", type=int)
    p_assign_temp.add_argument("temp_employee_ssn")

    p_del_emp = sub.add_parser("delete-employee")
    p_del_emp.add_argument("employee_ssn")

    p_upd_emp = sub.add_parser("update-employee")
    p_upd_emp.add_argument("employee_ssn")
    p_upd_emp.add_argument("--name")
    p_upd_emp.add_argument("--level")

    p_del_act = sub.add_parser("delete-activity")
    p_del_act.add_argument("activity_id", type=int)

    p_list_con = sub.add_parser("list-contractors")
    p_add_con = sub.add_parser("add-contractor-company")
    p_add_con.add_argument("name")

    p_set_temp_sup = sub.add_parser("set-temp-supervisor")
    p_set_temp_sup.add_argument("temp_employee_ssn")
    p_set_temp_sup.add_argument("supervisor_ssn")

    p_set_cc_sup = sub.add_parser("set-contractor-company-supervisor")
    p_set_cc_sup.add_argument("company_name")
    p_set_cc_sup.add_argument("supervisor_ssn")

    p_list_temp = sub.add_parser("list-temp-employees")
    p_add_temp = sub.add_parser("add-temp-employee")
    p_add_temp.add_argument("ssn")
    p_add_temp.add_argument("name")
    p_add_temp.add_argument("company")

    p_list_loc = sub.add_parser("list-locations")
    p_add_loc = sub.add_parser("add-location")
    p_add_loc.add_argument("building")
    p_add_loc.add_argument("floor")
    p_add_loc.add_argument("room")

    p_del_loc = sub.add_parser("delete-location")
    p_del_loc.add_argument("location_id", type=int)

    sub.add_parser("menu")
    p_sql = sub.add_parser("run-sql")
    p_sql.add_argument("sql")
    p_sqlf = sub.add_parser("run-sql-file")
    p_sqlf.add_argument("path")
    p_imp = sub.add_parser("import-csv")
    p_imp.add_argument("entity")
    p_imp.add_argument("path")
    p_clean = sub.add_parser("cleaning-schedule")
    p_clean.add_argument("building")
    p_clean.add_argument("start")
    p_clean.add_argument("end")

    sub.add_parser("report-employee-activity")
    p_rep_type = sub.add_parser("report-activity-type")
    p_rep_type.add_argument("start")
    p_rep_type.add_argument("end")
    p_rep_build = sub.add_parser("report-building-activity")
    p_rep_build.add_argument("building")
    p_rep_build.add_argument("start")
    p_rep_build.add_argument("end")
    p_rep_chem = sub.add_parser("report-chemical-usage")
    p_rep_chem.add_argument("building")
    p_rep_chem.add_argument("start")
    p_rep_chem.add_argument("end")
    sub.add_parser("db-ping")

    p_init = sub.add_parser("db-init")
    p_init.add_argument("--schema", default="sql/schema.sql")
    p_init.add_argument("--data", default="sql/test_data.sql")

    sub.add_parser("db-bootstrap")

    args = parser.parse_args()
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
        dao.add(args.ssn, args.name, args.level)
        conn.close()
        print("OK")
    elif args.cmd == "set-supervisor":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        ssvc.set_supervision(args.employee_ssn, args.supervisor_ssn)
        conn.close()
        print("OK")
    elif args.cmd == "list-subordinates":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        rows = ssvc.list_subordinates(args.supervisor_ssn)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "list-activities":
        conn = get_connection()
        svc = ActivityService(ActivityDAO(conn))
        rows = svc.list_by_employee(args.employee_ssn)
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
        dao.assign_employee(args.activity_id, args.employee_ssn)
        conn.close()
        print("OK")
    elif args.cmd == "assign-contractor":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.assign_contractor(args.activity_id, args.contractor_id)
        conn.close()
        print("OK")
    elif args.cmd == "unassign-employee":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.unassign_employee(args.activity_id, args.employee_id)
        conn.close()
        print("OK")
    elif args.cmd == "unassign-contractor":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.unassign_contractor(args.activity_id, args.contractor_id)
        conn.close()
        print("OK")
    elif args.cmd == "assign-temp-employee":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.assign_temp_employee(args.activity_id, args.temp_employee_ssn)
        conn.close()
        print("OK")
    elif args.cmd == "delete-employee":
        conn = get_connection()
        dao = EmployeeDAO(conn)
        dao.delete(args.employee_ssn)
        conn.close()
        print("OK")
    elif args.cmd == "update-employee":
        conn = get_connection()
        dao = EmployeeDAO(conn)
        dao.update(args.employee_ssn, name=args.name, level=args.level)
        conn.close()
        print("OK")
    elif args.cmd == "delete-activity":
        conn = get_connection()
        dao = ActivityDAO(conn)
        dao.delete(args.activity_id)
        conn.close()
        print("OK")
    elif args.cmd == "list-contractors":
        conn = get_connection()
        csvc = ContractorService(ContractorDAO(conn))
        rows = csvc.list_all()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "add-contractor-company":
        conn = get_connection()
        csvc = ContractorService(ContractorDAO(conn))
        csvc.add(args.name)
        conn.close()
        print("OK")
    elif args.cmd == "set-temp-supervisor":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        ssvc.set_temp_supervision(args.temp_employee_ssn, args.supervisor_ssn)
        conn.close()
        print("OK")
    elif args.cmd == "set-contractor-company-supervisor":
        conn = get_connection()
        ssvc = SupervisionService(SupervisionDAO(conn))
        ssvc.set_contractor_company_supervision(args.company_name, args.supervisor_ssn)
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
    elif args.cmd == "delete-location":
        conn = get_connection()
        lsvc = LocationService(LocationDAO(conn))
        lsvc.dao.delete(args.location_id)
        conn.close()
        print("OK")
    elif args.cmd == "report-employee-activity":
        conn = get_connection()
        svc = ReportService(ReportDAO(conn))
        rows = svc.employee_activity_summary()
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "report-activity-type":
        conn = get_connection()
        dao = ReportDAO(conn)
        rows = dao.activity_type_employee_count(args.start, args.end)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "report-building-activity":
        conn = get_connection()
        dao = ReportDAO(conn)
        rows = dao.building_activity_status(args.building, args.start, args.end)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "report-chemical-usage":
        conn = get_connection()
        dao = ReportDAO(conn)
        rows = dao.chemical_usage(args.building, args.start, args.end)
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
        import mysql.connector
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
                    try:
                        cur.execute(stmt)
                    except mysql.connector.Error as e:
                        if e.errno in (1060, 1061, 1022, 1826, 1833, 1062):
                            pass
                        else:
                            raise
                    buf = []
            if buf:
                stmt = " ".join(buf)
                if stmt:
                    try:
                        cur.execute(stmt)
                    except mysql.connector.Error as e:
                        if e.errno in (1060, 1061, 1022, 1826, 1833, 1062):
                            pass
                        else:
                            raise
        conn.commit()
        cur.close()
        conn.close()
        print("OK")
    elif args.cmd == "run-sql":
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(args.sql)
        try:
            rows = cur.fetchall()
            for r in rows:
                print(r)
        except Exception:
            pass
        cur.close(); conn.close()
        print("OK")
    elif args.cmd == "run-sql-file":
        conn = get_connection()
        cur = conn.cursor()
        with open(args.path, "r", encoding="utf-8") as f:
            sql = f.read()
        for stmt in sql.split(";"):
            s = stmt.strip()
            if not s:
                continue
            cur.execute(s)
        conn.commit(); cur.close(); conn.close(); print("OK")
    elif args.cmd == "import-csv":
        import csv
        conn = get_connection()
        if args.entity.lower() == "employees":
            dao = EmployeeDAO(conn)
            with open(args.path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dao.add(row.get("ssn"), row.get("name"), row.get("gender"), row.get("level"))
        elif args.entity.lower() == "locations":
            dao = LocationDAO(conn)
            with open(args.path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dao.add(row.get("building"), row.get("floor"), row.get("room"))
        conn.close(); print("OK")
    elif args.cmd == "cleaning-schedule":
        conn = get_connection()
        dao = ActivityDAO(conn)
        rows = dao.cleaning_schedule(args.building, args.start, args.end)
        for r in rows:
            print(r)
        conn.close()
    elif args.cmd == "menu":
        while True:
            print("1) list-employees")
            print("2) add-employee")
            print("3) set-supervisor")
            print("4) list-contractors")
            print("5) add-contractor-company")
            print("6) list-temp-employees")
            print("7) add-temp-employee")
            print("8) list-locations")
            print("9) add-location")
            print("10) add-activity")
            print("11) assign-employee")
            print("12) assign-contractor (deprecated)")
            print("13) list-activities")
            print("14) report-employee-activity")
            print("14b) report-activity-type")
            print("14c) report-building-activity")
            print("14d) report-chemical-usage")
            print("15) run-sql")
            print("16) import-csv")
            print("17) cleaning-schedule")
            print("18) update-employee")
            print("19) delete-employee")
            print("20) delete-location")
            print("21) delete-activity")
            print("22) unassign-employee")
            print("23) unassign-contractor")
            print("24) assign-temp-employee")
            print("25) set-temp-supervisor")
            print("26) set-contractor-company-supervisor")
            print("0) exit")
            sel = input().strip()
            if sel == "0":
                break
            if sel == "1":
                print("cmd: list-employees")
            elif sel == "2":
                ssn = input().strip(); name = input().strip(); level = input().strip()
                conn = get_connection(); dao = EmployeeDAO(conn); dao.add(ssn, name, level); conn.close(); print("OK")
            elif sel == "3":
                essn = input().strip(); sssn = input().strip()
                conn = get_connection(); ssvc = SupervisionService(SupervisionDAO(conn)); ssvc.set_supervision(essn, sssn); conn.close(); print("OK")
            elif sel == "4":
                conn = get_connection(); csvc = ContractorService(ContractorDAO(conn)); rows = csvc.list_all(); [print(r) for r in rows]; conn.close()
            elif sel == "5":
                name = input().strip()
                conn = get_connection(); csvc = ContractorService(ContractorDAO(conn)); csvc.add(name); conn.close(); print("OK")
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
                print("Deprecated: contractor assignments removed")
            elif sel == "13":
                essn = input().strip(); conn = get_connection(); svc = ActivityService(ActivityDAO(conn)); rows = svc.list_by_employee(essn); [print(r) for r in rows]; conn.close()
            elif sel == "14":
                conn = get_connection(); svc = ReportService(ReportDAO(conn)); rows = svc.employee_activity_summary(); [print(r) for r in rows]; conn.close()
            elif sel == "14b":
                st = input().strip(); ed = input().strip(); conn = get_connection(); dao = ReportDAO(conn); rows = dao.activity_type_employee_count(st, ed); [print(r) for r in rows]; conn.close()
            elif sel == "14c":
                b = input().strip(); st = input().strip(); ed = input().strip(); conn = get_connection(); dao = ReportDAO(conn); rows = dao.building_activity_status(b, st, ed); [print(r) for r in rows]; conn.close()
            elif sel == "14d":
                b = input().strip(); st = input().strip(); ed = input().strip(); conn = get_connection(); dao = ReportDAO(conn); rows = dao.chemical_usage(b, st, ed); [print(r) for r in rows]; conn.close()
            elif sel == "15":
                s = input().strip(); conn = get_connection(); cur = conn.cursor(dictionary=True); cur.execute(s); 
                try:
                    rows = cur.fetchall(); [print(r) for r in rows]
                except Exception:
                    pass
                cur.close(); conn.close(); print("OK")
            elif sel == "16":
                e = input().strip(); pth = input().strip(); import csv; conn = get_connection(); 
                if e.lower() == "employees":
                    dao = EmployeeDAO(conn); 
                    with open(pth, newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            dao.add(row.get("ssn"), row.get("name"), row.get("gender"), row.get("level"))
                elif e.lower() == "locations":
                    dao = LocationDAO(conn);
                    with open(pth, newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            dao.add(row.get("building"), row.get("floor"), row.get("room"))
                conn.close(); print("OK")
            elif sel == "17":
                b = input().strip(); st = input().strip(); ed = input().strip(); conn = get_connection(); dao = ActivityDAO(conn); rows = dao.cleaning_schedule(b, st, ed); [print(r) for r in rows]; conn.close()
            elif sel == "18":
                essn = input().strip(); name = input().strip(); level = input().strip(); conn = get_connection(); dao = EmployeeDAO(conn); dao.update(essn, name=name or None, level=level or None); conn.close(); print("OK")
            elif sel == "19":
                essn = input().strip(); conn = get_connection(); dao = EmployeeDAO(conn); dao.delete(essn); conn.close(); print("OK")
            elif sel == "20":
                lid = int(input().strip()); conn = get_connection(); LocationService(LocationDAO(conn)).dao.delete(lid); conn.close(); print("OK")
            elif sel == "21":
                aid = int(input().strip()); conn = get_connection(); ActivityDAO(conn).delete(aid); conn.close(); print("OK")
            elif sel == "22":
                aid = int(input().strip()); essn = input().strip(); conn = get_connection(); ActivityDAO(conn).unassign_employee(aid, essn); conn.close(); print("OK")
            elif sel == "23":
                aid = int(input().strip()); cid = int(input().strip()); conn = get_connection(); ActivityDAO(conn).unassign_contractor(aid, cid); conn.close(); print("OK")
            elif sel == "24":
                aid = int(input().strip()); tssn = input().strip(); conn = get_connection(); ActivityDAO(conn).assign_temp_employee(aid, tssn); conn.close(); print("OK")
            elif sel == "25":
                tssn = input().strip(); sssn = input().strip(); conn = get_connection(); SupervisionService(SupervisionDAO(conn)).set_temp_supervision(tssn, sssn); conn.close(); print("OK")
            elif sel == "26":
                cname = input().strip(); sssn = input().strip(); conn = get_connection(); SupervisionService(SupervisionDAO(conn)).set_contractor_company_supervision(cname, sssn); conn.close(); print("OK")
    elif args.cmd is None:
        def set_env(k, v):
            if v is not None and str(v).strip() != "":
                os.environ[k] = str(v)
        print("Enter username:")
        u = input().strip()
        print("Enter password:")
        p = input().strip()
        print("Enter port (default 3306):")
        pp = input().strip()
        set_env("MYSQL_USER", u)
        set_env("MYSQL_PASSWORD", p)
        set_env("MYSQL_PORT", pp if pp else "3306")
        set_env("MYSQL_HOST", os.getenv("MYSQL_HOST", "localhost"))
        set_env("MYSQL_DATABASE", os.getenv("MYSQL_DATABASE", "appdb"))
        print("Ready. Type commands like: 'List locations', 'Add employee <ssn> <name> <gender> <level>', 'Exit'")
        while True:
            line = input().strip()
            if not line:
                continue
            cmd = line.strip()
            low = cmd.lower()
            if low in ("exit", "quit"):
                break
            toks = shlex.split(cmd)
            ltoks = [t.lower() for t in toks]
            if len(ltoks) >= 2 and ltoks[0] == "list" and ltoks[1] == "locations":
                conn = get_connection(); lsvc = LocationService(LocationDAO(conn)); rows = lsvc.list_all(); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 2 and ltoks[0] == "list" and ltoks[1] == "employees":
                conn = get_connection(); esvc = EmployeeService(EmployeeDAO(conn)); rows = esvc.list_all(); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 2 and ltoks[0] == "list" and ltoks[1] == "contractors":
                conn = get_connection(); csvc = ContractorService(ContractorDAO(conn)); rows = csvc.list_all(); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 3 and ltoks[0] == "list" and ltoks[1] == "activities":
                essn = ltoks[2]; conn = get_connection(); asvc = ActivityService(ActivityDAO(conn)); rows = asvc.list_by_employee(essn); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 5 and ltoks[0] == "add" and ltoks[1] == "employee":
                ssn = toks[2]; name = toks[3]; gender = toks[4]; level = toks[5] if len(toks) > 5 else "basic"; conn = get_connection(); dao = EmployeeDAO(conn); dao.add(ssn, name, gender, level); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "set" and ltoks[1] == "supervisor":
                eid = int(toks[2]); sid = int(toks[3]); conn = get_connection(); ssvc = SupervisionService(SupervisionDAO(conn)); ssvc.set_supervision(eid, sid); conn.close(); print("OK"); continue
            if len(ltoks) >= 5 and ltoks[0] == "add" and ltoks[1] == "location":
                b = toks[2]; f = toks[3]; r = toks[4]; conn = get_connection(); lsvc = LocationService(LocationDAO(conn)); lsvc.add(b, f, r); conn.close(); print("OK"); continue
            if len(ltoks) >= 3 and ltoks[0] == "delete" and ltoks[1] == "location":
                lid = int(toks[2]); conn = get_connection(); LocationService(LocationDAO(conn)).dao.delete(lid); conn.close(); print("OK"); continue
            if len(ltoks) >= 6 and ltoks[0] == "add" and ltoks[1] == "activity":
                mid = int(toks[2]); lid = int(toks[3]); date = toks[4]; atype = toks[5]; desc = " ".join(toks[6:]) if len(toks) > 6 else ""; conn = get_connection(); dao = ActivityDAO(conn); dao.add(mid, lid, date, atype, desc); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "assign" and ltoks[1] == "employee":
                aid = int(toks[2]); essn = toks[3]; conn = get_connection(); dao = ActivityDAO(conn); dao.assign_employee(aid, essn); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "assign" and ltoks[1] == "contractor":
                aid = int(toks[2]); cid = int(toks[3]); conn = get_connection(); dao = ActivityDAO(conn); dao.assign_contractor(aid, cid); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "assign" and ltoks[1] == "temp" and ltoks[2] == "employee":
                aid = int(toks[3]); tid = int(toks[4]); conn = get_connection(); dao = ActivityDAO(conn); dao.assign_temp_employee(aid, tid); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "unassign" and ltoks[1] == "employee":
                aid = int(toks[2]); essn = toks[3]; conn = get_connection(); dao = ActivityDAO(conn); dao.unassign_employee(aid, essn); conn.close(); print("OK"); continue
            if len(ltoks) >= 4 and ltoks[0] == "unassign" and ltoks[1] == "contractor":
                aid = int(toks[2]); cid = int(toks[3]); conn = get_connection(); dao = ActivityDAO(conn); dao.unassign_contractor(aid, cid); conn.close(); print("OK"); continue
            if len(ltoks) >= 3 and ltoks[0] == "delete" and ltoks[1] == "employee":
                essn = toks[2]; conn = get_connection(); dao = EmployeeDAO(conn); dao.delete(essn); conn.close(); print("OK"); continue
            if len(ltoks) >= 3 and ltoks[0] == "delete" and ltoks[1] == "activity":
                aid = int(toks[2]); conn = get_connection(); ActivityDAO(conn).delete(aid); conn.close(); print("OK"); continue
            if len(ltoks) >= 3 and ltoks[0] == "update" and ltoks[1] == "employee":
                essn = toks[2]; fields = {}
                for tok in toks[3:]:
                    if "=" in tok:
                        k,v = tok.split("=",1); fields[k]=v
                conn = get_connection(); dao = EmployeeDAO(conn); dao.update(essn, name=fields.get("name"), level=fields.get("level")); conn.close(); print("OK"); continue
            if low in ("report employee activity", "employee activity report"):
                conn = get_connection(); rsvc = ReportService(ReportDAO(conn)); rows = rsvc.employee_activity_summary(); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 4 and ltoks[0] == "report" and ltoks[1] == "activity" and ltoks[2] == "type":
                st = toks[3]; ed = toks[4] if len(toks)>4 else st; conn = get_connection(); dao = ReportDAO(conn); rows = dao.activity_type_employee_count(st, ed); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 5 and ltoks[0] == "report" and ltoks[1] == "building" and ltoks[2] == "activity":
                b = toks[3]; st = toks[4]; ed = toks[5] if len(toks)>5 else st; conn = get_connection(); dao = ReportDAO(conn); rows = dao.building_activity_status(b, st, ed); [print(r) for r in rows]; conn.close(); continue
            if len(ltoks) >= 5 and ltoks[0] == "report" and ltoks[1] == "chemical" and ltoks[2] == "usage":
                b = toks[3]; st = toks[4]; ed = toks[5] if len(toks)>5 else st; conn = get_connection(); dao = ReportDAO(conn); rows = dao.chemical_usage(b, st, ed); [print(r) for r in rows]; conn.close(); continue
            print("Unknown command")
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
          ssn CHAR(9) PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          level VARCHAR(20),
          supervisor_ssn CHAR(9) NULL,
          supervisee_ssn CHAR(9) NULL,
          office_location_id INT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS contractor_companies (
          name VARCHAR(100) PRIMARY KEY
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS temp_employees (
          TempSsn CHAR(9) PRIMARY KEY,
          name VARCHAR(100) NOT NULL,
          company VARCHAR(100) NOT NULL
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
          employee_ssn CHAR(9),
          PRIMARY KEY (activity_id, employee_ssn)
        )
        """)
        # contractors removed
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_temp_employees (
          activity_id INT,
          temp_employee_ssn CHAR(9),
          PRIMARY KEY (activity_id, temp_employee_ssn)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supervise (
          employee_id CHAR(9) NOT NULL,
          supervisor_id CHAR(9) NOT NULL,
          PRIMARY KEY (employee_id, supervisor_id),
          UNIQUE KEY uniq_employee (employee_id)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supervise_temp_employees (
          temp_employee_ssn CHAR(9) NOT NULL,
          supervisor_ssn CHAR(9) NOT NULL,
          PRIMARY KEY (temp_employee_ssn, supervisor_ssn),
          UNIQUE KEY uniq_temp (temp_employee_ssn)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS supervise_contractor_companies (
          company_name VARCHAR(100) NOT NULL,
          supervisor_ssn CHAR(9) NOT NULL,
          PRIMARY KEY (company_name, supervisor_ssn),
          UNIQUE KEY uniq_company (company_name)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS dependents (
          id INT PRIMARY KEY AUTO_INCREMENT,
          employee_id CHAR(9) NOT NULL UNIQUE,
          name VARCHAR(100) NOT NULL,
          relationship VARCHAR(50)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_locations (
          activity_id INT NOT NULL,
          location_id INT NOT NULL,
          reason VARCHAR(255) NOT NULL,
          PRIMARY KEY (activity_id, location_id)
        )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("OK")

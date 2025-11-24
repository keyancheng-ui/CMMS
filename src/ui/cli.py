import argparse
from db.connection import get_connection
from db.employee_dao import EmployeeDAO
from db.activity_dao import ActivityDAO
from db.report_dao import ReportDAO
from logic.employee_service import EmployeeService
from logic.activity_service import ActivityService
from logic.report_service import ReportService

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-employees")

    p_act = sub.add_parser("list-activities")
    p_act.add_argument("employee_id", type=int)

    sub.add_parser("report-employee-activity")

    args = parser.parse_args()
    conn = get_connection()

    if args.cmd == "list-employees":
        svc = EmployeeService(EmployeeDAO(conn))
        rows = svc.list_all()
        for r in rows:
            print(r)
    elif args.cmd == "list-activities":
        svc = ActivityService(ActivityDAO(conn))
        rows = svc.list_by_employee(args.employee_id)
        for r in rows:
            print(r)
    elif args.cmd == "report-employee-activity":
        svc = ReportService(ReportDAO(conn))
        rows = svc.employee_activity_summary()
        for r in rows:
            print(r)
    conn.close()

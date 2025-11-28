from db import initialize_database
from logic.employee_service import EmployeeService

def main():
    print("start to initialize database...")

    # use all default values
    initialize_database(password=input("Input your own mySQL password: "))

    print("database initialization finished")
    print("the system is now ready for use")

    employee_service = EmployeeService()
    employee_service.get_current_employee()
    employee_service.employee_fire(1000000013)
    employee_service.employee_fire(1000000012)
    employee_service.get_current_employee()
    employee_service.close()

if __name__ == "__main__":
    main()

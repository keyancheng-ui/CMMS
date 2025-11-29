from db import initialize_database

from logic.employee_service import EmployeeService
from logic.supervision_service import SupervisionService


def main():
    print("start to initialize database...")
    password = input("Input your own mySQL password: ")

    # use all default values
    initialize_database(password = password)

    print("database initialization finished")
    print("the system is now ready for use")

    supervision_service = EmployeeService(password)
    supervision_service.get_current_employee()
    supervision_service.register_employee(1000000013, 'Jen', 'mid_level manager')
    supervision_service.get_current_employee()
    supervision_service.close()

if __name__ == "__main__":
    main()

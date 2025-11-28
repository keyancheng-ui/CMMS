from db import initialize_database

from logic.employee_service import EmployeeService
from logic.supervision_service import SupervisionService

def main():
    print("start to initialize database...")

    # use all default values
    initialize_database(password=input("Input your own mySQL password: "))

    print("database initialization finished")
    print("the system is now ready for use")






if __name__ == "__main__":
    main()

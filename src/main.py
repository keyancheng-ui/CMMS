from db import initialize_database

from logic.employee_service import EmployeeService
from logic.supervision_service import SupervisionService

def main():
    print("start to initialize database...")

    # use all default values
    initialize_database(password=input("Input your own mySQL password: "))

    print("database initialization finished")
    print("the system is now ready for use")


    supervision_service = SupervisionService()
    supervision_service.list_supervision(1000000001)
    supervision_service.delete_supervision(1000000001, 1000000002)
    supervision_service.list_supervision(1000000001)
    supervision_service.close()

if __name__ == "__main__":
    main()

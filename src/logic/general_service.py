from src.db.quick_query_dao import QuickQueryDAO

class Service:
    def __init__(self, password):
        self.quick_query = QuickQueryDAO(password)

    def get_activity(self, activity_time, activity_building, activity_floor, activity_room_num):

        return self.quick_query.get_activity(activity_time, activity_building, activity_floor, activity_room_num)


    def create_activity(self, activity_time, activity_type, require_chemical, activity_building, activity_floor,activity_room_num):

        return self.quick_query.create_activity(activity_time, activity_type, require_chemical, activity_building,activity_floor, activity_room_num)


    def get_all_activities(self):

        return self.quick_query.get_all_activities()


    def assign_manager_to_activity(self, manager_ssn, activity_time, activity_building, activity_floor, activity_room_num):

        return self.quick_query.assign_manager_to_activity(manager_ssn, activity_time, activity_building, activity_floor,activity_room_num)


    def assign_employee_to_activity(self, working_time, working_building, working_floor, working_room_number,working_worker_ssn):

        return self.quick_query.assign_employee_to_activity(working_time, working_building, working_floor, working_room_number, working_worker_ssn)


    def assign_temp_employee_to_activity(self, temp_working_time, temp_working_building, temp_working_floor,temp_working_room_number, temp_working_worker_ssn):

        return self.quick_query.assign_temp_employee_to_activity(temp_working_time, temp_working_building,temp_working_floor, temp_working_room_number,temp_working_worker_ssn)


    def create_applied_to(self, applied_time, applied_building, applied_floor, applied_room_number, applied_reason):

        return self.quick_query.create_applied_to(applied_time, applied_building, applied_floor, applied_room_number,applied_reason)


    def remove_manager_from_activity(self, manager_ssn, activity_time, activity_building, activity_floor,activity_room_num):

        return self.quick_query.remove_manager_from_activity(manager_ssn, activity_time, activity_building, activity_floor,activity_room_num)


    def remove_employee_from_activity(self, working_time, working_building, working_floor, working_room_number,working_worker_ssn):

        return self.quick_query.remove_employee_from_activity(working_time, working_building, working_floor,working_room_number, working_worker_ssn)


    def remove_temp_employee_from_activity(self, temp_working_time, temp_working_building, temp_working_floor,temp_working_room_number, temp_working_worker_ssn):

        return self.quick_query.remove_temp_employee_from_activity(temp_working_time, temp_working_building,temp_working_floor, temp_working_room_number,temp_working_worker_ssn)



    #about temporary employee


    def create_temp_employee_with_company(self, temp_ssn, company_name, contractor_company_name):
        return self.quick_query.create_temp_employee_with_company(temp_ssn, company_name, contractor_company_name)


    def get_temp_employee_with_company(self, temp_ssn):
        return self.quick_query.get_temp_employee_with_company(temp_ssn)

    def get_temp_employee_by_ssn(self, temp_ssn):
        return self.quick_query.get_temp_employee_by_ssn(temp_ssn)

    def get_all_temp_employees(self):
        return self.quick_query.get_all_temp_employees()

    def get_all_temp_employees_with_companies(self):
        return self.quick_query.get_all_temp_employees_with_companies()

    def delete_temp_employee(self, temp_ssn):
        return self.quick_query.delete_temp_employee(temp_ssn)

    def update_contractor_company(self, temp_employee_ssn, new_company_name):
        return self.quick_query.update_contractor_company(temp_employee_ssn, new_company_name)

    #about supervision

    def set_supervision(self, employee_ssn, supervisor_ssn):
        return self.quick_query.set_supervision(employee_ssn, supervisor_ssn)

    def list_supervision(self, ssn):
        return self.quick_query.list_supervision(ssn)

    def delete_supervision(self, supervisor_ssn, supervisee_ssn):
        return self.quick_query.delete_supervision(supervisor_ssn, supervisee_ssn)

    def set_temp_supervision(self, temp_employee_ssn, supervisor_ssn):
        return self.quick_query.set_temp_supervision(temp_employee_ssn, supervisor_ssn)

    def list_temp_supervision(self, supervisee_ssn):
        return self.quick_query.list_temp_supervision(supervisee_ssn)

    def delete_temp_supervision(self, temp_supervisee_ssn):
        return self.quick_query.delete_temp_supervision(temp_supervisee_ssn)

    #about report

    def get_mid_level_managers(self):
        return self.quick_query.get_mid_level_managers()

    def get_activities_by_date_range(self, start_date, end_date):
        return self.quick_query.get_activities_by_date_range(start_date, end_date)

    def get_manager_activity_counts(self,manager_ssn):
        return self.quick_query.get_manager_activity_counts(manager_ssn)

    def get_employees_in_certain_building(self, activity_date, building):
        return self.quick_query.get_employees_in_certain_building(activity_date, building)

    def get_contractor_employee_counts(self):
        return self.quick_query.get_contractor_employee_counts()


    #about location

    def create_location(self, building, floor, room_number):
        return self.quick_query.create_location(building, floor, room_number)

    def check_location(self, building, floor, room_number):
        return self.quick_query.check_location(building, floor, room_number)

    def get_all_locations(self):
        return self.quick_query.get_all_locations()

    def get_locations_by_building(self, building):
        return self.quick_query.get_locations_by_building(building)

    def get_vacant_offices(self):
        return self.quick_query.get_vacant_offices()

    def assign_office_to_employee(self, building, floor, room_number, owner_ssn):
        return self.quick_query.assign_office_to_employee(building, floor, room_number, owner_ssn)

    def vacate_office(self, building, floor, room_number):
        return self.quick_query.vacate_office(building, floor, room_number)

    #about employee

    def get_all_employees(self):
        return self.quick_query.get_all_employees()

    def get_employee_by_ssn(self, ssn):
        return self.quick_query.get_employee_by_ssn(ssn)

    def add_employee(self, ssn, name, emp_level):
        return self.quick_query.add_employee( ssn, name, emp_level)

    def get_employees_by_level(self, level):
        return self.quick_query.get_employees_by_level(level)

    def update_employee(self, ssn, new_level):
        return self.quick_query.update_employee(ssn, new_level)

    def delete_employee(self, ssn):
        return self.quick_query.delete_employee( ssn)

    #free sql

    def execute_custom_sql(self, sql_statement):
        return self.quick_query.execute_custom_sql(sql_statement)
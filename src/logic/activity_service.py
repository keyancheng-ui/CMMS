from src.db.activity_dao import ActivityDAO

class ActivityService:
    def __init__(self, password):
        self.activity_dao = ActivityDAO(password)

    def get_activity(self, activity_time, activity_building, activity_floor, activity_room_num):
        return self.activity_dao.get_activity(activity_time, activity_building, activity_floor, activity_room_num)

    def create_activity(self, activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num):
        return self.activity_dao.create_activity(activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num)

    def get_all_activities(self):
        return self.activity_dao.get_all_activities()

    def assign_manager_to_activity(self, manager_ssn, activity_time, activity_building, activity_floor,activity_room_num):
        return self.activity_dao.assign_manager_to_activity(manager_ssn, activity_time, activity_building, activity_floor,activity_room_num)

    def assign_employee_to_activity(self, working_time, working_building, working_floor, working_room_number, working_worker_ssn):
        return self.activity_dao.assign_employee_to_activity(working_time, working_building, working_floor, working_room_number,working_worker_ssn)

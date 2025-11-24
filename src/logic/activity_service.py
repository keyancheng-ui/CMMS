class ActivityService:
    def __init__(self, activity_dao):
        self.activity_dao = activity_dao

    def list_by_employee(self, employee_id):
        return self.activity_dao.list_by_employee(employee_id)

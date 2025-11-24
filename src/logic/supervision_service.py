class SupervisionService:
    def __init__(self, dao):
        self.dao = dao

    def set_supervision(self, employee_id, supervisor_id):
        return self.dao.set_supervision(employee_id, supervisor_id)

    def list_subordinates(self, supervisor_id):
        return self.dao.list_subordinates(supervisor_id)

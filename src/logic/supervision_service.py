from src.db.supervision_dao import SupervisionDAO


class SupervisionService:
    def __init__(self):
        self.supervision_dao = SupervisionDAO()

    def set_supervision(self, employee_id, supervisor_id):
        return self.dao.set_supervision(employee_id, supervisor_id)

    def list_supervision(self, supervisor_id):
        self.supervision_dao.list_supervision(supervisor_id)
    # finished

    def delete_supervision(self, supervisor_id, supervisee_id):
        self.supervision_dao.delete_supervision(supervisor_id, supervisee_id)


    def set_temp_supervision(self, temp_ssn, supervisor_ssn):
        return self.dao.set_temp_supervision(temp_ssn, supervisor_ssn)

    def list_temp_subordinates(self, supervisor_ssn):
        return self.dao.list_temp_subordinates(supervisor_ssn)

    def set_contractor_company_supervision(self, company_name, supervisor_ssn):
        return self.dao.set_contractor_company_supervision(company_name, supervisor_ssn)

    def list_contractor_company_subordinates(self, supervisor_ssn):
        return self.dao.list_contractor_company_subordinates(supervisor_ssn)

    def close(self):
        self.supervision_dao.close()

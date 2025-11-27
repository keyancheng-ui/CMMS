from .base_dao import BaseDAO


class ContractorDAO(BaseDAO):
    def get_all_contractor(self):
        result = self.execute_query("SELECT Company_name FROM Contractor_Company")
        index = 1
        for company in result:
            print(f"Contractor Company {index}: {company[0]}")
            index += 1
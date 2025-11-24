class ContractorService:
    def __init__(self, dao):
        self.dao = dao

    def add(self, name):
        return self.dao.add(name)

    def list_all(self):
        return self.dao.list_all()

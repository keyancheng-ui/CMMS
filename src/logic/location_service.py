class LocationService:
    def __init__(self, dao):
        self.dao = dao

    def list_all(self):
        return self.dao.list_all()

    def add(self, building, floor, room):
        return self.dao.add(building, floor, room)

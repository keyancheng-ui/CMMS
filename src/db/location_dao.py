from .base_dao import BaseDAO
from .validators import Validators


class LocationDAO(BaseDAO):

    # insert a new campus location to the database
    def create_location(self, building, floor, room_number):
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'",
            )
            if len(result) == 0:
                return self.execute_update(
                    f"INSERT INTO Location (Building, Floor, Room_number) VALUES ('{building}', '{floor}', '{room_number}')"
                )
            else:
                print("This location already already exist!")



        else:
            print("insertion is invalid, f**k off.")

    def check_location(self, building, floor, room_number):

        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'",
            )
            if len(result) == 0:
                print("Ain’t no such place")

            else:
                print("You are right. It is on campus")



        else:
            print("Not valid. Please have some common sense.")

    def get_all_locations(self):

        result = self.execute_query("SELECT * FROM Location")
        for row in result:
            print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")

    def get_locations_by_building(self, building):
        build_valid, build_msg = Validators.validate_building(building)
        if build_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}'",
            )
            for row in result:
                print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")
        else:
            print("Not valid. Please have some common sense.")

    def get_vacant_offices(self):
        result = self.execute_query(
                f"SELECT * FROM Office WHERE OwnerSsn IS NULL"
        )
        for row in result:
            print(f"Building: {row['Office_Building']}, Floor: {row['Office_Floor']}, Room_number: {row['Office_RoomNum']}")


    def assign_office_to_employee(self, building, floor, room_number, owner_ssn):
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            self.execute_query(
                f"UPDATE Office SET OwnerSsn = '{owner_ssn}' WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
            )
        else:
            print("Not valid. This place doesn't exist. What are you f**king thinkin of?")


    def vacate_office(self, building, floor, room_number) :
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            self.execute_query(
                f"UPDATE Office SET OwnerSsn = NULL WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
            )

        else:
            print("Not valid. This place doesn't exist. What are you f**king thinkin of?")

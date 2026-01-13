import sys
import os
import cmd
import shlex
import getpass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from src.logic.general_service import Service


class ActivityCLI(cmd.Cmd):
    """Command Line Interface for CMMS System"""

    def __init__(self, password):
        """Initialize the CLI with database connection"""
        super().__init__()
        try:
            self.service = Service(password)
            self.prompt = "activity> "
            self.intro = """
╔══════════════════════════════════════════════════════════════╗
║                         CMMS System CLI                      ║
║                    Type 'help' for commands                  ║
║                       Thanks for your use!                   ║
╚══════════════════════════════════════════════════════════════╝
"""
            print("Successfully connected to database!")
        except Exception as e:
            print(f"Failed to initialize service: {e}")
            sys.exit(1)

    def do_exit(self, arg):
        """Exit the application: exit"""
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the application: quit"""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """Exit on Ctrl+D: EOF"""
        return self.do_exit(arg)

    # Activity Commands
    def do_list_activities(self, arg):
        """List all activities: list_activities"""
        try:
            activities = self.service.get_all_activities()
            if activities:
                print("\nAll Activities:")
                print("-" * 80)
                for activity in activities:
                    print(f"Time: {activity[0]}, Building: {activity[3]}, Floor: {activity[4]}, Room: {activity[5]}")
                    print(f"  Type: {activity[1]}, Requires Chemical: {activity[2]}")
                    print("-" * 80)
            else:
                print("No activities found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_create_activity(self, arg):
        """Create a new activity: create_activity "time" "type" "chemical" "building" "floor" "room" """
        try:
            args = shlex.split(arg)
            if len(args) != 6:
                print("Usage: create_activity \"time\" \"type\" \"chemical\" \"building\" \"floor\" \"room\"")
                return

            time, activity_type, chemical, building, floor, room = args
            result = self.service.create_activity(time, activity_type, chemical, building, floor, room)
            print(f"Activity created successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    def do_get_activity(self, arg):
        """Get activity details: get_activity "time" "building" "floor" "room" """
        try:
            args = shlex.split(arg)
            if len(args) != 4:
                print("Usage: get_activity \"time\" \"building\" \"floor\" \"room\"")
                return

            time, building, floor, room = args
            activity = self.service.get_activity(time, building, floor, room)
            if activity:
                print(f"Activity Details: {activity}")
            else:
                print("Activity not found.")
        except Exception as e:
            print(f"Error: {e}")

    # Employee Commands
    def do_list_employees(self, arg):
        """List all employees: list_employees"""
        try:
            employees = self.service.get_all_employees()
            if employees:
                print("\nAll Employees:")
                print("-" * 50)
                for emp in employees:
                    print(f"SSN: {emp[0]}, Name: {emp[1]}, Level: {emp[2]}")
            else:
                print("No employees found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_add_employee(self, arg):
        """Add a new employee: add_employee "ssn" "name" "level" """
        try:
            args = shlex.split(arg)
            if len(args) != 3:
                print("Usage: add_employee \"ssn\" \"name\" \"level\"")
                return

            ssn, name, level = args
            result = self.service.add_employee(ssn, name, level)
            print(f"Employee added successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    # Location Commands
    def do_list_locations(self, arg):
        """List all locations: list_locations"""
        try:
            locations = self.service.get_all_locations()
            if locations:
                print("\nAll Locations:")
                print("-" * 40)
                for loc in locations:
                    print(f"Building: {loc[0]}, Floor: {loc[1]}, Room: {loc[2]}")
            else:
                print("No locations found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_create_location(self, arg):
        """Create a new location: create_location "building" "floor" "room" """
        try:
            args = shlex.split(arg)
            if len(args) != 3:
                print("Usage: create_location \"building\" \"floor\" \"room\"")
                return

            building, floor, room = args
            result = self.service.create_location(building, floor, room)
            print(f"Location created successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    # Temporary Employee Commands
    def do_list_temp_employees(self, arg):
        """List all temporary employees: list_temp_employees"""
        try:
            temp_emps = self.service.get_all_temp_employees()
            if temp_emps:
                print("\nAll Temporary Employees:")
                print("-" * 60)
                for emp in temp_emps:
                    print(f"SSN: {emp[0]}, Company: {emp[1]}")
            else:
                print("No temporary employees found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_create_temp_employee(self, arg):
        """Create a temporary employee: create_temp_employee "ssn" "company" """
        try:
            args = shlex.split(arg)
            if len(args) != 2:
                print("Usage: create_temp_employee \"ssn\" \"company\"")
                return

            ssn, company = args
            result = self.service.create_temp_employee_with_company(ssn, company, company)
            print(f"Temporary employee created successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    # Report Commands


    def do_vacant_offices(self, arg):
        """List vacant offices: vacant_offices"""
        try:
            offices = self.service.get_vacant_offices()
            if offices:
                print("\nVacant Offices:")
                print("-" * 40)
                for office in offices:
                    print(f"Building: {office[0]}, Floor: {office[1]}, Room: {office[2]}")
            else:
                print("No vacant offices found.")
        except Exception as e:
            print(f"Error: {e}")

    # SQL Command
    def do_sql(self, arg):
        """Execute custom SQL query: sql SQL_STATEMENT"""
        if not arg:
            print("Usage: sql SQL_STATEMENT")
            print("Example: sql SELECT * FROM Employee WHERE Emp_Level = 'base_level worker'")
            return

        try:
            result = self.service.execute_custom_sql(arg)
            if result:
                print("\nQuery Result:")
                print("-" * 80)
                if isinstance(result, list):
                    for row in result:
                        print(row)
                else:
                    print(result)
            else:
                print("Query executed successfully (no results returned).")
        except Exception as e:
            print(f"SQL Error: {e}")

    # Assignment Commands
    def do_assign_manager(self, arg):
        """Assign manager to activity: assign_manager "manager_ssn" "time" "building" "floor" "room" """
        try:
            args = shlex.split(arg)
            if len(args) != 5:
                print("Usage: assign_manager \"manager_ssn\" \"time\" \"building\" \"floor\" \"room\"")
                return

            manager_ssn, time, building, floor, room = args
            result = self.service.assign_manager_to_activity(manager_ssn, time, building, floor, room)
            print(f"Manager assigned successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    def do_assign_employee(self, arg):
        """Assign employee to activity: assign_employee "time" "building" "floor" "room" "worker_ssn" """
        try:
            args = shlex.split(arg)
            if len(args) != 5:
                print("Usage: assign_employee \"time\" \"building\" \"floor\" \"room\" \"worker_ssn\"")
                return

            time, building, floor, room, worker_ssn = args
            result = self.service.assign_employee_to_activity(time, building, floor, room, worker_ssn)
            print(f"Employee assigned successfully: {result}")
        except Exception as e:
            print(f"Error: {e}")

    def do_help(self, arg):
        """Show available commands: help [command]"""
        commands = {
            'Activity': ['list_activities', 'create_activity', 'get_activity'],
            'Employee': ['list_employees', 'add_employee'],
            'Temporary Employee': ['list_temp_employees', 'create_temp_employee'],
            'Location': ['list_locations', 'create_location'],
            'Assignment': ['assign_manager', 'assign_employee'],
            'Reports': [ 'vacant_offices'],
            'Advanced': ['sql'],
            'System': ['help', 'exit', 'quit']
        }

        print("\nAvailable Commands:")
        print("=" * 50)
        for category, cmds in commands.items():
            print(f"\n{category}:")
            for cmd in cmds:
                method = getattr(self, f'do_{cmd}')
                # 安全地获取文档字符串
                doc = method.__doc__
                if doc is None:
                    doc = "No description available"
                else:
                    # 提取第一行作为简短描述
                    doc = doc.split('\n')[0].strip()
                    # 如果包含冒号，取冒号后面的部分
                    if ':' in doc:
                        doc = doc.split(':', 1)[1].strip()
                print(f"  {cmd:20} - {doc}")
        print("\nFor detailed help on a command, type: help <command>")

    def default(self, line):
        """Handle unknown commands"""
        print(f"Unknown command: {line}. Type 'help' for available commands.")


def get_password():
    """Get database password from user input"""
    print("Database Authentication Required")
    print("-" * 30)
    password = getpass.getpass("Enter database password: ")
    return password


def main():
    """Main entry point for the CLI"""
    try:
        password = get_password()
        ActivityCLI(password).cmdloop()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"Error starting CLI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
import sys
from dotenv import load_dotenv

load_dotenv()

from db.connection import ping_server

if __name__ == "__main__":
    ok = ping_server()
    if ok:
        print("MySQL connection: OK")
    else:
        print("MySQL connection: ERROR")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        from ui.gui import run
        run()
    else:
        from ui.cli import main
        main()

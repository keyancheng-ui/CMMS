import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        from ui.gui import run
        run()
    else:
        from ui.cli import main
        main()

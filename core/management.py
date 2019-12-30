import sys
from bot.main import Main


class ManagementUtility:
    """
    Encapsulate the logic of the manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]

    def execute(self):
        """
        Run given command-line arguments.
        """
        bot = Main()
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        if subcommand == "runbot":
            bot.start_bot()
        elif subcommand == "calibrate_colors":
            bot.calibrate_colors()
        elif subcommand == "calibrate_positions":
            bot.calibrate_positions()
        else:
            sys.stdout.write("Command not found")


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()

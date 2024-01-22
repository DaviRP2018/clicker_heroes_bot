import sys

from bot.main import Main
from utils.manual_utils import manual_calibrate_colors, manual_calibrate_positions
from utils.utils import calibrate_colors, calibrate_positions, configure


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
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"  # Display help if no arguments were given.

        if subcommand == "runbot":
            bot = Main()
            bot.start_bot()
        elif subcommand == "configure":
            configure()
        elif subcommand == "calibratecolors":
            calibrate_colors()
        elif subcommand == "calibratepositions":
            calibrate_positions()
        elif subcommand == "mcc":
            manual_calibrate_colors()
        elif subcommand == "mcp":
            manual_calibrate_positions()

        else:
            sys.stdout.write("Command not found")


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()

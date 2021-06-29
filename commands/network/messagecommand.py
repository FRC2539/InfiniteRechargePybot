from commands2 import InstantCommand

from subsystems.cougarsystem import CougarSystem


class MessageCommand(InstantCommand):
    """
    Sends a general-robot related message, not
    specific to any one subsystem.
    """

    def __init__(self, msg):
        super().__init__()

        self.msg = msg

    def initialize(self):
        CougarSystem.sendGeneralMessage(self.msg)

    def runWhenDisabled(self):
        return True

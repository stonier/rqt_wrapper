#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/stonier/rqt_wrapper/license/LICENSE
#
##############################################################################
# Imports
##############################################################################

import sys
from .ros_masters import RosMasterMonitor
import rocon_python_utils.system
import signal
import tempfile

try:  # indigo
    from python_qt_binding.QtGui import QApplication, QMessageBox
except ImportError:  # kinetic+ (pyqt5)
    from python_qt_binding.QtWidgets import QApplication, QMessageBox

from python_qt_binding.QtCore import Qt, QCoreApplication, QObject, QTimer, Signal, Slot

##############################################################################
# Classes
##############################################################################


class Switcher(QObject):
    # PySide signals are always defined as class attributes (GPL Pyqt4 Signals use pyqtSignal)
    signal_master_changed_state = Signal(bool)

    def __init__(self, rqt_plugin_name):
        super(Switcher, self).__init__()
        self._rqt_plugin_name = rqt_plugin_name
        self._rqt_subprocess = None
        self._no_ros_master_dialog = QMessageBox(QMessageBox.Warning, self.tr(self._rqt_plugin_name), self.tr("Waiting for the ROS Master to become available."))
        self._no_ros_master_abort_button = self._no_ros_master_dialog.addButton(QMessageBox.Abort)
        self._no_ros_master_abort_button.clicked.connect(self.shutdown)
        self.signal_master_changed_state.connect(self.switch_state, type=Qt.QueuedConnection)
        self._ros_master_monitor = RosMasterMonitor(period=1, callback_function=self._master_changed_state)
        self._rqt_subprocess_shutdown_by_us = False

    @Slot(bool)
    def switch_state(self, new_master_found):
        '''
        :param bool new_master_found: true when a new master is detected, false when a master has disappeared.
        '''
        if new_master_found:
            self._no_ros_master_dialog.hide()
            self._launch_rocon_remocon()
        else:
            self._no_ros_master_dialog.show()
            self._no_ros_master_dialog.raise_()
            if self._rqt_subprocess is not None:
                self._rqt_subprocess_shutdown_by_us = True
                self._rqt_subprocess.send_signal(signal.SIGINT)
                # self._rqt_subprocess.terminate() # this is SIGTERM
                self._rqt_subprocess = None

    def shutdown(self):
        '''
        Shutdowns from external signals or the abort button while waiting for a master.
        '''
        print("Shutting down the ros master monitor")
        self._ros_master_monitor.shutdown()
        if self._rqt_subprocess is not None:
            print("Terminating subprocess")
            self._rqt_subprocess.send_signal(signal.SIGINT)
            # self._rqt_subprocess.terminate() # this is SIGTERM
            self._rqt_subprocess = None
        QCoreApplication.instance().quit()

    def _rqt_shutdown(self):
        '''
        Shutdown handler coming from the rqt subprocess shutting down. This needs
        to be handled differently depending on whether it's us shutting it down
        because a ros master shut down (in which case we need to stay alive)
        or otherwise.
        '''
        if not self._rqt_subprocess_shutdown_by_us:
            self._ros_master_monitor.shutdown()
            QCoreApplication.instance().quit()
        else:
            self._rqt_subprocess_shutdown_by_us = False

    def _master_changed_state(self, available):
        '''
        :param bool available: whether the ros master is available or not.
        '''
        self.signal_master_changed_state.emit(available)

    def _launch_rocon_remocon(self):
        script = '''
#!/usr/bin/env python
import sys
from rqt_gui.main import Main
main = Main()
sys.exit(main.main(sys.argv, standalone='%s'))
        ''' % self._rqt_plugin_name
        executable_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        executable_file.write(script)
        executable_file.flush()
        self._rqt_subprocess = rocon_python_utils.system.Popen(['python', executable_file.name], postexec_fn=self._rqt_shutdown)


class RQTWrapper(object):
    def __init__(self, rqt_plugin_name):
        signal.signal(signal.SIGINT, self._shutdown)
        self._app = QApplication(sys.argv)
        self._rqt_wrapper = Switcher(rqt_plugin_name)
        # Let the interpreter run each 200 ms, this gives a chance for CTRL-C signals to come through
        self._give_signals_a_chance_timer = QTimer()
        self._give_signals_a_chance_timer.timeout.connect(lambda: None)
        self._give_signals_a_chance_timer.start(200)

    def exec_(self):
        return self._app.exec_()

    def _shutdown(self, signum, f):
        if signum == signal.SIGINT:
            self._rqt_wrapper.shutdown()

##############################################################################
# Example Usage - Rocon Remocon
##############################################################################

# if __name__ == '__main__':
#     rqt_wrapper = RQTWrapper('rocon_remocon')
#     sys.exit(rqt_wrapper.exec_())

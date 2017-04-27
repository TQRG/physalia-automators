"""Interaction using Monkeyrunner"""

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import os
import subprocess
import click

ANDROID_HOME = os.environ['ANDROID_HOME']
if not ANDROID_HOME:
    click.secho("Error: Could not find $ANDROID_HOME", fg='red')

monkeyrunner_path = os.path.join(ANDROID_HOME, "tools/monkeyrunner")
if not os.path.exists(monkeyrunner_path):
    monkeyrunner_path = os.path.join(ANDROID_HOME, "tools/bin/monkeyrunner")
if not os.path.exists(monkeyrunner_path):
    click.secho("Error: Could not find monkeyrunner", fg='red')

class MonkeyrunnerUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `Monkeyrunner`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 jython_module, test_case,
                 minimum_execution_time):  # noqa: D102
        super(MonkeyrunnerUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
        )
        self.jython_module = jython_module
        self.test_case = test_case
        self.minimum_execution_time = minimum_execution_time

    def prepare(self):
        """Prepare environment for running."""
        self.install_app()
        self.open_app()
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.uninstall_app()
    
    def _run(self):
        @minimum_execution_time(seconds=self.minimum_execution_time)
        def launch_monkeyrunner():
            subprocess.check_output(
                [
                    monkeyrunner_path,
                    self.jython_module,
                    self.test_case
                ]
            )
        launch_monkeyrunner()
        
JYTHON_MODULE = "./monkeyrunner_jython.py"
APK = "../apks/testapp.apk"
APP_PKG = "com.tqrg.physalia.testapp"
APP_VERSION = "0.01"

# -------------------------------------------------------------------------- #

tap_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-tap",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_tap",
    time_boundaries.TAP
)

# print tap_use_case.run().duration

# -------------------------------------------------------------------------- #

long_tap_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-long_tap",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_long_tap",
    time_boundaries.LONG_TAP
)

# print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

dragndrop_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-dragndrop",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_dragndrop",
    time_boundaries.DRAGNDROP
)

# print dragndrop_use_case.run().duration

# -------------------------------------------------------------------------- #

swipe_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-swipe",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_swipe",
    time_boundaries.SWIPE
)

# print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

back_button_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-back_button",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_back_button",
    time_boundaries.BACK_BUTTON
)

print back_button_use_case.run().duration

# -------------------------------------------------------------------------- #

input_text_use_case = MonkeyrunnerUseCase(
    "Monkeyrunner-input_text",
    APK,
    APP_PKG,
    APP_VERSION,
    "monkeyrunner_jython.py",
    "run_input_text",
    time_boundaries.INPUT_TEXT
)

print input_text_use_case.run().duration

# -------------------------------------------------------------------------- #

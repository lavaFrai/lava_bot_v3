import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


class SystemRequirementsChecker:
    SYSTEM_REQUIREMENTS_OK = 0
    SYSTEM_REQUIREMENTS_ERROR_CAN_NOT_IMPORT_MODULES = 1
    SYSTEM_REQUIREMENTS_INVALID_INTERPRETER_VERSION = 2

    MINIMAL_PYTHON_VERSION = (3, 7)

    @staticmethod
    def check_system_requirements():
        requirements = SystemRequirementsChecker.load_requirements()
        interpreter = SystemRequirementsChecker.get_python_interpreter_version()

        try:
            pkg_resources.require(requirements)
        except (DistributionNotFound, VersionConflict) as e:
            return SystemRequirementsChecker.SYSTEM_REQUIREMENTS_ERROR_CAN_NOT_IMPORT_MODULES

        if interpreter[0] < SystemRequirementsChecker.MINIMAL_PYTHON_VERSION[0] or \
           interpreter[1] < SystemRequirementsChecker.MINIMAL_PYTHON_VERSION[1]:
            return SystemRequirementsChecker.SYSTEM_REQUIREMENTS_INVALID_INTERPRETER_VERSION

        return SystemRequirementsChecker.SYSTEM_REQUIREMENTS_OK

    @staticmethod
    def get_python_interpreter_version():
        return sys.version_info

    @staticmethod
    def load_requirements():
        with open("requirements.txt", "r") as f:
            requirements = f.readlines()
            return requirements

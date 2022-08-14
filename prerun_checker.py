from utils.system_requirements import SystemRequirementsChecker

from utils.logger import *


logger = Logger(Logger.LOG_LEVEL_DEBUG)
requirements_checker_result = SystemRequirementsChecker.check_system_requirements()

if not requirements_checker_result == SystemRequirementsChecker.SYSTEM_REQUIREMENTS_OK:
    if requirements_checker_result == SystemRequirementsChecker.SYSTEM_REQUIREMENTS_INVALID_INTERPRETER_VERSION:
        logger.Error("Minimal supported version of python interpreter is " + '.'.join(map(str, SystemRequirementsChecker.MINIMAL_PYTHON_VERSION)))
    elif requirements_checker_result == SystemRequirementsChecker.SYSTEM_REQUIREMENTS_ERROR_CAN_NOT_IMPORT_MODULES:
        logger.Error("Can not import modules, please run command: \"pip install -r requirements.txt\"")
    exit(-1)

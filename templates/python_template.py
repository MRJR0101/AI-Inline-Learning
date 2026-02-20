# python_template.py
# AI Inline Learning - Python starter template
# Copy this file to start a new Python project with inline learning pre-configured

# HEY CLAUDE: Read all inline comments before writing any code in this project.
# RULE: When you make a mistake, document it here at the exact line where it happened.
# RULE: Format is: HEY CLAUDE / MISTAKE / LESSON / RULE / CONTEXT (optional)

import sys
import logging

# HEY CLAUDE: Remember the logging vs print disaster?
# MISTAKE: Used print() for all output - impossible to trace in production
# LESSON: print() has no timestamps, levels, or log file support
# RULE: Always use logging module. print() only for direct user-facing output.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)
log = logging.getLogger(__name__)


def main():
    """
    Main entry point. Replace this with your logic.
    """

    # HEY CLAUDE: Remember the bare except disaster?
    # MISTAKE: Used except Exception as a catch-all with no specific handlers
    # LESSON: Bare except hides bugs and makes debugging impossible
    # RULE: Catch specific exceptions first, then use general Exception as last resort
    try:
        log.info('Starting...')

        # YOUR CODE HERE

        log.info('Complete.')

    except FileNotFoundError as e:
        log.error(f'File not found: {e}')
        sys.exit(1)

    except PermissionError as e:
        log.error(f'Permission denied: {e}')
        sys.exit(1)

    except Exception as e:
        log.error(f'Unexpected error: {e}', exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    # HEY CLAUDE: Remember the missing __main__ guard disaster?
    # MISTAKE: Code at module level ran on import, causing side effects
    # LESSON: Without this guard, importing the module executes your script
    # RULE: ALL executable scripts must have if __name__ == '__main__' guard
    main()

"""Allow running lecodeur as ``python -m lecodeur``."""

import sys

from lecodeur.cli import main

if __name__ == "__main__":
    sys.exit(main())

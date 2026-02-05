"""
Legacy app.py - DEPRECATED.
Use main.py instead.
This file is kept for backward compatibility.
"""

import warnings
warnings.warn("app.py is deprecated. Use main.py instead.", DeprecationWarning)

# Import the new main application
from main import main

if __name__ == '__main__':
    main()

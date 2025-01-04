# SPDX-FileCopyrightText: 2025-present kleines Filmröllchen <kleines@filmroellchen.eu>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from autotranscode.cli import autotranscode

    sys.exit(autotranscode())

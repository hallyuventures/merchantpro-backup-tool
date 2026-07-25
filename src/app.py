"""
MerchantPro Backup Tool

Main entry point.
"""

from pathlib import Path


def banner():

    print("=" * 60)
    print(" MerchantPro Backup Tool")
    print("=" * 60)
    print()


def main():

    banner()

    print("Application started.")
    print()

    print("Project folder:")
    print(Path.cwd())

    print()

    print("Ready.")


if __name__ == "__main__":
    main()
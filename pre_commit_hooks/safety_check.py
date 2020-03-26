import argparse
import logging
import os
import subprocess
import sys

from safety.cli import check

logger = logging.getLogger(__name__)


def do_the_safety_check(args):
    if args.requirements_file:
        with open(args.requirements_file) as fp:
            reqs = fp.read()
    else:
        reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode()

    if args.exclude:
        reqs = reqs.splitlines()
        exclude = []
        for item in args.exclude:
            exclude.append(item + "==")

        exclude = tuple(exclude)
        for item in reqs:
            if item.startswith(exclude):
                reqs.remove(item)

        reqs = """
        {}
        """.format(
            "\n".join(reqs[1:])
        )

    with open("temp_file.txt", "w+") as file:
        file.write(reqs)
    try:
        check.main(["--full-report", "--file", "temp_file.txt"])
    except SystemExit as error:
        if error.code == 0:
            return 0
        return 1

    finally:
        os.remove("temp_file.txt")


def main(args=None):
    parser = argparse.ArgumentParser(
        usage="""
                           Download json files containing a list of CVE's and run the safety tool to check if the current environment(or specified file) contains vulnerabilities.
                           Examples of usage:
                           1: python /path/to/this/file/safety_script.py --download --safetycheck
                           2: python /path/to/this/file/safety_script.py --safetycheck --exclude bleach mistune web3

                           """
    )

    parser.add_argument(
        "--requirementsfile",
        dest="requirements_file",
        type=str,
        default=None,
        help="Set if you want to run safety tool on a file instead of on environment. None by default",
    )
    parser.add_argument(
        "--exclude",
        dest="exclude",
        type=str,
        nargs="+",
        default=None,
        help="Specify which requirements you want to exclude",
    )
    args = parser.parse_args(args)

    safety_check = do_the_safety_check(args)
    sys.exit(safety_check)


if __name__ == "__main__":
    exit(main(sys.argv[1:]))

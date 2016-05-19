import os
import sys


def getenv():
    env = os.environ.copy()
    env["PYTHONPATH"] = ":".join(sys.path)[1:]  # strip leading colon
    return env


def kill(process):
    if os.name == "nt":
        os.system("taskkill /f /pid %s" % process.pid)
    else:
        process.terminate()

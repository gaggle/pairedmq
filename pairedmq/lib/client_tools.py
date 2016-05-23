import os
from contextlib import contextmanager
from distutils.dir_util import copy_tree
from importlib import import_module
from shutil import rmtree
from tempfile import mkdtemp


@contextmanager
def expose_modules(*modulenames):
    """

    :type modulenames: list
    """
    tmpdir = mkdtemp()

    def modulename_to_srcdst(m):
        mod = import_module(m)
        src_ = os.path.dirname(os.path.abspath(mod.__file__))
        dst_ = os.path.join(tmpdir, os.path.basename(src_))
        return src_, dst_

    try:
        copypaths = dict(map(modulename_to_srcdst, modulenames))
        [copy_tree(src, dst) for (src, dst) in copypaths.iteritems()]
        yield tmpdir
    finally:
        rmtree(tmpdir, ignore_errors=True)


def mergeenv(moreenv=None, pythonpaths=None):
    if moreenv is None:
        moreenv = {}
    if pythonpaths is None:
        pythonpaths = []
    env = merge_dicts(os.environ, moreenv)
    env["PYTHONDONTWRITEBYTECODE"] = "true"
    if pythonpaths:
        paths = env.get("PYTHONPATH").split(os.pathsep) if env.get("PYTHONPATH") else []
        paths.extend(pythonpaths)
        env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def kill(process):
    if os.name == "nt":
        os.system("taskkill /f /pid %s" % process.pid)
    else:
        process.terminate()

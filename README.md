# pairedmq
[![Build Status](https://travis-ci.org/gaggle/pairedmq.svg?branch=master)](https://travis-ci.org/gaggle/pairedmq)

Simple paired client/server: 
You make a client that spawns a server, 
and you tell it what to do.

It's especially easy to run Python-like interpreters such as Autodesk Maya,
you can execute Maya commands from your pure-Python tool to e.g. batch-process assets.

But any environment that supports [ZeroMQ][zmq] can be automated, sky's the limit.


## Getting Started
Lets do a simple example. This guide is based on Windows but should be easy to adapt to Linux/Mac.

* Make a folder somewhere to hold this experiment
* Open a command line prompt in that folder

You probably want to activate a virtualenv for this,
to avoid polluting your global modules:

    > virtualenv .venv
    > .venv\Scripts\activate

Good, now Python modules we install will only go to this folder.
Let's do our simple experiment:

    > pip install git+https://github.com/gaggle/pairedmq.git
    > python
    >>> from evalexec.client import EvalExecClient
    >>> c = EvalExecClient()
    >>> c.eval("1 + 1")
    2

Great, you just sent that expression to the server process,
it got calculated,
and returned to your client.


## The Next Step
This library provides 5 extendable classes, so you can customize behavior to your liking:

    from pairedmq.client import Client
    from pairedmq.server import Server
    from pairedmq.evalexec.client import EvalExecClient
    from pairedmq.evalexec.server import EvalExecClient
    from pairedmq.mayaclient.client import MayaClient

You can inherit from either of these and override/extend as you please.
The `pairedmq` baseclasses needs just one override each to get going,
the `evalexec` classes are good to go as-is (they spawn a normal python process),
and if your needs are specifically to run Maya you can use the `mayaclient` class.


## Using Maya
Lets kick it up a notch and try interacting with Autodesk Maya.
With this technique we can write pure-Python tools that uses Maya for calculations,
which has several benefits over using the Maya Python interpreter directly:

* You're not tied to the Python version that comes with Maya
* You're not limited to libraries that may or may not exist for Maya's Python
* You're not tied to any stability issues of Maya

And it's pretty easy to do:

First of all it's necessary to install ZMQ into Maya.
[This page has precompiled zip files specifically made for Maya][mayabinaries].
Download the file matching your Maya version
and extract it into `<maya version>/Python/Lib/site-packages`.

Usually:
* Windows: `"C:\Program Files\Autodesk\<Maya version>\Python/Lib/site-packages"`
* Mac: `"/applications/autodesk/<maya version>/Python/Lib/site-packages"`

The `site-packages` folder should end up containing a `zmq` folder.

Now let's create a MayaClient:

    > python
    >>> from pairedmq.mayaclient.client import MayaClient
    >>> c = MayaClient(<path to mayapy.exe>)

That `exe` string has to point to where you have Maya installed, usually it's:

* Windows: `"C:\Program Files\Autodesk\<Maya version>\bin\mayabatch.exe"`
* Mac: `"/applications/autodesk/<maya version>/bin/mayabatch"` on Mac

And finally let's create a sphere and get its radius:

    >>> c.exec_("import pymel.core as pmc", timeout=60000, silent=True)
    >>> c.exec_("transform, sphere = pmc.polySphere()")
    >>> c.eval("sphere.radius.get()")
    1.0

That's it, the full power of Maya is in your hands. Now make something cool!


## Thanks
This whole library is based on examples
from the wonderful book [Practical Maya Programming with Python][book] by [Rob Galanakis][robg].
If you are dealing with Maya in any technical capacity I cannot recommend this book enough.


[zmq]: http://zeromq.org
[mayabinaries]: http://www.robg3d.com/maya-windows-binaries/
[robg]: http://github.com/rgalanakis
[book]: https://www.packtpub.com/hardware-and-creative/practical-maya-programming-python

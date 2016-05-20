# pairedmq
[![Build Status](https://travis-ci.org/gaggle/pairedmq.svg?branch=master)](https://travis-ci.org/gaggle/pairedmq)

Simple paired client/server RPC.

Easily launch a separate process and communicate with it.
It's especially easy to run Python-like interpreters, e.g. Autodesk Maya.

## Getting Started
Lets do a simple example.

* First you probably want to activate a virtualenv for this,
to avoid polluting your main installation)

Then follow these steps:

    $ pip install git+https://github.com/gaggle/pairedmq.git
    $ python
    >>> from evalexec.client import EvalExecClient
    >>> c = EvalExecClient()
    >>> c.eval("1 + 1")
    2

And that's it,
that expression was sent to the server process,
calculated,
and returned to the client.

## Thanks
Based on examples from the wonderful [Practical Maya Programming with Python][book] by [Rob Galanakis][rg].
If you are dealing with Maya in any technical capacity I cannot recommend this book enough.

[rg]: http://github.com/rgalanakis
[book]: https://www.packtpub.com/hardware-and-creative/practical-maya-programming-python

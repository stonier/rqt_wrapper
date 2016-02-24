# RQT Wrapper

This package provides a class that lets you wrap a typical rqt program with code that
allows you to keep it alive while a ROS master at the other end goes up and down.

# Status

Still beta.

Major areas of concern are:

* Doesn't allow you to handle any of the arguments that rqt programs usually let you do.
* Could feasibly be embedded in `rqt_gui` and `qt_gui` where plugins can be loaded in subprocesses (the `--multi-process` option)


# Usage

Todo.

# Programs

Many of the common rqt programs are recreated here with the `wrqt_xxx` prefix.

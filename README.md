# RQT Wrapper

This package provides a class that lets you wrap a typical rqt program with code that
allows you to automatically keep it alive and bring the rqt part up and down as a ROS master
at the other end goes up and down.

This solves the frustration of having to restart all of your rqt applications on
your laptop/pc every time you teardown the robot and relaunch it again.

# Status

Still beta.

Major areas of concern are:

* Doesn't allow you to handle any of the arguments that rqt programs usually let you do.
* Could feasibly be embedded in `rqt_gui` and `qt_gui` where plugins can be loaded in subprocesses (the `--multi-process` option)
* Needs optional policies for the trigger that brings down the rqt plugin

# Usage

Todo.

# Programs

Many of the common rqt programs are recreated here with the `wrqt_xxx` prefix.

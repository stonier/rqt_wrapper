##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(rqt_wrapper)

##############################################################################
# Catkin
##############################################################################

find_package(catkin REQUIRED)
catkin_package()

catkin_python_setup()

##############################################################################
# Installs
##############################################################################

install(
    PROGRAMS
        scripts/wrqt_graph
        scripts/wrqt_reconfigure
        scripts/wrqt_robot_monitor
        scripts/wrqt_py_trees
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

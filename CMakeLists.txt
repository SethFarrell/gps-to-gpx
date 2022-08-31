cmake_minimum_required(VERSION 2.8.3)
project(gps-to-gpx)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
)


catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs sensor_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

# For C++
#set(GPX_CPP gpx_cpp)
#set(GPX_CPP_SRC src/bag_to_gpx.cpp)
#add_executable(${GPX_CPP} ${GPX_CPP_SRC})
#target_link_libraries(${GPX_CPP} ${catkin_LIBRARIES})
#add_dependencies(${GPX_CPP}
#	${catkin_EXPORTED_TARGETS}
	#	${${PROJECT_NAME}_EXPORTED_TARGETS}
	#	)

# Install C++ file
#install(TARGETS ${GPX_CPP}
	#	RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
	#	)

# Install python script 
catkin_install_python(PROGRAMS scripts/bag_to_gpx.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


# Install the launch files
install(DIRECTORY launch/ DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)


#roslint_cpp(${GPX_CPP_SRC})

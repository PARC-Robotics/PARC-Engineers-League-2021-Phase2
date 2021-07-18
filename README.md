# PARC Engineers League - Phase 2
PARC Engineer's League Competition Package for Phase 2

# Setup
### Setup ROS workspace (Only if you don't already have a catkin_ws)
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
```

### Install TurtleBot3 packages via Debian packages

```
sudo apt-get install ros-melodic-dynamixel-sdk
sudo apt-get install ros-melodic-turtlebot3-msgs
sudo apt-get install ros-melodic-turtlebot3
```

### Clone the repository
```
cd ~/catkin_ws/src
git clone --recurse-submodules https://github.com/PARC-Robotics/PARC-Engineers-League-Phase2.git
```
Or if you already have cloned the repo without submodules, run command `git submodule update --init --recursive` to update them.

### Install dependencies
```
cd ~/catkin_ws
sudo apt update
rosdep install --from-paths ./src --ignore-src -y
```

### Compile
```
cd ~/catkin_ws
catkin_make
```

**NOTE:** There is a known issue while compiling, ` Intel RealSense SDK 2.0 is missing`
To solve, update the file `realsense-ros/realsense_camera/CMakeLists.txt`,line: 43 to `find_package(realsense2 2.36.0)`
i.e. downgrade the required version of `realsense2` to `2.36.0`



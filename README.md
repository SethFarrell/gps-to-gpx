Package for reading in messages from gps /fix and outputing a file in gpx form.

# Instructions
1. In your workspace /src directory clone this repo: `git clone https://github.com/SethFarrell/gps-to-gpx.git`
2. Build your workspace: `cd .. && catkin_make`
3. Source your workspace: `source devel/setup.bash`
4. Start the node: `roslaunch launch/gpx_converter.launch`
* If your gps is not publishing on /fix you can specify the topic to use `roslaunch launch/gpx_converter.launch gps_topic:=/other_topic`

The resulting .gpx file will be placed in the scripts folder and be titled with the date


GPX 
https://wiki.openstreetmap.org/wiki/GPX#:~:text=GPX%2C%20or%20GPS%20exchange%20format,and%20convert%20to%20other%20forms

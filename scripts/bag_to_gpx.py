#!/usr/bin/env python

from datetime import datetime
import os

import rospy
from sensor_msgs.msg import TimeReference
from sensor_msgs.msg import NavSatFix
from datetime import datetime

class GPX_Listener:
    def __init__(self):
        self.gps_data = None
        self.gps_time = None

    def gps_callback(self, msg):
        self.gps_data = msg
        self.format_gpx()

    def format_gpx(self):
        date_time = datetime.fromtimestamp(self.gps_data.header.stamp.secs)
        stamped_date = date_time.strftime('%Y-%m-%d')
        stamped_time = date_time.strftime('%H:%M:%S')
        time = stamped_date + 'T' + stamped_time + 'Z'

        lat = self.gps_data.latitude
        lon = self.gps_data.longitude
        ele = self.gps_data.altitude

        # Format each "trkpt" using data from the NavSatFix Message 
        sentence = "\t<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{ele}</ele><time>{time}</time></trkpt>\n".format(lat = lat, lon = lon, ele = ele, time = time)
        f.write(sentence)

    # Print the start of the gpx file (this only happens once per file)
    def print_beginning(self, date):
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n")
        f.write("<gpx \n xmlns=\"http://www.topografix.com/GPX/1/1\"  \n creator= \"A-GPS Tracker5.5\" \n version= \"1.1\" \n xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"  \n xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
        f.write("<metadata>\n")
    
        sentence = "\t<name>" + date + "</name>\n"
        f.write(sentence)
        f.write("\t<desc></desc>\n")
        f.write("</metadata>\n\n")
        f.write("<trk>\n\t<name></name>\n\t<desc></desc>\n\n<trkseg>\n")

    # Print the ending of the gpx file (this only happens once per file)
    def print_ending(self):
	f.write("</trkseg>\n\n")
        f.write("</trk>\n")
        f.write("</gpx>\n")


if __name__ == '__main__':
    rospy.init_node('gpx_converter')

    gpx_converter = GPX_Listener()
    
    # Get the argument for the topic to subscribe to
    gps_topic = rospy.get_param("/gpx_converter/gps_topic")

    rospy.Subscriber(gps_topic, NavSatFix, gpx_converter.gps_callback)

    # Open a new .gpx file with name based on current date
    # Create a file using the current day as file name (would be better if this was retrieved from the first message timestamp
    current_time = datetime.now()
    file_name = current_time.strftime('%m-%d-%Y')

    # If a file for the current day already exists, append the minutes and seconds to the file name
    #file_exists = os.path.isfile(file_name + '.gpx')
    #if (file_exists):
    file_name = file_name + current_time.strftime('_%H_%M_%S')

    # Inside callbacks, fill in trkpt segments as we get data
    # callbacks are called as long as rospy spins, this ends automatically when nodes shut down or maybe if our bag data ends? Might have to manually shutdown at that point 
    #with open("./" + file_name + '.gpx', 'w+') as f:
        #gpx_converter.print_beginning(file_name)
        #rospy.spin()
        #gpx_converter.print_ending()

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Opening with 'a' so that hopefully it writes to file and if power goes out data is still there.
    # might need to try open(filename, 'a', 0) for buffer size 0
    # will test
    with open(os.path.join(__location__, file_name + '.gpx'), 'a', 0) as f:
        gpx_converter.print_beginning(file_name)
        rospy.spin()
        gpx_converter.print_ending()



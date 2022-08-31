#!/usr/bin/env python

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

    def time_callback(self, msg):
        self.gps_time = msg

    def format_gpx(self):
        # convert gps data and time into trkpt line
        time = self.gps_time.time_ref
        lat = self.gps_data.latitude
        lon = self.gps_data.longitude
        ele = self.gps_data.altitude
        
        sentence = "<trkpt lat=\"{lat}\" lon=\"{lon}\"><ele>{ele}</ele><time>{time}</time></trkpt>\n".format(lat = lat, lon = lon, ele = ele, time = time)
        f.write(sentence)

    def print_beginning(self, date):
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n")
        f.write("<gpx \n xmlns=\"http://www.topografix.com/GPX/1/1\"  \n creator= \"A-GPS Tracker5.5\" \n version= \"1.1\" \n xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"  \n xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
        f.write("<metadata>\n")
    
        sentence = "<name>" + date + "</name>\n"
        f.write(sentence)
        f.write("<desc></desc>\n")
        f.write("</metadata>\n\n")
        f.write("<trk> \n <name></name> \n <desc></desc> \n <trkseg>\n")

    def print_ending(self):
	f.write(" </trkseg>\n")
        f.write("</trk>\n")
        f.write("</gpx>\n")


if __name__ == '__main__':
    rospy.init_node('gpx_converter')

    gpx_converter = GPX_Listener()

    rospy.Subscriber('/fix', NavSatFix, gpx_converter.gps_callback)
    rospy.Subscriber('/time_reference', TimeReference, gpx_converter.time_callback)

    # Open a new .gpx file with name based on current date
    # Add general information
    current_time = datetime.now()
    file_name = current_time.strftime('%m-%d-%Y')

    # Inside callbacks, fill in trkpt segments as we get data
    # callbacks are called as long as rospy spins, this ends automatically when nodes shut down or maybe if our bag data ends? 
    with open(file_name + '.gpx', 'w+') as f:
        gpx_converter.print_beginning(file_name)
        rospy.spin()
        gpx_converter.print_ending()
        # add ending data to file before it closes


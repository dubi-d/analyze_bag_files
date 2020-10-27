#!/usr/bin/env python3
import rosbag

class Analyzer:
    def __init__(self):
        self.prev_timestamp = {"/tesla/camera_node/camera_info": None,
                               "/tesla/line_detector_node/segment_list": None,
                               "/tesla/wheels_driver_node/wheels_cmd": None}

        self.periods = {"/tesla/camera_node/camera_info": [],
                     "/tesla/line_detector_node/segment_list": [],
                     "/tesla/wheels_driver_node/wheels_cmd": []}

    def add_msg_data(self, topic, t):
        print("called")

        # skip if it's the first message on this topic
        if self.prev_timestamp[topic] == None:
            self.prev_timestamp[topic] = t
            return

        diff = t - self.prev_timestamp[topic]
        self.periods[topic].append(diff.to_sec())
        self.prev_timestamp[topic] = t


if __name__ == "__main__":
    
    bag = rosbag.Bag("/home/rosbags/example_rosbag_H3.bag")
    
    analyzer = Analyzer() 

    for topic, msg, t in bag.read_messages():
        print(t)
        print(type(t))
        analyzer.add_msg_data(topic, t)
    bag.close()

    print(analyzer.periods)

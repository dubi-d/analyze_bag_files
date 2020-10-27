#!/usr/bin/env python3
import rosbag
import statistics

class Analyzer:
    def __init__(self):
        self.prev_timestamp = {"/tesla/camera_node/camera_info": None,
                               "/tesla/line_detector_node/segment_list": None,
                               "/tesla/wheels_driver_node/wheels_cmd": None}

        self.periods = {"/tesla/camera_node/camera_info": [],
                     "/tesla/line_detector_node/segment_list": [],
                     "/tesla/wheels_driver_node/wheels_cmd": []}

    def add_msg_data(self, topic, t):

        # skip if it's the first message on this topic
        if self.prev_timestamp[topic] == None:
            self.prev_timestamp[topic] = t
            return

        # append new time period (in seconds) to the right list
        diff = t - self.prev_timestamp[topic]
        self.periods[topic].append(diff.to_sec())

        self.prev_timestamp[topic] = t

    def print_results(self):

        for key in self.periods.keys():
            t_min = min(self.periods[key])
            t_max = max(self.periods[key])
            t_avg = statistics.mean(self.periods[key])
            t_med = statistics.median(self.periods[key])
            print(f"{key}:")
            print(f"  num_messages: {len(self.periods[key]) + 1}")
            print("  period:")
            print(f"    min: {t_min:.2f}")
            print(f"    max: {t_max:.2f}")
            print(f"    average: {t_avg:.2f}")
            print(f"    median: {t_med:.2f}")
            print()




if __name__ == "__main__":
    
    bag = rosbag.Bag("/home/rosbags/example_rosbag_H3.bag")
    
    analyzer = Analyzer() 

    for topic, msg, t in bag.read_messages():
        print(t)
        print(type(t))
        analyzer.add_msg_data(topic, t)
    bag.close()

    analyzer.print_results()

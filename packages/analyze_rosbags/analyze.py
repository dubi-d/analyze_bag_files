#!/usr/bin/env python3
import rosbag
import statistics


class Analyzer:
    def __init__(self, topics):
        self.prev_timestamp = {key: None for key in topics}
        self.periods = {key: [] for key in topics}

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
            print("  period (seconds):")
            print(f"    min: {t_min:.2f}")
            print(f"    max: {t_max:.2f}")
            print(f"    average: {t_avg:.2f}")
            print(f"    median: {t_med:.2f}")
            print()


# Config (could also be put in a seperate config file):

topics = ["/tesla/camera_node/camera_info",
          "/tesla/line_detector_node/segment_list",
          "/tesla/wheels_driver_node/wheels_cmd"] 
#topics = ["/diodak/camera_node/image/compressed",
#          "/diodak/wheels_driver_node/wheels_cmd"]
bag_path = "/home/rosbags/example_rosbag_H3.bag"
#bag_path = "/home/rosbags/amod20-rh3-ex-record-David_Dubach.bag"

if __name__ == "__main__":  
    bag = rosbag.Bag(bag_path)

    analyzer = Analyzer(topics) 

    for topic, msg, t in bag.read_messages():
        analyzer.add_msg_data(topic, t)
    bag.close()

    analyzer.print_results()

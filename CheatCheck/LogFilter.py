import UserProfile
import json
from datetime import timedelta


# Class that contains everything to extract necessary info from log
class LogFilter:
    # Init list of instructions and dictionary of users
    def __init__(self):
        self.instructors = list()
        self.users = dict()

    # First check: whether log contains all necessary info
    #              whether that`s the log of student or instructor
    # Then send for more sorting
    def extract_info(self, log):
        if 'username' in log \
                and 'time' in log \
                and 'event' in log \
                and 'event_type' in log \
                and log["username"] not in self.instructors:
            if log["username"][:1] == '0':
                log["username"] = 'z' + log["username"]
            if log["event_type"].find("instructor") != -1:
                self.instructors.append(log["username"])
                if log["username"] in self.users:
                    del self.users[log["username"]]
            else:
                if log["username"] not in self.users:
                    self.users[log["username"]] = UserProfile.UserInfo(UserProfile.convert_to_date(log["time"]))
                self.define_events(log)

    # Define what type of event does the log describe and extract necessary info
    def define_events(self, log):
        cur_user = self.users[log["username"]]
        cur_user.log_number += 1

        if log["event_source"] == "browser":

            if log["event_type"] == "seq_goto" \
                    or log["event_type"] == "seq_next" \
                    or log["event_type"] == "seq_prev":
                event = json.loads(log["event"])

                if int(event["old"]) > int(event["new"]):
                    cur_user.go_back_number += 1

                if event["id"] not in cur_user.tabs:
                    temp_list = list()
                    temp_list.append(int(event["tab_count"]))
                    temp_list.append(int(event["old"]))
                    temp_list.append(int(event["new"]))
                    cur_user.tabs[event["id"]] = temp_list
                else:
                    temp_list = cur_user.tabs[event["id"]]
                    if int(event["new"]) not in temp_list:
                        temp_list.append(int(event["new"]))
                    cur_user.tabs[event["id"]] = temp_list

            elif log["event_type"] == "play_video":
                self.video_settings(cur_user, log)

            elif log["event_type"] == "pause_video" \
                    or log["event_type"] == "stop_video":
                self.video_settings(cur_user, log)
                event = json.loads(log["event"])
                cur_user.videos[event["id"]].pause += 1

            elif log["event_type"] == "seek_video":
                self.video_settings(cur_user, log)
                event = json.loads(log["event"])

                if float(event["old_time"]) > float(event["new_time"]):
                    cur_user.videos[event["id"]].b_seek += 1
                else:
                    cur_user.videos[event["id"]].f_seek += 1

            elif log["event_type"] == "speed_change_video":
                cur_user.number_speed_clicks += 1
                self.video_settings(cur_user, log)

            elif log["event_type"] == "problem_show":
                cur_user.show_answer += 1

            elif log["event_type"] == "edx.ui.lms.link_clicked":
                cur_user.link_clicked_number += 1

        elif log["event_source"] == "server":

            if log["event_type"] == "problem_check":
                event = log["event"]
                cur_user.tasks[event["problem_id"]] = int(event["attempts"]), event["success"] == "correct"

            elif log["event_type"] == "edx.forum.comment.created" \
                    or log["event_type"] == "edx.forum.response.created" \
                    or log["event_type"] == "edx.forum.response.voted" \
                    or log["event_type"] == "edx.forum.searched" \
                    or log["event_type"] == "edx.forum.thread.created" \
                    or log["event_type"] == "edx.forum.thread.voted":
                cur_user.forum_actions += 1

        cur_date = UserProfile.convert_to_date(log["time"])
        if cur_date - cur_user.end_session_date < timedelta(minutes=30):
            cur_user.end_session_date = cur_date
        else:
            cur_user.session_number += 1
            if cur_user.study_time == 0:
                cur_user.study_time = cur_user.end_session_date - cur_user.start_session_date
            else:
                cur_user.study_time += cur_user.end_session_date - cur_user.start_session_date
            cur_user.end_session_date = cur_date
            cur_user.start_session_date = cur_date

    # Get users` info in proper format
    def get_users(self):
        training_set = dict()
        for key in self.users.keys():
            training_set[key] = self.users[key].extract_training_data()
        return training_set

    # Helps extract and sort video info
    @staticmethod
    def video_settings(user, log):
        event = json.loads(log["event"])

        if event["id"] not in user.videos:
            user.videos[event["id"]] = UserProfile.Video(log["time"])
        else:
            video = user.videos[event["id"]]
            if video.end_session != user.end_session_date:
                video.jump += 1
            if UserProfile.convert_to_date(log["time"]) - video.end_session > timedelta(minutes=30):
                video.sessions += 1
                video.time += video.end_session - video.start_session
                video.start_session = UserProfile.convert_to_date(log["time"])
            video.end_session = UserProfile.convert_to_date(log["time"])

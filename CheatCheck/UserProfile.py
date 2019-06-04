from datetime import timedelta, datetime


# Class that contains all necessary info about each user of the course and some extra functions
# which makes some final calculations which can`t be done during reading logs process
# and present final data as a list of values especially for machine learning algorithms
class UserInfo:

    def __init__(self, first_date):

        self.log_number = 0                           # Number of logs connected with the user
        self.forum_actions = 0                        # Number of actions made on the forum
        self.show_answer = 0                          # How many times user asked for an answer
        self.link_clicked_number = 0                  # How many times user clicked the links

        self.total_time = timedelta(0)                # Total time, from the first log till the last
        self.study_time = timedelta(0)                # Time spend studying
        self.session_number = 0                       # Number of study sessions
        self.average_session_time = timedelta(0)      # Average time spent on the study session

        self.go_back_number = 0                       # How many times user rewatches materials
        self.in_tab_visited_percentage = 0            # How thoroughly user was visiting course pages
        self.number_tabs_visited = 0                  # How many tabs in the course were visited

        self.jump_number = 0                          # How many times user comes back while watching videos
        self.average_jump_number = 0                  # Average number of times user comes back while watching the video

        self.average_video_time = timedelta(0)        # Average time user spends watching the video
        self.number_speed_clicks = 0                  # How many times user changed the speed of the video
        self.average_forward_seek = 0                 # How many times user seeks video forward
        self.average_backward_seek = 0                # How many times user seeks video backward
        self.video_watched_number = 0                 # How many videos was watched by user
        self.average_pause_number = 0                 # Average number of pauses while watching the video
        self.average_rewatch_video = 0                # Average number of times the user rewatches the video

        self.average_attempts_number = 0              # Average number of attempts necessary for user to solve problem
        self.success_number = 0                       # Number of solved tasks
        self.tasks_number = 0                         # Total number of tasks

        self.first_date = first_date                  # Temporary. Necessary for date calcs
        self.start_session_date = first_date          # Temporary. Necessary for date calcs
        self.end_session_date = first_date            # Temporary. Necessary for date calcs

        self.final_calcs_done = False                 # Whether final calculations are already done

        # Dictionary of tasks. Each value contains number of attempts and whether the task was solved
        self.tasks = dict()
        # Dictionary of tabs. Each value contains the list of visited pages, but the first element is total number
        self.tabs = dict()
        # Dictionary of videos. Each value contains info in video class
        self.videos = dict()

    # Final Calculations that are to be done when all the logs are already processed
    def final_calcs(self):
        # Final calculations of everything connected with time in general
        self.total_time = self.end_session_date - self.first_date
        self.session_number += 1
        self.study_time += self.end_session_date - self.start_session_date
        if self.session_number == 0:
            self.average_session_time = timedelta(0)
        else:
            self.average_session_time = self.study_time / self.session_number

        # Final calculations for everything connected with moving between pages
        self.number_tabs_visited = len(self.tabs)
        for key in self.tabs.keys():
            temp_list = self.tabs[key]
            self.in_tab_visited_percentage += self.divide((len(temp_list) - 1), int(temp_list[0]))
        self.in_tab_visited_percentage = self.divide(self.in_tab_visited_percentage, self.number_tabs_visited)

        # Final calculations for everything connected with videos
        for key in self.videos.keys():
            video = self.videos[key]
            self.jump_number += video.jump
            self.average_video_time += video.time + \
                (video.end_session - video.start_session)
            self.average_forward_seek += video.f_seek
            self.average_backward_seek += video.b_seek
            self.average_pause_number += video.pause
            self.average_rewatch_video += video.sessions

        self.video_watched_number = len(self.videos)
        self.average_jump_number = self.divide(self.jump_number, self.video_watched_number)
        self.average_forward_seek = self.divide(self.average_forward_seek, self.video_watched_number)
        self.average_backward_seek = self.divide(self.average_backward_seek, self.video_watched_number)
        self.average_pause_number = self.divide(self.average_pause_number, self.video_watched_number)
        self.average_rewatch_video = self.divide(self.average_rewatch_video, self.video_watched_number)
        if self.video_watched_number == 0:
            self.average_video_time = timedelta(0)
        else:
            self.average_video_time = self.average_video_time / self.video_watched_number

        # Finals calculations of everything connected with problems
        for key in self.tasks.keys():
            attempts, success = self.tasks[key]
            if success:
                self.success_number += 1
            self.average_attempts_number += attempts
        self.tasks_number = len(self.tasks)
        self.average_attempts_number = self.divide(self.average_attempts_number, self.tasks_number)

    # If necessary makes final calcs, returns gathered info as a list ready for machine learning
    def extract_training_data(self):

        if not self.final_calcs_done:
            self.final_calcs()
            self.final_calcs_done = True

        return [float(self.log_number),
                float(self.forum_actions),
                float(self.show_answer),
                float(self.link_clicked_number),
                float(self.total_time.total_seconds()),
                float(self.study_time.total_seconds()),
                float(self.session_number),
                float(self.average_session_time.total_seconds()),
                float(self.go_back_number),
                float(self.in_tab_visited_percentage),
                float(self.number_tabs_visited),
                float(self.jump_number),
                float(self.average_jump_number),
                float(self.average_video_time.total_seconds()),
                float(self.number_speed_clicks),
                float(self.average_forward_seek),
                float(self.average_backward_seek),
                float(self.video_watched_number),
                float(self.average_pause_number),
                float(self.average_rewatch_video),
                float(self.average_attempts_number),
                float(self.success_number),
                float(self.tasks_number)]

    # Solves division by zero
    @staticmethod
    def divide(fst, snd):
        if snd == 0:
            return 0.0
        else:
            return float(fst / snd)


# Convert time string to datetime type
def convert_to_date(time):
    time = time[:time.find(".")]
    time = time[:time.find("+")]
    time = time.replace("T", "-")
    time = time.replace(":", "-")
    y, m, d, h, mi, sec = map(int, time.split('-'))
    return datetime(y, m, d, h, mi, sec)


# Class that describes necessary info about the video watched by the user
# When created asks for the time of the log
class Video:
    pause: int

    def __init__(self, time):
        self.f_seek = 0                                   # - forward seek number
        self.b_seek = 0                                   # - backward seek number
        self.start_session = convert_to_date(time)        # - first time of current session
        self.end_session = convert_to_date(time)          # - last time of current session
        self.sessions = 0                                 # - number of sessions
        self.time = timedelta(0)                          # - time of watching
        self.pause = 0                                    # - pause number
        self.jump = 0

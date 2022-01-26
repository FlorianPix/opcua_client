import ctypes
from turtle import distance
import _ctypes
import pygame
import pygame.freetype
import sys
import time
import math
import threading
from queue import Empty, Queue

from dataclasses import dataclass
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication


if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]


class BodyGameRuntime(QObject):
    swipe_signal = pyqtSignal(str, str)
    hand_gesture_signal = pyqtSignal(str, str)
    get_status_signal = pyqtSignal(dict)
    request_status_signal = pyqtSignal(dict)

    def __init__(self, fps, hand_data_queue):
        super().__init__() 
        pygame.init()
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()
        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        pygame.display.set_caption("Kinect for Windows v2 Body Game")
        # Loop until the user clicks the close button.
        self._done = False
        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        # here we will store skeleton data 
        self._bodies = None
        self.status = {}

        self.right_hand = GestureDetector(200, 900)
        self.left_hand = GestureDetector(200, 900)
        self.left_hand_gesture = None
        self.right_hand_gesture = None
        self.fps = fps
        self.hand_data_queue = hand_data_queue


    def timed_call(self, callback, calls_per_second):
        time_time = time.time
        start = time_time()
        period = 1.0 / calls_per_second
        while not self._done:
            if (time_time() - start) > period:
                start += period
                callback()
        self._kinect.close()
        pygame.quit()


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return
        
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def run(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self._done = True # Flag that we are done so we exit this loop

            elif event.type == pygame.VIDEORESIZE: # window resized
                self._screen = pygame.display.set_mode(event.dict['size'], 
                                            pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
        # --- Getting frames and drawing  
        # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
        if self._kinect.has_new_color_frame():
            frame = self._kinect.get_last_color_frame()
            self.draw_color_frame(frame, self._frame_surface)
            frame = None

        # --- Cool! We have a body frame, so can get skeletons
        if self._kinect.has_new_body_frame(): 
            self._bodies = self._kinect.get_last_body_frame()

        # --- draw skeletons to _frame_surface
        if self._bodies is not None: 
            for i in range(0, self._kinect.max_body_count):
                body = self._bodies.bodies[i]
                if not body.is_tracked: 
                    continue 
                
                joints = body.joints 
                # convert joint coordinates to color space 
                joint_points = self._kinect.body_joints_to_color_space(joints)
                self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                self.detect_gestures(joint_points, body.hand_left_state, body.hand_right_state)

        # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
        # --- (screen size may be different from Kinect's color frame size) 
        h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
        target_height = int(h_to_w * self._screen.get_width())
        surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
        self._screen.blit(surface_to_draw, (0,0))
        surface_to_draw = None
        pygame.display.update()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to self.fps frames per second
        self._clock.tick(self.fps)

    def set_disabled_area(self, area):
        self.right_hand.disabled_area = area
        self.left_hand.disabled_area = area

    def detect_gestures(self, joint_points, hand_left_state, hand_right_state):
        #print((joint_points[PyKinectV2.JointType_HandRight].x - joint_points[PyKinectV2.JointType_SpineShoulder].x))
        self.right_hand.update_series(joint_points[PyKinectV2.JointType_HandRight].x, joint_points[PyKinectV2.JointType_HandRight].y, joint_points[PyKinectV2.JointType_SpineShoulder].x, hand_right_state)
        self.status["right"] = self.right_hand.update_status()
        if self.status["right"]["swipe"]:
            self.swipe_signal.emit("right", self.status["right"]["swipe"])
        
        if not None in self.status['right']['hand_gesture']:
            gesture = self.status['right']['hand_gesture'][0]
            if not gesture == self.right_hand_gesture:
                self.hand_gesture_signal.emit("right", gesture)
                self.right_hand_gesture = gesture
           
        self.left_hand.update_series(joint_points[PyKinectV2.JointType_HandLeft].x, joint_points[PyKinectV2.JointType_HandLeft].y, joint_points[PyKinectV2.JointType_SpineShoulder].x, hand_left_state)
        self.status["left"] = self.left_hand.update_status()
        if self.status["left"]["swipe"]:
            self.swipe_signal.emit("left", self.status["left"]["swipe"])

        
        if not None in self.status['left']['hand_gesture']:
            gesture = self.status['left']['hand_gesture'][0]
            if not gesture == self.left_hand_gesture:
                self.hand_gesture_signal.emit("left", gesture)
                self.left_hand_gesture = gesture
        if self.hand_data_queue.full():
            try:
                self.hand_data_queue.get_nowait()
            except Empty:
                pass
        self.hand_data_queue.put(self.status)

@dataclass
class BodyPoint:
    x: int = 0
    y: int = 0
    central: int = 0
    status: int = 0

class GestureDetector:
   
    def __init__(self, y_min, y_max) -> None:
        self.disabled_area = None
        self.point_series = [None] * 30
        self.dead_time = 30
        self.calibration = [y_min, y_max]
        self.hand_status = {
            "percentage": 0,
            "swipe" : None,
            "hand_gesture" : [None, None],
            "hand_area" : 0 
        }

    def update_series(self, x_hand, y_hand, x_central, status):
        self.point_series.insert(0, BodyPoint(x_hand, y_hand, x_central, status))
        self.point_series.pop()
        self.dead_time = self.dead_time - 1


    def update_status(self):
        self.hand_status["swipe"] = self.swipe_action(self.point_series)
        self.hand_status["percentage"] = self.current_percentage(self.point_series[0].y)
        tmp = self.hand_status["hand_gesture"][0]
        self.hand_status["hand_gesture"][0] = self.hand_gesture(self.point_series)
        if not (tmp == self.hand_status["hand_gesture"][0]):
            self.hand_status["hand_gesture"][1] = tmp

        self.hand_status["hand_area"] = self.hand_in_area(self.point_series[0])
        return self.hand_status

    def swipe_action(self, point_series):
        if not None in point_series:
            x_movement = point_series[0].x - point_series[-10].x
            y_movement = abs(point_series[0].y - point_series[-10].y)
            if y_movement < 100 and self.dead_time <= 0:
                self.dead_time = 30
                if x_movement < -350:
                    if self.check_straight_swipe(point_series[0:10]):
                        #print(f"swipe left detected nr. {x_movement}, {y_movement}")
                        return "left"
                    
                if x_movement > 350:
                    if self.check_straight_swipe(point_series[0:10]):
                        #print(f"swipe right detected nr. {x_movement}, {y_movement}")
                        #print(f"x1, x2 {point_series[0].x}, {point_series[-10].x}")
                        #print(f"y1, y2 {point_series[0].y}, {point_series[-10].y}")
                        return "right"
        return None



    def check_straight_swipe(self, point_series):
        x1 = point_series[0].x
        y1 = point_series[0].y
        x2 = point_series[-1].x
        y2 = point_series[-1].y

        m = (y2 - y1)/(x2-x1)
        n = y1 - m*x1
        for point in point_series[1:9]:
            y = m*point.x +n
            if y/point.y < 0.9 or y/point.y > 1.1:
                print("not in a straight line")
                return False 
        return True


    def hand_gesture(self, point_series):
        if not None in point_series:
            #valid_area = self.hand_in_area(point_series)
            valid_area = True
            if valid_area:
                any_check = []
                for point in point_series:
                    any_check.append(point.status)   
                if any_check.count(2) >= len(any_check)-5:
                    return "open"
                if  any_check.count(3) >= len(any_check)-5:
                    return "closed"
                if  any_check.count(4) >= len(any_check)-5:
                    return "thumbs"
        return 'undefined'

    def hand_in_area(self, point):
        if point is not None:
            if not (point.y > self.calibration[0] and point.y < self.calibration[1]):
                 return None
            distance = point.x - point.central
            if self.disabled_area == None:
                if (distance <= 300):
                    return 0
                if (distance > 300 and distance <= 550):
                    return 1
                if (distance > 550):
                    return 2 
            else:
                if self.disabled_area == 0:
                    if (distance <= 400):
                        return 1
                    else:
                        return 2
                if self.disabled_area == 1:
                    if (distance <= 400):
                        return 0
                    else:
                        return 2
                if self.disabled_area == 2:
                    if (distance <= 400):
                        return 0
                    else:
                        return 1
            return None

    def current_percentage(self, value):
        percentage = self.convert_to_percent(value)
        if percentage > 100:
            return 100
        elif percentage < 0:
            return 0
        return percentage
    
    def convert_to_percent(self, value):
        percentage = round(100/(self.calibration[1]-self.calibration[0]) * (self.calibration[1] - value),1)
        if math.isinf(percentage):
            return 0
        return percentage





if __name__ == "__main__":
    def kinect_thread_runner(request_status):
        game = BodyGameRuntime(20, request_status);
        game.swipe_signal.connect(swipe_detected)
        game.hand_gesture_signal.connect(hand_gesture_detected)
        while not game._done:
            game.run()

    def get_hand_data():
        try:
            return hand_data.get_nowait()
        except Empty as e:
            return None

    @pyqtSlot(str, str)
    def swipe_detected(side, direction):
        print(f"{side} Hand: {direction} swipe")
        pass

    @pyqtSlot(str, str)
    def hand_gesture_detected(side, gesture):
        print(f"{side} Hand: {gesture} detected")
        data = get_hand_data()
        if not data:
            return
        data = data[side]
        if data["hand_gesture"][0] == "closed":
            if not data["hand_gesture"][1] == "closed":
                area = data["hand_area"]
                print(area)  
    """
    hand_data dictionary contains dictionary with hand data:
    keys: left, right --> contains dictionary to corresponding hand

    containing dictionary:
    keys:   swipe --> if swipe has been detected (better use emitted signal) - str: left, right 
            percentage --> where y_pos of hand is from 0-100% - int: 0-100
            hand_gesture --> last detected hand gesture - str: open, closed, thumbs
    """
    hand_data = Queue(maxsize=1)

    kinect_thread = threading.Thread(target=kinect_thread_runner, args=(hand_data,))
    kinect_thread.setDaemon(False)
    kinect_thread.start()
    time.sleep(7)
    #get hand data
    print(hand_data.get())

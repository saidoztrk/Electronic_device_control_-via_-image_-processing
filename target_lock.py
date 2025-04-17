import time
import datetime
import cv2
from hand_detector import HandDetector, count_fingers

class TargetLock:
    def __init__(self):
        self.detector = HandDetector(detection_confidence=0.75)

    def process_frame(self, frame):
        frame = self.detector.find_hands(frame, draw=True)
        lm_list = self.detector.find_positions(frame)
        finger_count = count_fingers(lm_list)

        # current_time = time.perf_counter()
        # if finger_count == self.prev_finger_count:
        #     if self.lock_start_time is None:
        #         self.lock_start_time = current_time
        #     elif current_time - self.lock_start_time >= 1.0:
        #         self.is_locked = True
        # else:
        #     self.lock_start_time = None
        #     self.is_locked = False

        # if self.is_locked and not finger_count==0:
        #     cv2.putText(frame, f"Basarili Okuma -> {finger_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        #     self.success=True
        # else:
        #     cv2.putText(frame, f"Parmak Sayisi: {finger_count}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #     self.success=False

        # self.prev_finger_count = finger_count
        return frame,finger_count

    def get_lock_info(self):
        if self.is_locked:
            start_time = datetime.datetime.now()
            return {
                "kilitlenmeZamani": {
                    "saat": start_time.hour,
                    "dakika": start_time.minute,
                    "saniye": start_time.second,
                    "milisaniye": start_time.microsecond,
                }
            }
        return None

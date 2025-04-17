import customtkinter as ctk
from gui import App
import threading
from Cprint import cp
import esp32_tcpServer
import multiprocessing
import time
# image_processing.py
import numpy as np
from hand_detector import *
import cv2
from target_lock import TargetLock

FULL_COMMAND_LIST =[
    "TURN_ON",
    "TURN_OFF",
    "MOTOR_START",
    "MOTOR_STOP",
    "MAGENTA",
    "CYAN",
    "ORANGE",
    "RED",
    "GREEN",
    "BLUE",
    "BUZZER1",
    "BUZZER2",
    "GETCHIP_ID",
]

COMMANDS = {
  1: "RED",
  2: "GREEN",
  3: "BLUE",
  4: "CYAN",
  5: "GETCHIP_ID",
}

# COMMANDS = {
#   1: "RED",
#   2: "GREEN",
#   3: "BLUE",
#   4: "CYAN",
#   5: "MAGENTA",
# }

class image_processing:
    def __init__(self, esp_receive_buff, esp_sending_buff, esp_heartbeat, terminal_buffer):
        self.esp_receive_buff = esp_receive_buff
        self.esp_sending_buff = esp_sending_buff
        self.esp_heartbeat = esp_heartbeat
        self.terminal_buffer = terminal_buffer
        self.camera_status=False

        # El algılama sınıfını başlat
        self.detector = HandDetector(detection_confidence=0.75)

    def reopen_camera_system(self):
        if not self.camera_status==False:
            self.terminal_buffer.put("[IMAGE PROCESSING] CAMERA RECREATION ERROR -> ALREADY WORKING..")
        else:
            new_cam_thread = threading.Thread(target=self.main)
            new_cam_thread.start()

    def finger_command(self,finger_count):
        self.terminal_buffer.put(f"[CONTROL] Command -> {COMMANDS[finger_count]} : {finger_count}")
        self.esp_sending_buff.put(COMMANDS[finger_count]+"\n")

    def main(self):
        self.terminal_buffer.put("[IMAGE PROCESSING] MAIN LOOP")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.terminal_buffer.put("[IMAGE PROCESSING] CAMERA ERROR -> cap.isOpened()")
            return
        self.camera_status=True

        lock_system = TargetLock()
        self.terminal_buffer.put("[IMAGE PROCESSING] START PROCESSING..")


        finger_prev=None
        finger_count=None
        timer=0
        elapsed_time=0
        detected_once = False

        while True:
            ret, frame = cap.read()
            cv2.flip(frame,-1)
            if not ret:
                self.camera_status=False
                self.terminal_buffer.put("[IMAGE PROCESSING] CAMERA ERROR -> cap.read()")
                break

            processed_frame,finger_count = lock_system.process_frame(frame)

            #* 1 SANIYE-KILITLENME
            if finger_count != 0:
                if (finger_count != finger_prev):                    
                    timer=time.perf_counter()
                    finger_prev=finger_count
                    detected_once = False
                elif (finger_count == finger_prev):
                    cv2.putText(processed_frame, f"DETECTION -> {finger_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (122, 122, 255), 2)
                    elapsed_time = time.perf_counter()-timer

                if elapsed_time >= 0.5 and elapsed_time <=1.5 and not detected_once:
                    cv2.putText(processed_frame, f"COMMAND SET -> {finger_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (122, 122, 255), 2)
                    self.finger_command(finger_count)
                    elapsed_time = 0
                    detected_once = True

            cv2.imshow("Target Lock System", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.camera_status=False
                break

        assert self.camera_status==False , "CAMERA_STATUS must be FALSE!"
        cap.release()
        cv2.destroyAllWindows()
        self.terminal_buffer.put("[IMAGE PROCESSING] SHUTDOWN...")


class controller:
    def __init__(self,esp_receive_buff,esp_sending_buff,esp_heartbeat,terminal_buffer):
        self.esp_receive_buff = esp_receive_buff
        self.esp_sending_buff = esp_sending_buff
        self.esp_heartbeat = esp_heartbeat
        self.terminal_buffer = terminal_buffer
    
    def give_command_to_esp1(self,command="TURN_ON\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'TURN_ON'")
        
    def give_command_to_esp2(self,command="TURN_OFF\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'TURN_OFF'")

    def give_command_to_esp3(self,command="MOTOR_START\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'MOTOR_START'")

    def give_command_to_esp4(self,command="MOTOR_STOP\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'MOTOR_STOP'")
    
    def give_command_to_esp5(self,command="MAGENTA\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'MAGENTA'")

    def give_command_to_esp6(self,command="CYAN\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'CYAN'")

    def give_command_to_esp7(self,command="ORANGE\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'ORANGE'")
    
    def give_command_to_esp8(self,command="RED\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'RED'")

    def give_command_to_esp9(self,command="GREEN\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'GREEN'")

    def give_command_to_esp10(self,command="BLUE\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'BLUE'")
        
    def give_command_to_esp11(self,command="GETCHIP_ID\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'GETCHIP_ID'")

    def give_command_to_esp12(self,command="BLUETOOTH_SCAN\n"):
        self.esp_sending_buff.put(command)
        self.terminal_buffer.put("[CONTROL] Command -> 'BLUETOOTH_SCAN'")

class ESP:
    def __init__(self,ip,port,esp_receive_buff,esp_sending_buff,esp_heartbeat,terminal_buffer):
        self.esp32=esp32_tcpServer.tcp_server(ip,port)
        self.esp_receive_buff = esp_receive_buff
        self.esp_sending_buff = esp_sending_buff
        self.esp_heartbeat = esp_heartbeat
        self.terminal_buffer = terminal_buffer
        self.Heartbeat_status=False

    def connect(self):
        while (not self.esp32.connection_status):
            self.esp32.connect_to_esp()

    def sender_loop(self):
        cp.err("[ESP32] SENDER LOOP")
        self.terminal_buffer.put("[ESP32] SENDER LOOP")
        while(True):
            if (not self.esp_sending_buff.empty()):
                message=self.esp_sending_buff.get()
                self.esp32.send_data(message)
            else:
                time.sleep(0.2)

    def receive_loop(self):
        cp.err("[ESP32] RECEIVER LOOP")
        self.terminal_buffer.put("[ESP32] RECEIVER LOOP")
        while(True):
            if (not self.esp_receive_buff.full()):
                message=self.esp32.receive_data()
                if message == "HEARTBEAT":
                    self.esp_heartbeat.put(message)
                else:
                    self.terminal_buffer.put("[ESP32] MSG -> "+message)
                    self.esp_receive_buff.put(message)
            else:
                time.sleep(0.2)

    def heartbeat_checker(self):
        cp.err("[ESP32] HEARBEAT CHECKER LOOP")
        self.terminal_buffer.put("[ESP32] HEARBEAT CHECKER LOOP")
        timer_prev=time.perf_counter()
        self.Heartbeat_status=False
        while True:
            if (not self.esp_heartbeat.empty()):
                _=self.esp_heartbeat.get()
                timer_prev=time.perf_counter() #Timer reset
                self.Heartbeat_status=True
            else:
                ETA_SINCE_HEARTBEAT = time.perf_counter()-timer_prev
                if (ETA_SINCE_HEARTBEAT >= 2):
                        self.Heartbeat_status=False
                        if (ETA_SINCE_HEARTBEAT % 5 == 0):
                            self.terminal_buffer.put(f"[HEARTBEAT] NO HEARBEAT SINCE {ETA_SINCE_HEARTBEAT:.2f}")
            time.sleep(0.3)

    def main(self):
        self.connect() #Threadlerin için en az bir kez bağlantı kurulmuş olmalı
        recv_thread=threading.Thread(target=self.receive_loop)
        send_thread=threading.Thread(target=self.sender_loop)
        heartbeat_thread=threading.Thread(target=self.heartbeat_checker)

        heartbeat_thread.start()
        recv_thread.start()
        send_thread.run()

def main():
    #Buffers
    esp_receive_buff = multiprocessing.Queue()
    esp_sending_buff = multiprocessing.Queue()
    esp_heartbeat=  multiprocessing.Queue()
    terminal_buffer = multiprocessing.Queue()

    for _ in range(1):
        terminal_buffer.put("SYSTEM STARTUP.....")

    #INIT
    imager=image_processing(esp_sending_buff=esp_sending_buff,
                            esp_receive_buff=esp_receive_buff,
                            esp_heartbeat=esp_heartbeat,
                            terminal_buffer=terminal_buffer)


    esp32_link = ESP(ip="192.168.4.1",port=2024,
                    esp_sending_buff=esp_sending_buff,
                    esp_receive_buff=esp_receive_buff,
                    esp_heartbeat=esp_heartbeat,
                    terminal_buffer=terminal_buffer)

    controller_obj = controller(esp_sending_buff=esp_sending_buff,
                                esp_receive_buff=esp_receive_buff,
                                esp_heartbeat=esp_heartbeat,
                                terminal_buffer=terminal_buffer)

    gui_obj = App(control_obj=controller_obj,
                  esp_obj=esp32_link,
                  imager_obj = imager,
                  terminal_buffer=terminal_buffer)

    #Side Threads
    imager_thread = threading.Thread(target=imager.main)
    #cont_thread = threading.Thread(target=controller_obj.)
    esp_thread = threading.Thread(target=esp32_link.main)
    
    imager_thread.start()
    #cont_thread.start()
    esp_thread.start()
    gui_obj.run()

if __name__ == "__main__":
    main()

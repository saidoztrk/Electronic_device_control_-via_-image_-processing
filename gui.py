import customtkinter as ctk
import os ,datetime
import tkinter as tk
from typing import Union,Callable
from Cprint import cp

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#?  LAYER-1
class MAIN_GUI_FRAME(ctk.CTkFrame):
    def __init__(self, master,control_obj,imager_obj,**kwargs):
        
        self.control_obj = control_obj
        self.imager_obj=imager_obj

        super().__init__(master,**kwargs)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

    #? LAYER-2
        self.left_main_frame = ctk.CTkTabview(self,corner_radius=5,border_width=1)
        self.left_main_frame.add("CONTROL")
        self.right_main_frame=ctk.CTkTabview(self,corner_radius=5,border_width=1)
        self.right_main_frame.add("VIDEO-FEED")

        self.left_main_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.right_main_frame.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

    #? LAYER-3
        self.left_main_frame.tab("CONTROL").grid_columnconfigure(3,weight=1)

        self.left_main_frame.columnconfigure(0,weight=1)

        self.command_1=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="LED_ON",command=control_obj.give_command_to_esp1,font=("Cascadia Mono", 15, "bold"))
        self.command_1.grid(row=0,column=0,padx=10,pady=10,sticky="nw")

        self.command_2=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="LED_OFF",command=control_obj.give_command_to_esp2,font=("Cascadia Mono", 15, "bold"))
        self.command_2.grid(row=0,column=1,padx=10,pady=10,sticky="nw")

        self.command_3=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="MOTOR_START",command=control_obj.give_command_to_esp3,font=("Cascadia Mono", 15, "bold"))
        self.command_3.grid(row=1,column=0,padx=10,pady=10,sticky="nw")

        self.command_4=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="MOTOR_STOP",command=control_obj.give_command_to_esp4,font=("Cascadia Mono", 15, "bold"))
        self.command_4.grid(row=1,column=1,padx=10,pady=10,sticky="nw")

        self.command_5=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="MAGENTA",command=control_obj.give_command_to_esp5,font=("Cascadia Mono", 15, "bold"))
        self.command_5.grid(row=2,column=0,padx=10,pady=10,sticky="nw")

        self.command_6=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="CYAN",command=control_obj.give_command_to_esp6,font=("Cascadia Mono", 15, "bold"))
        self.command_6.grid(row=2,column=1,padx=10,pady=10,sticky="nw")

        self.command_7=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="ORANGE",command=control_obj.give_command_to_esp7,font=("Cascadia Mono", 15, "bold"))
        self.command_7.grid(row=3,column=0,padx=10,pady=10,sticky="nw")

        self.command_8=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="RED",command=control_obj.give_command_to_esp8,font=("Cascadia Mono", 15, "bold"))
        self.command_8.grid(row=3,column=1,padx=10,pady=10,sticky="nw")

        self.command_9=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="GREEN",command=control_obj.give_command_to_esp9,font=("Cascadia Mono", 15, "bold"))
        self.command_9.grid(row=4,column=0,padx=10,pady=10,sticky="nw")

        self.command_10=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="BLUE",command=control_obj.give_command_to_esp10,font=("Cascadia Mono", 15, "bold"))
        self.command_10.grid(row=4,column=1,padx=10,pady=10,sticky="nw")

        self.command_11=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="GETCHIP_ID",command=control_obj.give_command_to_esp11,font=("Cascadia Mono", 15, "bold"))
        self.command_11.grid(row=5,column=0,padx=10,pady=10,sticky="nw")

        self.command_11=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="BLUETOOTH_SCAN",command=control_obj.give_command_to_esp12,font=("Cascadia Mono", 15, "bold"))
        self.command_11.grid(row=5,column=1,padx=10,pady=10,sticky="nw")



        self.command_camera=ctk.CTkButton(master=self.left_main_frame.tab("CONTROL"),text="CAMERA_RESET",command=imager_obj.reopen_camera_system,font=("Cascadia Mono", 15, "bold"))
        self.command_camera.grid(row=0,column=3,padx=10,pady=10,sticky="ne")

#?  LAYER-1
class COMPANION_FRAMES(ctk.CTkFrame):
    def __init__(self, master,control_obj,**kwargs):
        super().__init__(master,**kwargs)
        self.control_obj = control_obj

        self.rowconfigure(0,weight=1)

        #? LAYER-2
        self.tabview = ctk.CTkTabview(self,corner_radius=5,border_width=1)
        self.tabview.grid(row=0,rowspan=2,column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.tabview.add("MONITOR")
        self.tabview.add("LIST")
        self.tabview.add("DATA")
        # self.tabview.tab("TAB-1").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview.tab("TAB-2").grid_columnconfigure(0, weight=1)
        #? LAYER-3
        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("TAB-1"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("TAB-2"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("TAB-3"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tabview.tab("MONITOR").columnconfigure(0,weight=1)
        self.tabview.tab("MONITOR").rowconfigure(5,weight=1)

        try:
            self.heartbeat_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="HEARTBEAT",bg_color="orange",font=("Cascadia Mono", 15, "bold"))
            self.heartbeat_label.grid(row=0,column=0,padx=10,pady=10,sticky="nwe")
            self.camera_status=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="CAMERA-STATUS",bg_color="orange",font=("Cascadia Mono", 15, "bold"))
            self.camera_status.grid(row=1,column=0,padx=10,pady=10,sticky="we")        
            self.Mod_sunucu_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="A",bg_color="orange",font=("Cascadia Mono", 15, "bold"))
            self.Mod_sunucu_label.grid(row=2,column=0,padx=10,pady=10,sticky="we")
            self.Kamikaze_sunucu_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="B",bg_color="orange",font=("Cascadia Mono", 15, "bold"))
            self.Kamikaze_sunucu_label.grid(row=3,column=0,padx=10,pady=10,sticky="we")
            self.Onay_sunucu_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="C",bg_color="orange",font=("Cascadia Mono", 15, "bold"))
            self.Onay_sunucu_label.grid(row=4,column=0,padx=10,pady=10,sticky="we")
            
            self.timer_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="12:12:12",bg_color="transparent",font=("Cascadia Mono",28))
            self.timer_label.grid(row=6,column=0,padx=10,pady=10,sticky="swe")

            self.checker_label=ctk.CTkLabel(master=self.tabview.tab("MONITOR"),text="CHECKER CLOCK",bg_color="red",font=("Cascadia Mono", 15, "bold"))
            self.checker_label.grid(row=7,column=0,padx=10,pady=10,sticky="swe")
        except Exception as e:
            cp.fatal(f"LABEL ERROR -> {e}")

#?  LAYER-1
class MENU_FRAME(ctk.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)

        #? LAYER-2
        button1 = ctk.CTkButton(self,text="   MAIN   ",width=50,height=50,corner_radius=20,font=("Cascadia Mono", 15, "bold"))
        button1.grid(row=0,column=0,padx=5, pady=20,sticky="n")
        button2 = ctk.CTkButton(self,text="CUSTOM-1",width=50,height=50,corner_radius=20,font=("Cascadia Mono", 15, "bold"))
        button2.grid(row=1,column=0,padx=5, pady=20)
        button3 = ctk.CTkButton(self,text="CUSTOM-2",width=50,height=50,corner_radius=20,font=("Cascadia Mono", 15, "bold"))
        button3.grid(row=2,column=0,padx=5, pady=20)
        button4 = ctk.CTkButton(self,text="SETTINGS",width=50,height=50,corner_radius=20,font=("Cascadia Mono", 15, "bold"))
        button4.grid(row=3,column=0,padx=5, pady=20,sticky="s")

#?  LAYER-1
class TERMINAL_FRAME(ctk.CTkFrame):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.tabview = ctk.CTkTabview(self,corner_radius=5,border_width=1)
        self.tabview.grid(row=0,column=0, padx=5, pady=0, sticky="nsew")
        self.tabview.add("TERMINAL")

        self.tabview.tab("TERMINAL").columnconfigure(0,weight=1)
        self.tabview.tab("TERMINAL").rowconfigure(0,weight=1)

        self.textbox = ctk.CTkTextbox(master=self.tabview.tab("TERMINAL"), width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.configure(state=ctk.DISABLED)
        self.textbox.configure(font=("Cascadia Mono", 15, "bold"))


#? MAIN-LAYER
class App(ctk.CTk):
    def __init__(self,control_obj,esp_obj,imager_obj,terminal_buffer):
        super().__init__()
        self.control_obj = control_obj
        self.esp_obj=esp_obj
        self.imager_obj=imager_obj
        self.terminal_buffer=terminal_buffer
        self.checker_clock=True
    

        self.title("ALGAN - GROUND CONTROL STATION")
        self.geometry("1920x1080")
        self.wm_attributes("-fullscreen",True)

        self.rowconfigure(0,weight=3)
        self.rowconfigure(1,weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=0)

        self.menu_frame = MENU_FRAME(master=self,width=150,corner_radius=0)
        self.main_frame = MAIN_GUI_FRAME(master=self,control_obj=self.control_obj,imager_obj=self.imager_obj)
        self.terminal_frame = TERMINAL_FRAME(master=self)
        self.companion_frame = COMPANION_FRAMES(master=self,control_obj=self.control_obj,width=500)

        self.menu_frame.grid(row=0,column=0,rowspan=2,pady=(0,20),sticky="nsw")
        self.main_frame.grid(row=0,column=1, padx=20, pady=20,sticky="nswe")
        self.terminal_frame.grid(row=1,column=1, padx=20, pady=20,sticky="nswe")
        self.companion_frame.grid(row=0,column=2,rowspan=2,padx=20,pady=20,sticky="nswe")

    def terminal_print(self,message):
        self.terminal_frame.textbox.configure(state=ctk.NORMAL)
        self.terminal_frame.textbox.insert(ctk.END,f"[{datetime.datetime.now().strftime("%H:%M:%S.%f")[:12]}] : {message}\n")
        self.terminal_frame.textbox.yview(ctk.END)
        self.terminal_frame.textbox.configure(state=ctk.DISABLED)

    def check_terminal_buffer(self):
        if( not self.terminal_buffer.empty()):
            message=self.terminal_buffer.get()
            self.terminal_print(message=message)
        self.after(100, self.check_terminal_buffer)
    
    def check_status(self):
        if (self.esp_obj.Heartbeat_status):
            self.companion_frame.heartbeat_label.configure(bg_color="green")
        else:
            self.companion_frame.heartbeat_label.configure(bg_color="orange")

        if (self.imager_obj.camera_status):
            self.companion_frame.camera_status.configure(bg_color="green")
        else:
            self.companion_frame.camera_status.configure(bg_color="orange")

        if (self.checker_clock):
            self.companion_frame.checker_label.configure(bg_color="red")
            self.checker_clock=False
        else:
            self.companion_frame.checker_label.configure(bg_color="green")
            self.checker_clock=True
        
        self.companion_frame.timer_label.configure(text=f"[{datetime.datetime.now().strftime("%H:%M:%S")}]")
        self.after(500,self.check_status)
        
    def run(self):# Run the GUI event
        try:
            self.after(2000, self.check_terminal_buffer)
            self.after(2000,self.check_status)
            self.mainloop()
        except KeyboardInterrupt:
            print("KEYBOARD INTERRUPT\tKEYBOARD INTERRUPT\nKEYBOARD INTERRUPT\tKEYBOARD INTERRUPT")

class dummy_class:
    def __init__(self):
        pass

if __name__ == "__main__":
    dummy_obj=dummy_class
    app = App(control_obj=dummy_obj,esp_obj=dummy_obj,imager_obj=dummy_obj,terminal_buffer=dummy_obj)
    app.mainloop()

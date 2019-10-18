from tkinter import *

class ObstaclesFrame:
    def __init__(self, root, options):            
        self.options = options
        self.frame = Frame(root)

        num_of_obs = Label(self.frame, text="How many obstacles do you want?")
        num_of_obs.pack()
        
        self.add_option("None", "n")
        self.add_option("Low", "l")
        self.add_option("Medium", "m")
        self.add_option("High", "h")
        self.add_option("Crazy", "c")
        self.add_option("Bananas", "b")
        self.add_option("Insanity", "i")

        self.frame.pack()

    def add_option(self, value, alias):
        option_button = Button(self.frame, text=value, command=lambda:self.option_callback(alias))
        option_button.pack()

    def option_callback(self, value):
        self.value = value
        
        self.frame.destroy()
        self.options.nextFrame()

class WeaponFrame:
    def __init__(self, root, player_name, options):
        self.options = options
        self.frame = Frame(root)

        weapclass = Label(self.frame, text=player_name+": Pick your weapon class:")
        weapclass.pack()
        
        self.add_option("Trapper", "t")
        self.add_option("Necromancer", "n")
        self.add_option("Sub-Machine Gun", "smg")
        self.add_option("Machine Gun", "mg")
        self.add_option("Heavy Machine Gun", "hmg")
        self.add_option("Minigun", "mng")
        self.add_option("Super Sniper", "ss")
        self.add_option("Sniper", "s")
        self.add_option("Combat Shotgun", "cs")
        self.add_option("Pump-Action Shotgun", "ps")
        self.add_option("Random", "r")
        self.add_option("Burst(3)", "br")
        self.add_option("Burst(2)", "bp")
        self.add_option("Flame Thrower", "ft")
        self.add_option("Target Dummy", "td")
        self.add_option("Grenade Launcher", "gl")
        self.add_option("Dev ONLY", "D")
        
        

    def add_option(self, name, alias):
        option_button = Button(self.frame, text=name, command=lambda:self.option_callback(alias))
        option_button.pack()

    def option_callback(self, alias):
        self.value = alias
        
        self.frame.destroy()
        self.options.nextFrame()

class OptionsGUI:
    def __init__(self, root):
        self.root = root
        self.frames = []

    def nextFrame(self):
        self.frames.pop(0)

        if len(self.frames) > 0:
            self.frames[0].frame.pack()
        else:
            self.root.destroy()

root = Tk()
root.title("TANK 3.6.2")
root.geometry("250x435")

options = OptionsGUI(root)

obstacles_frame = ObstaclesFrame(root, options)
player1_weapon = WeaponFrame(root, "Player 1", options)
player2_weapon = WeaponFrame(root, "Player 2", options)

options.frames.append(obstacles_frame)
options.frames.append(player1_weapon)
options.frames.append(player2_weapon)

root.mainloop()

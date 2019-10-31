from tkinter import *
import json

player1_weapon = None
player2_weapon = None
obstacles_frame_answer = None
maps_frame_answer = None


class MapsFrame:
    def __init__(self, root, options):
        self.options = options
        self.frame = Frame(root)
        self.value = 'z'

        use_maps = Label(self.frame, text='Do you want to use a map?')
        use_maps.pack()

        self.add_option('Yes', 'y')
        self.add_option('No', 'n')
        self.frame.pack()

    def add_option(self, value, alias):
        option_button = Button(self.frame, text=value, command=lambda:self.option_callback(alias))
        option_button.pack()

    def option_callback(self, value):
        self.value = value

        global maps_frame_answer
        maps_frame_answer = self.value

        obstacles_frame = ObstaclesFrame(root, options, self.value)
        self.options.frames.append(obstacles_frame)
        
        self.frame.destroy()
        self.options.nextFrame()
        

class ObstaclesFrame:
    def __init__(self, root, options, maps_frame_answer):            
        self.options = options
        self.frame = Frame(root)
    
        if maps_frame_answer == 'n':
            num_of_obs = Label(self.frame, text='How many obstacles do you want to have?')
            num_of_obs.pack()

            self.add_option('None', 'n')
            self.add_option('Low', 'l')
            self.add_option('Medium', 'm')
            self.add_option('High', 'h')
            self.add_option('Crazy', 'c')
            self.add_option('Bananas', 'b')
            self.add_option('Insanity', 'i')
            
        elif maps_frame_answer == 'y':
            num_of_obs = Label(self.frame, text='Which map do you want to use?')
            num_of_obs.pack()
            
            with open('TANKMaps.json', 'r') as map_file:
                map_file_contents = map_file.read()
                map_dict = json.loads(map_file_contents)

            for key in map_dict.keys():
                self.add_option(key, key)

        self.frame.pack()

    def add_option(self, value, alias):
        option_button = Button(self.frame, text=value, command=lambda:self.option_callback(alias))
        option_button.pack()

    def option_callback(self, alias):
        self.value = alias
        
        global obstacles_frame_answer
        obstacles_frame_answer = self.value
        
        player1_weapon_frame = WeaponFrame(root, 'Player 1', options)
        self.options.frames.append(player1_weapon_frame)
        
        self.frame.destroy()
        self.options.nextFrame()
        

class WeaponFrame:
    def __init__(self, root, player_name, options):
        self.options = options
        self.frame = Frame(root)
        self.player_name = player_name

        weapclass = Label(self.frame, text=self.player_name+': Pick your weapon class:')
        weapclass.pack()
        
        self.add_option('Trapper', 't')
        self.add_option('Minelayer', 'ml')
        self.add_option('Necromancer', 'n')
        self.add_option('Sub-Machine Gun', 'smg')
        self.add_option('Machine Gun', 'mg')
        self.add_option('Heavy Machine Gun', 'hmg')
        self.add_option('Marksman Assault Rifle', 'mar')
        self.add_option('Minigun', 'mng')
        self.add_option('Super Sniper', 'ss')
        self.add_option('Sniper', 's')
        self.add_option('Combat Shotgun', 'cs')
        self.add_option('Pump-Action Shotgun', 'ps')
        self.add_option('Random', 'r')
        self.add_option('Burst Rifle', 'br')
        self.add_option('Burst Pistol', 'bp')
        self.add_option('Flame Thrower', 'ft')
        self.add_option('Target Dummy', 'td')
        self.add_option('Grenade Launcher', 'gl')
        self.add_option('Semi-Automatic Pistol', 'sap')
        self.add_option('Machine Pistol', 'mp')
        self.add_option('Homing Missile', 'hrpg')
        self.add_option('Thief', 'thf')
        self.add_option('Dev ONLY', 'D')

    def add_option(self, name, alias):
        option_button = Button(self.frame, text=name, command=lambda:self.option_callback(alias))
        option_button.pack()

    def option_callback(self, alias):
        self.value = alias

        if self.player_name == 'Player 1':
            global player1_weapon
            player1_weapon = self.value
            
            player2_weapon_frame = WeaponFrame(root, 'Player 2', options)
            self.options.frames.append(player2_weapon_frame)

        else:
            global player2_weapon
            player2_weapon = self.value
        
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
root.title('TANK 3.6.2')
root.geometry('250x591')

options = OptionsGUI(root)

maps_frame = MapsFrame(root, options)

options.frames.append(maps_frame)


root.mainloop()


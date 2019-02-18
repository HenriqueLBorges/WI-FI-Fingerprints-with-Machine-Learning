import os

path = ' ./audio/files'
command = 'aplay'
intersections = ['E-C', 'C-B', 'B-A', 'A-E']

#Plays a instruction audio.
def instruction(destination):
    os.system(command + path + '/sentences/head_to.wav')

    if destination in intersections:
        os.system(command + path + '/sentences/to_intersection.wav')
        os.system(command + path + '/intersections/' + destination + '.wav')
    else: 
        os.system(command + path + '/sentences/to_room.wav')
        os.system(command + path + '/rooms/' + destination + '.wav')    

#Plays room audio.
def room(room):
    os.system(command + path + '/rooms/' + room + '.wav') 

#Plays recalculating route audio.
def recalculating():
    os.system(command + path + '/sentences/recalculating.wav') 

#Plays route error audio.
def routeError():
    os.system(command + path + '/sentences/route_error.wav') 

#Plays wrong position audio.
def wrongPosition():
    os.system(command + path + '/sentences/wrong_position.wav') 

#Plays confirm audio.
def confirm():
    os.system(command + path + '/sentences/confirm.wav') 

#Plays cancel audio.
def cancel():
    os.system(command + path + '/sentences/cancel.wav') 

#Plays a input destination audio.
def inputDestination():
    os.system(command + path + '/sentences/input_destination.wav') 

#Plays a current location audio.
def currentLocation():
    os.system(command + path + '/sentences/current_location.wav') 

#Plays a destination audio.
def destination():
    os.system(command + path + '/sentences/destination.wav') 

#Plays a greeting audio.
def greetings():
    os.system(command + path + '/sentences/greetings.wav')   

#Plays a finish audio.
def finish():
    os.system(command + path + '/sentences/finish.wav')  

#Plays a number audio.
def number(number):
    os.system(command + path + '/numbers/' + number + '.wav')  

#Plays a letter audio.
def letter(letter):
    os.system(command + path + '/letters/' + letter + '.wav') 

#Plays a direction audio.
def direction(direction):
    os.system(command + path + '/directions/' + direction + '.wav') 

#Plays a compass error.
def compassError():
    os.system(command + path + '/sentences/compass_error.wav') 

#Plays a compass error.
def configError():
    os.system(command + path + '/sentences/config_error.wav') 

#Plays a turn right audio.
def turnRight():
    os.system(command + path + '/sentences/turn_right.wav') 

#Plays a turn left audio.
def turnLeft():
    os.system(command + path + '/sentences/turn_left.wav') 

#Plays a in front of audio
def frontOf():
    os.system(command + path + '/sentences/front_warning.wav') 
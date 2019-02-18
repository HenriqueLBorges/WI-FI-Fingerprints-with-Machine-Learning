import sys,tty,termios
import audio.audio as audio

'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#confirm button
confirm = 1
GPIO.setup(confirm, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#cancel button
cancel = 25
GPIO.setup(cancel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#left button
left = 8
GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#right button
right = 7
GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Returns the button pressed 
def get():
    while True:
        input = True

        input = GPIO.input(confirm)
        if input == False:
            return 'confirm'

        input = GPIO.input(cancel)
        if input == False:
            return 'cancel'

        input = GPIO.input(left)
        if input == False:
            return 'left'

        input = GPIO.input(right)
        if input == False:
            return 'right'

           
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
'''
def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
        
    if k=='\x1b[A':
        return "confirm"
    elif k=='\x1b[B':
        return "cancel"
    elif k=='\x1b[C':
        return "right"
    elif k=='\x1b[D':
        return "left"
    else:
        return "not an arrow key!"

def inputRoom():
    letters = ['A', 'B', 'C', 'E']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letter_index = 0
    number_index = 0
    room = ''

    #Gets the first letter.
    while True:
        key = get()
        if key == 'right':
            if letter_index == len(letters) - 1:
                letter_index = 0
            else:
                letter_index += 1

            #audio feedback
            audio.letter(letters[letter_index])

            print letters[letter_index]
            
        elif key == 'left':
            if letter_index == 0:
                letter_index = len(letters) - 1
            else:
                letter_index -= 1

            #audio feedback
            audio.letter(letters[letter_index])

            print letters[letter_index]

        elif key == 'cancel':
            #audio feedback
            audio.cancel()
            break

        elif key == 'confirm':
            #audio feedback
            audio.confirm()

            room = letters[letter_index]
            print 'room = ' + room

            #Gets the first number.
            while True:
                key = get()
                if key == 'right':
                    if number_index == len(numbers) - 1:
                        number_index = 0
                    else:
                        number_index += 1
                    
                    #audio feedback
                    audio.number(numbers[number_index])

                    print numbers[number_index]
                    
                elif key == 'left':
                    if number_index == 0:
                        number_index = len(numbers) - 1
                    else:
                        number_index -= 1

                    #audio feedback
                    audio.number(numbers[number_index])

                    print numbers[number_index]
                
                elif key == 'cancel':
                    #audio feedback
                    audio.cancel()
                    room = room[:1] + room[1+1:]
                    break

                elif key == 'confirm':
                    #audio feedback
                    audio.confirm()

                    #audio feedback
                    audio.number(numbers[number_index])

                    room += numbers[number_index]
                    print 'room = ' + room

                    #Gets the second number.
                    while True:
                        key = get()
                        if key == 'right':
                            if number_index == len(numbers) - 1:
                                number_index = 0
                            else:
                                number_index += 1

                            #audio feedback
                            audio.number(numbers[number_index])

                            print numbers[number_index]
                            
                        elif key == 'left':
                            if number_index == 0:
                                number_index = len(numbers) - 1
                            else:
                                number_index -= 1

                            #audio feedback
                            audio.number(numbers[number_index])

                            print numbers[number_index]

                        elif key == 'cancel':
                            #audio feedback
                            audio.cancel()
                            room = room[:2] + room[2+1:]
                            break

                        elif key == 'confirm':       
                            #audio feedback
                            audio.confirm()
                            
                            room += numbers[number_index]
                            print 'room = ' + room

                            #Gets the third number.
                            while True:
                                key = get()
                                if key == 'right':
                                    if number_index == len(numbers) - 1:
                                        number_index = 0
                                    else:
                                        number_index += 1

                                    #audio feedback
                                    audio.number(numbers[number_index])

                                    print numbers[number_index]
                                    
                                elif key == 'left':
                                    if number_index == 0:
                                        number_index = len(numbers) - 1
                                    else:
                                        number_index -= 1

                                    #audio feedback
                                    audio.number(numbers[number_index])

                                    print numbers[number_index]

                                elif key == 'cancel':
                                    #audio feedback
                                    audio.cancel()
                                    room = room[:3] + room[3+1:]
                                    break

                                elif key == 'confirm':
                                    #audio feedback
                                    audio.confirm()

                                    room += numbers[number_index]
                                    print 'room = ' + room
                                    return room

def main():
    print 'input = ' + str(inputRoom())

if __name__=='__main__':
    main()
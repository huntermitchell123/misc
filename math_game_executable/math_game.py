### Hunter Mitchell - 11/11/20

### Description: A little math game to test your quick math abilities using the curses library in python


import curses
import random
import time

# returns an easy, medium, or hard math equation string with the answer
def get_equation(difficulty):
    if difficulty == 'easy':
        first_number = random.randint(5,20) # easy addition
        second_number = random.randint(5,20)
        answer = first_number + second_number
        return '{} + {} ='.format(first_number,second_number), answer

    elif difficulty == 'medium':
        operator = random.randint(1,2)
        if operator == 1:
            first_number = random.randint(3,12) # medium multiplication
            second_number = random.randint(3,12)
            answer = first_number * second_number
            return '{} * {} ='.format(first_number,second_number), answer
        else:
            first_number = random.randint(10,30) # medium addition
            second_number = random.randint(10,30)
            answer = first_number + second_number
            return '{} + {} ='.format(first_number,second_number), answer

    else:
        operator = random.randint(1,3)
        if operator == 1:
            first_number = random.randint(30,100) # hard addition
            second_number = random.randint(30,100)
            answer = first_number + second_number
            return '{} + {} ='.format(first_number,second_number), answer
        if operator == 2:
            first_number = random.randint(50,70) # hard subtraction
            second_number = random.randint(20,40)
            answer = first_number - second_number
            return '{} - {} ='.format(first_number,second_number), answer
        else:
            first_number = random.randint(4,15) # hard multiplication
            second_number = random.randint(4,12)
            answer = first_number * second_number
            return '{} * {} ='.format(first_number,second_number), answer


# play function of varying difficulty
def play(stdscr,difficulty):

    stdscr.clear()

    # Get window height & width
    height, width = stdscr.getmaxyx()

    title = "Answer the problems to beat your opponent to the finish!"

    # get various x,y coordinates according to user's window size 
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_y_title = int((height // 4) - 2)

    start_x_problem = int((width // 2) - 4)
    start_y_problem = int((3*height // 4))

    enemy_x = int(width // 8)
    enemy_y = int((height // 2) - 1) 

    x = int(width // 8)
    y = int((height // 2) + 1)

    x_finish = int((width // 8) * 7)

    finished = False

    winner = False

    while (finished == False): # iterate until user finishes game

        stdscr.addstr(start_y_title, start_x_title, title)

        stdscr.addstr(enemy_y + -2, x_finish - 3, 'Finish')
        stdscr.addstr(enemy_y + -1, x_finish, '|')
        stdscr.addstr(enemy_y     , x_finish, '|')
        stdscr.addstr(enemy_y +  1, x_finish, '|')
        stdscr.addstr(enemy_y +  2, x_finish, '|')
        stdscr.addstr(enemy_y +  3, x_finish, '|')

        # get initial equation
        problem, actual_answer = get_equation(difficulty=difficulty)

        stdscr.addstr(start_y_problem, start_x_problem, problem)

        temp = 1

        stdscr.nodelay(True) # make sure it doesnt stop to get a character

        user_answer = ""

        while (enemy_x < x_finish - 4 and x < x_finish - 4):

            key = stdscr.getch()

            stdscr.addstr(enemy_y, enemy_x, '>[~~]>')

            stdscr.addstr(y, x, '>[~~]>')

            # how often the enemy moves forward - it's faster when the difficulty is harder
            if difficulty == 'easy':
                if temp % 20000 == 0:
                    enemy_x = enemy_x + 1
            if difficulty == 'medium':
                if temp % 10000 == 0:
                    enemy_x = enemy_x + 1
            if difficulty == 'hard':
                if temp % 7500 == 0:
                    enemy_x = enemy_x + 1
            
            temp = temp + 1

            stdscr.refresh()

            if key == 10: # user presses enter
                if user_answer == str(actual_answer): # correct answer
                    stdscr.addstr(y, x, '>>>>>>>>>>>')
                    x=x+10
                    stdscr.addstr(y, x, '>[~~]>') # moves user forward

                    problem, actual_answer = get_equation(difficulty=difficulty) # get new equation
                    stdscr.addstr(start_y_problem, start_x_problem, "          ")
                    stdscr.addstr(start_y_problem, start_x_problem, problem) # overwrite old equation
                    stdscr.addstr(start_y_problem, start_x_problem + 10, "          ")
                    user_answer = ""

                else: # incorrect answer
                    user_answer = ""
                    stdscr.addstr(start_y_problem, start_x_problem + 10, "          ")

            elif key == 127: # user presses backspace
                user_answer = user_answer[:-1]
                stdscr.addstr(start_y_problem, start_x_problem + 10, "          ")

            elif key != -1: # user adds character to their answer
                user_answer = user_answer + str(chr(key))


            stdscr.addstr(start_y_problem, start_x_problem + 10, user_answer) # update user answer


        finished = True

        if x >= x_finish - 4: # check if user won or lost
            winner = True

    stdscr.clear()

    if winner == True:
        title = 'Congratulations! You won!'
    else:
        title = 'You lost! Better luck next time!'
    
    subtitle = 'Press any key to continue'

    height, width = stdscr.getmaxyx()

    stdscr.addstr(int((height // 2) - 2) - 1, int((width // 2) - (len(title) // 2) - len(title) % 2), title)
    stdscr.addstr(int((height // 2) - 2) + 2, int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2), subtitle)

    stdscr.nodelay(False) # pause until user enters a character

    stdscr.getch()

    curses.wrapper(main) # back to main function


# main menu
def main(stdscr):

    k = 0

    # clear and refresh
    stdscr.clear()
    stdscr.refresh()

    while (k not in [ord('q'),ord('1'),ord('2'),ord('3')]): # repeat until user enters an option

        # Get window height & width
        height, width = stdscr.getmaxyx()

        # Decorate main menu
        title = "Welcome to Hunter's awesome math game!"
        subtitle1 = "Press \'1\' to play on Easy"
        subtitle2 = "Press \'2\' to play on Medium"
        subtitle3 = "Press \'3\' to play on Hard"
        subtitle4 = "Press \'q\' to quit"

        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle1) // 2) - len(subtitle1) % 2)
        start_y = int((height // 2) - 2)

        stdscr.addstr(start_y - 1, start_x_title, title)
        stdscr.addstr(start_y + 2, start_x_subtitle, subtitle1)
        stdscr.addstr(start_y + 3, start_x_subtitle, subtitle2)
        stdscr.addstr(start_y + 4, start_x_subtitle, subtitle3)
        stdscr.addstr(start_y + 5, start_x_subtitle, subtitle4)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    if k == ord('1'):
        play(stdscr,difficulty='easy')
    elif k == ord('2'):
        play(stdscr,difficulty='medium')
    elif k == ord('3'):
        play(stdscr,difficulty='hard')
    else:
        pass




if __name__ == "__main__":
    curses.wrapper(main)
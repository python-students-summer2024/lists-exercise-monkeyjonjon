'''
Stores the functions needed for mood assessing.
'''
from pathlib import Path
import datetime

def create_diary_file():
    '''
    Ensures the file for mood recording exists, if not, it will make it.
    '''
    filepath = Path("data/mood_diary.txt")
    diary_file = open(filepath, encoding="utf-8", mode="a")
    diary_file.close()

def get_diagnosis():
    '''
    Checks if there are at least 7 entries in diary_file and evaluates a diagnosis.
    '''
    ## Appends data to an empty list (data_list)
    data_list = []
    mood_list = []
    average_mood_value = 0
    filepath = Path("data/mood_diary.txt")
    diary_file = open(filepath, encoding="utf-8", mode="r")
    for line in diary_file:
        line = line.strip()
        data = line.split(':')
        data = [item.strip() for item in data]
        data_list.append(data)
    ## Counts data of last week
    if len(data_list) >= 7:
        recent_data = data_list[-1:-8:-1]
        for index in range(7):
            entry = recent_data[index][1]
            entry = entry.strip()
            average_mood_value += int(entry)
            mood_list.append(entry)
        ## Set up the mood counters
        # UPDATE: It seems that the data in the lists were strings, interesting
        happy_counter = mood_list.count('2')
        #relaxed_counter = mood_list.count(1)
        apathetic_counter = mood_list.count('0')
        sad_counter = mood_list.count('-1')
        #angry_counter = mood_list.count(-2)
        ## Calculates the average mood
        average_mood_value = round(average_mood_value/7)
        if average_mood_value == 2:
            average_mood = 'happy'
        elif average_mood_value == 1:
            average_mood = 'relaxed'
        elif average_mood_value == 0:
            average_mood = 'apathetic'
        elif average_mood_value == -1:
            average_mood = 'sad'
        elif average_mood_value == -2:
            average_mood = 'angry'
        ## Diagnoses accordingly
        if happy_counter >= 5:
            diagnosis = 'maniac'
        elif sad_counter >= 4:
            diagnosis = 'depressive'
        elif apathetic_counter >= 6:
            diagnosis = 'schizoid'
        else:
            diagnosis = average_mood
        return diagnosis

def check_if_mood_is_recorded():
    '''
    Checks if the user has recorded their mood for today.
    '''
    ## Gets the date
    filepath = Path("data/mood_diary.txt")
    date_today = datetime.date.today()
    date_today = str(date_today)
    ## Reads through the data lines checking for date
    diary_file = open(filepath, encoding="utf-8", mode="r")
    for line in diary_file:
        line = line.strip()
        data = line.split(':')
        ## Today's date has been found.
        if date_today in data:
            return True

def get_user_input():
    '''
    Gets and records the user's mood.
    '''
    reminder_token = 0
    recording_mood = True
    valid_moods = ['happy', 'relaxed', 'apathetic', 'sad', 'angry']
    ## Loops until it gets a valid input
    while recording_mood:
        if reminder_token >= 9:
            print("You're sadistic!")
            exit()
        if reminder_token >= 3:
            print("Remember! Valid inputs are: (happy), (relaxed), (apathetic), (sad) and (angry).")
        user_response = input("Hiya! How are you feeling today? ")
        user_response = user_response.strip().lower()
        ## This line of code isn't needed to work, but I personally think it adds readibility.
        if user_response in valid_moods:
            if user_response == valid_moods[0]:
                user_mood = 2
            elif user_response == valid_moods[1]:
                user_mood = 1
            elif user_response == valid_moods[2]:
                user_mood = 0
            elif user_response == valid_moods[3]:
                user_mood = -1
            elif user_response == valid_moods[4]:
                user_mood = -2
            recording_mood = False
            return user_mood
        else:
            reminder_token += 1

def record_mood(mood):
    '''
    Takes the an argument(mood) and records it into the mood_diary file.
    '''
    date_today = datetime.date.today()
    date_today = str(date_today)
    filepath = Path("data/mood_diary.txt")
    diary_file = open(filepath, encoding="utf-8", mode="a")
    diary_file.write(date_today)
    # For seperating date and mood values
    diary_file.write(':')
    diary_file.write(str(mood))
    diary_file.write("\n")
    diary_file.close()

def assess_mood():
    '''
    Initiates a mood_diary if it doesn't exist.
    or else if 7 days of moods are already recorded, evaluates a diagnosis.
    If less than 7 days are recorded,
    checks if today's mood has been recorded,
    either stops the user from further inputting or asks for their mood to record.
    '''
    create_diary_file()
    ## Checks if today's mood has been recorded
    mood_is_recorded = check_if_mood_is_recorded()
    if mood_is_recorded:
        #print("You've already input your mood for today!\nPlease come back tommorow. ;)")
        print("Sorry, you have already entered your mood today.")
    else:
        user_mood = get_user_input()
        if user_mood == 2:
            # RIP print("Happy, happy, happy!") I think this messed up the tests.
            print("Joy, joy, joy!")
        elif user_mood == 1:
            print("That's great!")
        elif user_mood == 0:
            print("Remember to go outside and touch grass!")
        elif user_mood == -1:
            print("That's unfortunate. Cheer up!")
        elif user_mood == -2:
            print("Calm down!")
        record_mood(user_mood)
    diagnosis = get_diagnosis()
    if diagnosis is None:
        # Ensures this is only printed after the user inputs their mood.
        if not mood_is_recorded:
            print("Thanks for coming! Remember to come back tomorrow!")
    else:
        print(f"Your diagnosis: {diagnosis}!")

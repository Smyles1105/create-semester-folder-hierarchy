from os import mkdir


def getSetting(weeks):
    inp = input("Every week, every two weeks, custom step, or manual? (0, 1, 2, or 3): ")
    setting = int(inp.strip())
    return setting


def getStartWeeks(s, wks, folder_num, task_type):
    starts = list()
    wksLst = list()

    #creates a indexable list, 1 index for each week in the semester
    for i in range(1, wks + 1):
        wksLst.append(i)
    new_weeks = wksLst

    first_week = int(input("Enter first week for pattern to start from: "))
    if s == 0: #Weekly
        starts = new_weeks[first_week-1:]

    elif s == 1: #Biweekly
        starts = new_weeks[first_week-1::2]

    elif s == 2: #Custom solid frequency
        step = int(input("Enter step for pattern: "))
        starts = new_weeks[first_week-1:first_week + step*(folder_num-1):step]

    else: #Completely manual
        for a in range(folder_num):
            week = int(input(f"Please enter the start week of {task_type}_{a + 1}"))
            starts.append(week)

    if len(starts) > folder_num:
        starts = starts[:folder_num]
    return starts


program_description = (
    "This program allows the user to create a multi-level directory for a class that creates folders for the number of assignments, labs, projects, etc.")
answer = "y"
#allows user to create multiple classes worth of folders
while answer == "y":

    #directory and dictionary information
    directory = input("Please enter a directory for creating a class folder (no quotes): ")
    directory.replace('\\', "/")
    class_info = {
        "week": 0,
        "assignment": 0,
        "project": 0,
        "lab": 0,
        "lecture": 0
    }
    keys = list(class_info.keys())

    # creates initial folder
    class_name = input('Please enter the name of the class: ')
    mkdir(f"{directory}/{class_name}")

    # creates folders for each week
    weeks = int(input("Please enter the number of weeks in the syllabus/course: "))
    for i in range(weeks):
        mkdir(f"{directory}/{class_name}/Week_{i + 1}")

    # Each iteration creates folders for a task type of a specific numebr and in specific weeks
    for i in range(1, len(class_info)):
        folder_type = keys[i]

       #Getting info for file names
        number_of_folders = int(input(f"Please enter the number of {folder_type}s you'd like to create: "))
        option = getSetting(weeks)
        #print(option)
        start_weeks = getStartWeeks(option, weeks, number_of_folders, folder_type)

        #Logic for new start_week_list if multiple folders per week
        if number_of_folders > weeks:
            #print(number_of_folders, " > ", weeks)
            repeats = number_of_folders / weeks
            new_start_weeks = list()
            for a in range(len(start_weeks)):
                for b in range(1, round(repeats + 1)):
                    new_start_weeks.append(start_weeks[a])
            start_weeks = new_start_weeks

        # iterates through once for each folder of a specific type and makes them in their start week folder.
        #print(start_weeks)
        for c in range(1, len(start_weeks)+1):
            folder_directory = f"{directory}/{class_name}/Week_{start_weeks[c-1]}/{folder_type}_{c}"
            #print(folder_directory)
            mkdir(folder_directory)
    answer = input('Do you want to create another set of folders for another class (y/n)? ').lower().strip()

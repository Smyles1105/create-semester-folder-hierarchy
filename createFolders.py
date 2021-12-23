from itertools import repeat
from os import mkdir

CLASS_INFO = {
    "CLASSNAME": "Class",
    "ASSIGNMENT": 0,
    "PROJECT": 0,
    "LAB": 0,
    "LECTURE": 0
}


def verifyInput(prompt, mode):  # TODO FINISH
    input_is_verified = False
    while input_is_verified is not True:
        if mode == "i0" or mode == "i1":
            try:
                inp = int(input(prompt).strip())
                if (mode == 'i0' and inp >= 0) or (mode == 'i1' and inp > 0):
                    input_is_verified = True
                    return inp
                else:
                    print("Input is not in valid range, please try again")
            except:
                print("Input is empty, try again.")
        elif mode == "s":
            try:
                inp = input(prompt).strip()
                input_is_verified = True
                return inp
            except:
                print("Input is empty, try again")
    return inp


def get_class_name():
    class_name = verifyInput("Enter Class Name: ", 's')
    return class_name


def get_class_count():
    class_count = verifyInput("Enter number of classes: ", 'i1')
    return class_count


def create_classes_dictionary(class_count, s_l):
    info_keys = list(CLASS_INFO.keys())
    classes_dict = {}
    for i in range(class_count):
        class_name = get_class_name()
        class_dict = CLASS_INFO.copy()
        for (key, value) in class_dict.items():
            if key != "CLASSNAME":
                task_dict = {}
                task_number = get_task_number(key)
                setting = get_setting()
                task_locations = get_task_locations(task_number, setting, key, s_l)
                task_dict.update({"count": task_number})
                task_dict.update({"locations": task_locations})
                class_dict.update({key: task_dict})
            else:
                value = class_name
                class_dict.update({key: value})
        classes_dict.update({class_name: class_dict})
    return classes_dict


def get_directory():
    directory = verifyInput("Please enter a directory: ", 's')
    return directory


def get_task_number(key):
    # This function requests the number of folders for any given task, defined by key.
    task_number = verifyInput(f"How many {key} folders do you want: ", 'i0')
    return task_number


def get_semester_length():
    semester_length = verifyInput("How many weeks in the semester: ", 'i1')
    return semester_length


def get_setting():
    setting = verifyInput("Weekly, Biweekly, custom step or manual (0, 1, 2, 3) ", 'i0')
    return setting


def calculate_repeats(num_of_tasks, s_l):
    if num_of_tasks > s_l:
        repeats = round(num_of_tasks / s_l)
    else:
        repeats = 1
    return repeats

def get_task_locations(number_of_tasks, setting, key, s_l):
    task_locations = []
    if setting in range(3):
        first_week = verifyInput("Enter first week: ", 'i1')
        if setting == 2:
            step = verifyInput("Enter step: ", 'i1')
        else:
            step = setting + 1
        repeats = calculate_repeats(number_of_tasks, s_l)
        task_locations = list(list(repeat(x, repeats) for x in range(
            first_week, round(number_of_tasks * step / repeats) + 1, step)))
        return task_locations
    else:
        task_locations = list(verifyInput(f"Enter start week of {key}_{x + 1}: ", 'i1')
                              for x in range(number_of_tasks))
        task_locations = [task_locations]
    return task_locations


def create_folders(classes_dict, s_l, dir):
    for c_name, c_info in classes_dict.items():

        for c_info_name, c_info_val in c_info.items():

            if c_info_name == "CLASSNAME":
                class_name = c_info_val
                mkdir(f"{dir}/{class_name}")
                for i in range(s_l):
                    mkdir(f"{dir}/{class_name}/Week_{i + 1}")

            if c_info_name != "CLASSNAME":

                for task_info_name, task_info_val in c_info_val.items():
                    task_type = c_info_name

                    if task_info_name == "locations":
                        a = 1

                        for location_set in task_info_val:

                            for location in location_set:
                                folder_directory = f"{dir}/{class_name}/Week_{location}/{task_type}_{a}"
                                mkdir(folder_directory)
                                a += 1


def main():
    dir = get_directory()
    count = get_class_count()
    sem_len = get_semester_length()
    c_dict = create_classes_dictionary(count, sem_len)
    create_folders(c_dict, sem_len, dir)
    print("Class Folders Created! Goodbye!")


main()

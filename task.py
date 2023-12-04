import time  # For Timer
import random  # For choosing a random word
import plyer  # For displaying notification
from PyDictionary import PyDictionary  # For meaning
import winsound  # For beep sound
import threading  # To make both menu and reminder work simultaneously

# Create a dictionary object for fetching word meanings
dictionary = PyDictionary()

# Path of the wordlist file
wordlist_path = r'C:\Users\RAIKAT\OneDrive\Documents\Task Reminder\dataset.txt'

# Function to load words from the wordlist file
def load_wordlist(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

def word_list() :
    wordlist = load_wordlist(wordlist_path)
    num_random_words = 10
    random_words = random.sample(wordlist, num_random_words) # Function to generate random words
    return random_words[0]  # Select the first word from the list

# Function to show a reminder notification
def show_reminder(task):
    # Beep sound before the notification
    winsound.Beep(4000, 200)
    winsound.Beep(4000, 200)

    # Notifying about the reminder
    plyer.notification.notify(
        title="Task Reminder",
        message=f"Reminder: {task}",
        timeout=10
    )

    # Showing a new word everytime
    vocabulary()

# Function for vocabulary
def vocabulary():
    try:
        word = word_list()
        meaning = dictionary.meaning(word)
        if meaning:
            plyer.notification.notify(
                title="Word of the Day",
                message=f"Word: {word}\nMeaning: {meaning}",
                timeout=15
            )
    except Exception as e:
        print(f"An error occurred while enriching vocabulary: {str(e)}")

# Initializing an empty dictionary for tasks
tasks = {}

# Function to add a task and its reminder time
def add_task():
    task_name = input("Enter the task: ")
    task_time = input("Enter the reminder time (HH:MM format): ")
    tasks[task_name] = task_time
    print(f"\n{task_name} added successfully.")

# Function to remove a task
def remove_task():
    task_name = input("Enter the task name to remove: ")
    if task_name in tasks:
        del tasks[task_name]
        print(f"\n{task_name} removed successfully.")
    else:
        print(f"\n{task_name} not found in the task list.")

# Function to edit a task's reminder time
def edit_task():
    task_name = input("Enter the task name to edit: ")
    if task_name in tasks:
        new_task_time = input(f"Enter the new reminder time for {task_name} (HH:MM format): ")
        tasks[task_name] = new_task_time
        print(f"\n{task_name}'s reminder time updated successfully.")
    else:
        print(f"\n{task_name} not found in the task list.")

# Function to display all tasks
def display_tasks():
    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\n\nTask list:\n")
        for task, task_time in tasks.items():
            print(f"{task}: {task_time}")

# Function to search for a task
def search_task():
    keyword = input("Enter a keyword to search for a task: ")
    found = False
    for task, task_time in tasks.items():
        if keyword in task:
            print(f"\nTask: {task}, Reminder Time: {task_time}")
            found = True
    if not found:
        print(f"No tasks found containing the keyword '{keyword}'.")

# Function to run the reminder loop
def reminder():
    end_time = time.time() + 24 * 60 * 60  # 24 hours in seconds
    while time.time() < end_time:
        current_time = time.strftime("%H:%M")

        # Check for reminders
        for task, task_time in tasks.items():
            if current_time == task_time:
                show_reminder(task)

        # Sleep for 60 seconds before checking again
        time.sleep(60)

# Function of menu
def menu():
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Edit Task")
        print("4. Display Tasks")
        print("5. Search Task")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            remove_task()
        elif choice == "3":
            edit_task()
        elif choice == "4":
            display_tasks()
        elif choice == "5":
            search_task()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

# Menu
menu_thread = threading.Thread(target=lambda: menu())
menu_thread.start()

# Reminder loop
reminder_thread = threading.Thread(target=lambda: reminder())
reminder_thread.start()

# Wait for both threads to finish
menu_thread.join()
reminder_thread.join()
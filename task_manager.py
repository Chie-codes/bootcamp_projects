# ===== Importing external modules ===========
"""
Imports date and datetime classes from Python's built-in datetime module.

These classes are used for handling and formatting date-related operations
throughout the program, such as assigning task dates, validating deadlines,
and generating reports.
"""


from datetime import date, datetime

# ==== Login Section ====
credentials = {}
try:
    with open("user.txt", "r", encoding="utf-8") as file:
        file.seek(0)
        for line in file:
            username, password = line.strip().split(", ")
            credentials[username] = password
except FileNotFoundError:
    print("Error: 'user.txt' file not found.")
    exit()

# Validate user login
while True:
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if username in credentials and credentials[username] == password:
        print(f"Welcome, {username}!")
        break
    else:
        print("Invalid username or password. Please try again.")

# After successful login
current_user = username
is_admin = current_user == "admin"


# ==== Function Definitions ====
def reg_user():
    """
    Registers a new user to the system.

    This function can only be accessed by an admin user. It prompts for a new
    username and password, checks for duplicates, and writes the new
    credentials
    to 'user.txt'.

    Parameters:
        None (relies on input prompts and current user context)

    Returns:
        None (writes to 'user.txt' and prints confirmation messages)
    """
    if not is_admin:
        print("Only the admin can register new users.")
        return

    while True:
        prompt = "Enter new username (or type 'cancel' to exit): "
        new_username = input(prompt).strip()

        if new_username.lower() == 'cancel':
            print("Registration cancelled.")
            return

        if new_username in credentials:
            print("Username already exists. Please choose a different one.")
            continue
        else:
            break

    while True:
        new_password = input("Enter new password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match. Try again.")
        else:
            break

    with open("user.txt", "a", encoding="utf-8") as record_file:
        record_file.write(f"{new_username}, {new_password}\n")

    credentials[new_username] = new_password
    print(f"User '{new_username}' registered successfully.")


def add_task():
    """
    Prompts the user to input details for a new task and appends it to the
    'tasks.txt' file.

    The function performs the following steps:
    - Asks for the username to assign the task to and checks if it exists in
      the credentials.
    - Collects the task title, description, and due date from the user.
    - Validates the due date format ('DD Mon YYYY').
    - Automatically sets the assigned date to today's date and marks the task
      as incomplete.
    - Writes the task details to the 'tasks.txt' file in a comma-separated
      format.

    Returns:
        None

    Effects
        - Prints messages to the console based on input validation and task
          creation status.
        - Appends a new line to 'tasks.txt' if all inputs are valid.
    """

    assigned_to = input("Enter the username to assign the task to: ").strip()
    if assigned_to not in credentials:
        print("User does not exist.")
        return

    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    try:
        due_date = input("Enter due date (e.g. 10 Oct 2019): ").strip()
        datetime.strptime(due_date, "%d %b %Y")
    except ValueError:
        print("Invalid date format. Please use 'DD Mon YYYY'.")
        return

    assigned_date = date.today().strftime("%d %b %Y")
    completed = "No"

    with open("tasks.txt", "a", encoding="utf-8") as source:
        source.write(
            f"{assigned_to}, {title}, {description}, "
            f"{assigned_date}, {due_date}, {completed}\n"
                  )

    print("Task added successfully.")


def view_all():
    """
    Displays all tasks stored in 'tasks.txt'.

    Reads each line from the file, splits it into task components, and prints
    the details in a readable format. Skips any malformed lines that do not
    contain the expected number of fields.

    Parameters:
        None

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r", encoding="utf-8") as transcript:
            tasks = transcript.readlines()
            if not tasks:
                print("No tasks found.")
                return
            for i, task in enumerate(tasks, 1):
                task_parts = task.strip().split(", ")

                if len(task_parts) < 6:
                    task_parts = task.strip().split(", ")
                    continue

                assigned_to = task_parts[0]
                title = task_parts[1]
                description = task_parts[2]
                assigned_date = task_parts[3]
                due_date = task_parts[4]
                completed = task_parts[5]

                print(f"\n Task {i}")
                print(f"Assigned to: {assigned_to}")
                print(f"Assigned Date: {assigned_date}")
                print(f"Title: {title}")
                print(f"Description: {description}")
                print(f"Due Date: {due_date}")
                print(f"Completed: {completed}")
    except FileNotFoundError:
        print("No tasks file found.")


def view_mine(current_user):
    """
    Displays and manages tasks assigned to the current user.

    Allows the user to view their tasks, mark them as complete, or edit the
    assignee and due date. Only incomplete tasks can be edited. Updates are
    written back to 'tasks.txt'.

    Parameters:
        current_user (str): The username of the currently logged-in user.

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r", encoding="utf-8") as readout:
            tasks = readout.readlines()

        user_tasks = [task for task in tasks if task.startswith(current_user + ",")]

        if not user_tasks:
            print("You have no tasks assigned.")
            return

        while True:
            print("\nYour Tasks:")
            for i, task in enumerate(user_tasks, 1):
                task_parts = task.strip().split(", ")
                print(f"\nTask {i}:")
                print(f"Assigned to: {task_parts[0]}")
                print(f"Title: {task_parts[1]}")
                print(f"Description: {task_parts[2]}")
                print(f"Assigned Date: {task_parts[3]}")
                print(f"Due Date: {task_parts[4]}")
                print(f"Completed: {task_parts[5]}")

            selection = input("\nEnter task number to manage or '-1' to return to menu: ").strip()
            if selection == "-1":
                break
            if not selection.isdigit() or not (1 <= int(selection) <= len(user_tasks)):
                print("Invalid selection.")
                continue

            task_index = int(selection) - 1
            task_parts = user_tasks[task_index].strip().split(", ")

            if task_parts[-1].lower() == "yes":
                print("This task is already completed and cannot be edited.")
                continue

            action = input("Enter 'c' to mark complete or 'e' to edit: ").strip().lower()

            if action == "c":
                task_parts[-1] = "Yes"
                print("Task marked as complete.")

            elif action == "e":
                current_assignee = task_parts[0]
                new_user = input(f"Enter new username (or press Enter to keep '{current_assignee}'): ").strip()
                new_due = input(f"Enter new due date (DD Mon YYYY) (or press Enter to keep '{task_parts[4]}'): ").strip()

                if new_user:
                    if new_user not in credentials:
                        print("Username does not exist.")
                        continue
                    task_parts[0] = new_user

                if new_due:
                    try:
                        datetime.strptime(new_due, "%d %b %Y")
                        task_parts[4] = new_due
                    except ValueError:
                        print("Invalid date format.")
                        continue

                print("Task updated.")

            else:
                print("Invalid action.")
                continue

            # Update the full task list
            original_task = user_tasks[task_index]
            updated_task = ", ".join(task_parts) + "\n"
            user_tasks[task_index] = updated_task
            tasks[tasks.index(original_task)] = updated_task

            # Write updated task back to file
            with open("tasks.txt", "w", encoding="utf-8") as data_file:
                data_file.writelines(tasks)

    except FileNotFoundError:
        print("Error: 'tasks.txt' file not found.")


def view_completed():
    """
    Displays all completed tasks from 'tasks.txt'.

    Filters tasks that end with 'Yes' (indicating completion) and prints
    their details. Skips display if no completed tasks are found.

    Parameters:
        None

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r", encoding="utf-8") as text_file:
            tasks = text_file.readlines()
            completed_tasks = [
                t for t in tasks if t.strip().endswith("Yes")
            ]
            if not completed_tasks:
                print("No completed tasks found.")
                return

            for i, task in enumerate(completed_tasks, 1):
                assigned_to, title, desc, date_assigned, due, done = (
                    task.strip().split(", ")
                )

                print(f"\nTask {i}:")
                print(f"Assigned to: {assigned_to}")
                print(f"Title: {title}")
                print(f"Description: {desc}")
                print(f"Assigned Date: {date_assigned}")
                print(f"Due Date: {due}")
                print(f"Completed: {done}")

    except FileNotFoundError:
        print("No tasks file found.")


def delete_task():
    """
    Allows the user to delete a task from 'tasks.txt'.

    Displays all valid tasks with their details, skipping any malformed
    entries. Prompts the user to select a task to delete by its number.
    If confirmed, removes the selected task from the file and updates
    the task list.

    Parameters:
        None

    Returns:
        None
    """
    try:
        with open("tasks.txt", "r", encoding="utf-8") as data_source:
            tasks = data_source.readlines()

        if not tasks:
            print("No tasks to delete.")
            return

        valid_tasks = []
        print("\nTask List:")
        for i, task in enumerate(tasks, 1):
            task_parts = task.strip().split(", ")
            if len(task_parts) < 6:
                print(f"Skipping malformed line {i}: {task.strip()}")
                continue

            assigned_to, title, desc, date_assigned, due, done = task_parts
            valid_tasks.append(task)

            print(f"\nTask {i}:")
            print(f"Assigned to: {assigned_to}")
            print(f"Title: {title}")
            print(f"Description: {desc}")
            print(f"Assigned Date: {date_assigned}")
            print(f"Due Date: {due}")
            print(f"Completed: {done}")

        if not valid_tasks:
            print("No valid tasks available for deletion.")
            return

        selection = input(
            "\nEnter task number to delete or '-1' to cancel: "
        ).strip()

        if selection == "-1":
            print("Deletion cancelled.")
            return

        if not selection.isdigit() or not (
            1 <= int(selection) <= len(valid_tasks)
        ):
            print("Invalid selection.")
            return

        task_index = int(selection) - 1
        deleted_task = valid_tasks.pop(task_index)

        updated_tasks = [
            task for task in tasks
            if task.strip() != deleted_task.strip()
        ]

        with open("tasks.txt", "w", encoding="utf-8") as doc:
            doc.writelines(updated_tasks)

        print(f"\nDeleted Task: {deleted_task.strip()}")
        print("Task deleted successfully.")

    except FileNotFoundError:
        print("Error: 'tasks.txt' file not found.")


def generate_reports():
    """
    Generates summary reports for tasks and users.

    Reads task and user data from 'tasks.txt' and 'user.txt', calculates key
    statistics (e.g. completed, incomplete, overdue tasks), and writes two
    reports: 'task_overview.txt' and 'user_overview.txt'. Skips malformed
    entries and handles invalid date formats gracefully.

    Parameters:
        None

    Returns:
        None
    """
    print("\nGenerating reports...")
    try:
        # Load tasks
        with open("tasks.txt", "r", encoding="utf-8") as script:
            raw_tasks = script.readlines()
            tasks = []
            for statement in raw_tasks:
                parts = statement.strip().split(", ")
                if len(parts) < 6:
                    print(f"Skipping malformed task: {line.strip()}")
                    continue
                tasks.append(parts)

        # Load users
        with open("user.txt", "r", encoding="utf-8") as document:
            users = [
                line.strip().split(", ")[0]
                for line in document.readlines()
            ]

        total_tasks = len(tasks)
        total_users = len(users)
        completed_tasks = sum(1 for t in tasks if t[5].lower() == "yes")
        incomplete_tasks = total_tasks - completed_tasks

        overdue_tasks = 0
        for t in tasks:
            try:
                if (
                    t[5].lower() == "no"
                    and datetime.strptime(t[4], "%d %b %Y") < datetime.today()
                ):
                    overdue_tasks += 1
            except ValueError:
                print(f"Invalid date format in task: {t}")
                continue

        percent_incomplete = (
            (incomplete_tasks / total_tasks) * 100 if total_tasks else 0
        )
        percent_overdue = (
            (overdue_tasks / total_tasks) * 100 if total_tasks else 0
        )

        # Write task overview
        with open("task_overview.txt", "w", encoding="utf-8") as record:
            record.write("Task Overview Report\n")
            record.write(f"Total tasks: {total_tasks}\n")
            record.write(f"Completed tasks: {completed_tasks}\n")
            record.write(f"Incomplete tasks: {incomplete_tasks}\n")
            record.write(f"Overdue tasks: {overdue_tasks}\n")
            record.write(
                f"Percentage incomplete: {percent_incomplete:.2f}%\n"
            )
            record.write(f"Percentage overdue: {percent_overdue:.2f}%\n")

        # Write user overview
        user_set = set(t[0] for t in tasks)
        with open("user_overview.txt", "w", encoding="utf-8") as input_data:
            input_data.write(f"Total users registered: {total_users}\n")
            input_data.write(f"Total tasks: {total_tasks}\n\n")

            for user in user_set:
                user_tasks = [t for t in tasks if t[0] == user]
                num_user_tasks = len(user_tasks)
                completed = sum(
                    1 for t in user_tasks if t[5].lower() == "yes"
                )
                incomplete = num_user_tasks - completed

                overdue = 0
                for t in user_tasks:
                    try:
                        if (
                            t[5].lower() == "no"
                            and datetime.strptime(
                                t[4], "%d %b %Y"
                            ) < datetime.today()
                        ):
                            overdue += 1
                    except ValueError:
                        continue

                percent_assigned = (
                    (num_user_tasks / total_tasks) * 100
                    if total_tasks else 0
                )
                percent_completed = (
                    (completed / num_user_tasks) * 100
                    if num_user_tasks else 0
                )
                percent_incomplete_user = (
                    (incomplete / num_user_tasks) * 100
                    if num_user_tasks else 0
                )
                percent_overdue_user = (
                    (overdue / num_user_tasks) * 100
                    if num_user_tasks else 0
                )

                file.write(f"User: {user}\n")
                file.write(f"Tasks assigned: {num_user_tasks}\n")
                file.write(
                    f"  % of total tasks: {percent_assigned:.2f}%\n"
                )
                file.write(f"  Completed: {completed}\n")
                file.write(
                    f"  % completed: {percent_completed:.2f}%\n"
                )
                file.write(f"  Incomplete: {incomplete}\n")
                file.write(
                    f"  % incomplete: {percent_incomplete_user:.2f}%\n"
                )
                file.write(f"  Overdue: {overdue}\n")
                file.write(
                    f"  % overdue: {percent_overdue_user:.2f}%\n\n"
                )

        print("Reports generated successfully.")

    except FileNotFoundError:
        print("Error: 'tasks.txt' file not found.")


def display_statistics():
    """
    Displays the contents of the generated task and user reports.

    Reads and prints data from 'task_overview.txt' and 'user_overview.txt'.
    If reports are missing, prompts the user to generate them first.

    Parameters:
        None

    Returns:
        None
    """
    print("\nDisplaying statistics...")
    try:
        with open("task_overview.txt", "r", encoding="utf-8") as task_file:
            task_stats = task_file.read()

        with open("user_overview.txt", "r", encoding="utf-8") as user_file:
            user_stats = user_file.read()

        if task_stats:
            print("\nTask Overview:")
            print(task_stats)
        else:
            print("Unable to display task statistics.")

        if user_stats:
            print("\nUser Overview:")
            print(user_stats)
        else:
            print("Unable to display user statistics.")

    except FileNotFoundError:
        print("Reports not found. Please generate them first using 'gr'.")


def read_report_file(filename):
    """
    Reads and returns the contents of a report file.

    Attempts to open the specified file and return its contents. If the file
    is not found, triggers report generation and retries. Returns None if
    the file still cannot be found.

    Parameters:
        filename (str): The name of the report file to read.

    Returns:
        The contents of the file, or None if unavailable.
    """
    try:
        with open(filename, "r", encoding="utf-8") as dataset:
            return dataset.read()
    except FileNotFoundError:
        print(f"Warning: '{filename}' not found. Generating reports...")
        generate_reports()
        try:
            with open(filename, "r", encoding="utf-8") as data_file:
                return data_file.read()
        except FileNotFoundError:
            print(f"Error: Failed to generate '{filename}'.")
            return None


# ***Main menu loop***
while True:
    if is_admin:
        menu = input(
            '''\nSelect one of the following options:
r  - register a user
a  - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del-delete tasks
ds - display statistics
gr -generate reports
e  - exit
: '''
        ).lower()
    else:
        menu = input(
            '''\nPlease select one of the following options:
a   - add task
va  - view all tasks
vm  - view my tasks
e   - exit
: '''
        ).lower()

    if menu == 'r' and is_admin:
        print("Registration in progress...")
        reg_user()

    elif menu == 'a':
        print("Adding a new task...")
        add_task()

    elif menu == 'va':
        print("Viewing all tasks...")
        view_all()

    elif menu == 'vm':
        print("Viewing your tasks...")
        view_mine(username)

    elif menu == 'vc' and is_admin:
        print("Viewing completed tasks...")
        view_completed()

    elif menu == 'del' and is_admin:
        print("Deleting a task...")
        delete_task()

    elif menu == 'ds' and is_admin:
        print("***STATISTICS***")
        display_statistics()

    elif menu == 'gr' and is_admin:
        generate_reports()

    elif menu == 'e':
        print("Thanks for using task manager! See you next time.")
        break

    else:
        print("Invalid option. Please try again.")

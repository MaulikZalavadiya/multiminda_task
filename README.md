# Task Management System

### Run the following commands to get started:

```
git clone https://github.com/MaulikZalavadiya/multiminda_task.git Task_Management_System
python3 -m venv venv
```
#### Activate the virtual environment

Mac OS / Windows
```source env/bin/activate```

Linux
```.\env\Scripts\activate```

```
cd Task_Management_System
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

# Overview

This project is a small task management.
It was built using Django and DRF and contains the following:

* Allows new accounts registration, login and logout.
* token-based authentication system.
* Each user can create edit delete any of his task.
* Each user can filter through his tasks (eg. Filter to show only uncompleted task).
* Calculate the ratio between complete and incomplete tasks and export it to a file in (CSV, Excel) format.

<a name="table-of-contents"></a>
## [Table of Contents](#table-of-contents)

In order to achieve all of these results, it is necessary to send the **_Authorization: Token_** with each link.

#### Note: Folder screenshots contains images for all operations.

* [Authentication](#auth)
  * Signup ```http://127.0.0.1:8000/user/auth/registration/```
  * Login ```http://127.0.0.1:8000/user/auth/login/```
  * Logout ```http://127.0.0.1:8000/user/auth/logout/```
  * Password-Reset-Send-Email ```http://127.0.0.1:8000/user/user/password-reset-email/```
  * Password-Reset ```http://127.0.0.1:8000/user/user/reset-password/(?P<password_reset_id>.*)```
  
* Task [CRUD Operations](#crud)
  * All Tasks ```http://127.0.0.1:8000/task/tasks/```
  * Create Task ```http://127.0.0.1:8000/task/tasks/```
  * Retrieve specific task ```http://127.0.0.1:8000/task/tasks/id/```
  * Update Task ```http://127.0.0.1:8000/task/tasks/id/```
  * Delete Task ```http://127.0.0.1:8000/task/tasks/id/```

* Comment [CRUD Operations](#crud)
  * All Comment ```http://127.0.0.1:8000/task/comments/```
  * Create Comment ```http://127.0.0.1:8000/task/comments/```
  * Retrieve specific Comment ```http://127.0.0.1:8000/task/comments/id/```
  * Update Comment ```http://127.0.0.1:8000/task/comments/id/```
  * Delete Comment ```http://127.0.0.1:8000/task/comments/id/```



* [Filter Tasks](#filter)
  * All Completed Tasks ```http://127.0.0.1:8000/task/tasks/?status=completed```
  * All Incompleted Tasks ```http://127.0.0.1:8000/task/tasks/?status=in_completed```
  

* [Report ](#export)
  * Task Completion Rate Over Time ```http://127.0.0.1:8000/task/task-completion-rate-over-time/```
  * Task Progress Report ```http://127.0.0.1:8000/task/task-progress-report/```
  * Task User Activity ```http://127.0.0.1:8000/task/user-activity-report/```
  
[Raseedi]: http://www.raseedi.co/


<a name="auth"></a>
<a name="all-tasks"></a>
<a name="crud"></a>
<a name="filter"></a>
<a name="export"></a>

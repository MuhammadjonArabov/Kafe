# Django Kafe Project Setup

Follow these steps to clone the project, set up a virtual environment, and install the required dependencies.


First, clone the repository to your local machine by running the following command:

```bash
git clone https://github.com/MuhammadjonArabov/Kafe.git
```
Let's get into the project.
```bash
cd Kafe/
```
We'll open it in Visual Studio Code. If you prefer, open it in PyCharma.
```bash
code .
```
Open the terminal and configure the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
We install libraries
```bash
pip install -r requarments.txt
```
We create a .env package and copy all the code from .env.example and fill in our PostgreSQL data.
We run the migration
```bash
python manage.py makemigrations
python manage.py migrate
```
Run
```bash
python manage.py runserver
```
Test implementation
```bash
pytest
```

After the project is launched, check the work by visiting the following URLs:
```bash
http://127.0.0.1:8000/
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```
Back in the terminal, we create a super user
```bash
python manage.py createsuperuser
```
We enter our created user information.
```bash
http://127.0.0.1:8000/admin/
```

The structure of models in database design
![Alt text](https://github.com/MuhammadjonArabov/Kafe/blob/main/DrawDB-Stricture.png)

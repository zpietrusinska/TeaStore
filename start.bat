cd \Users\Zuza\Desktop\TeaStore
call venv\Scripts\activate

cd \Users\Zuza\Desktop\TeaStore\teastore_project
python manage.py migrate
python manage.py runserver

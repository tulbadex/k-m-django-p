# Starting the Application

1. This application can eithe be cloned or download
2. Ones its available on a system, create vitual environment by runnig the command in the terminal from the directory folder
```
python -m venv venv 
```
3. activate virtual environment
```
venv\Scripts\activate 
```
4. Install all dependency with
```
pip install -r requirements/requirements.txt
```
5. Run with https
```
python manage.py runsslserver  --certificate cert.pem --key key.pem
```
6. Run without https
```
python manage.py runserver
```
flask --app main db init
flask --app main db migrate -m "init"
flask --app main db upgrade
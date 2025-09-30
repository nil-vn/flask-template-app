# Flask Template

Template for Flask applications

## Install dependencies

```bash
python3 -m venv venv  # on Windows, use "python -m venv venv" instead
. venv/bin/activate   # on Windows, use "venv\Scripts\activate" instead
pip install -r requirements\dev.txt # change to production.txt for production
```

## Application structure

```
--app/
    |--admin/
    |--homepage/
--config/
--instance/
--lang/
--log/
--requirements/
--static/
--templates/
--tests/
...
```

This structure is just a template; you can modify it and add controllers or models as needed. 

## Run application

```bash
python main.py
```

The applications will always running on http://localhost:5000.

## Example routes

- Homepage (`/`): Homepage
- Admin (`/admin`): Admin dashboard

## Migration

> flask --app main db init
> flask --app main db migrate -m "comment"
> flask --app main db upgrade


## TBD

- [] Migration with sample models
- [] Sample layouts with CLI
- [] Testcases
- [] Structure logging implement

## Contributions

Any contribution is welcome, just fork and submit your PR.

## License

This project is licensed under the MIT License (see the `LICENSE` file for details).

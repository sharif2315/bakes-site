This command runs vite which includes tailwind, AlpineJS and HTMX
```
npm run dev
```

Create Tables by running migrate
```
python3 manage.py migrate
```

create superuser
```
python3 manage.py createsuperuser
```

run the server
```
python3 manage.py runserver
```

To DUMP data 
```
python3 manage.py dumpdata products.DietaryOption > utils/fixtures/dietary_options.json
```

```
python3 manage.py dumpdata home.SvgIcon > utils/fixtures/svg_icons.json 
```

To LOAD data
```
python3 manage.py loaddata utils/fixtures/dietary_options.json
```

```
python3 manage.py loaddata utils/fixtures/svg_icons.json 
```
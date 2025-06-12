This command runs the Tailwind CSS CLI to process the input CSS file and outputs the result to the specified file while watching for changes:

```
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css --watch
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
if "%1" == "" (
	set PORT=8003
) else (
	set PORT=%1
)

::set _REGISTER_SERVICE=1
::python -c "import servicecli; servicecli.register_service(%PORT%)"

python manage.py runserver 0.0.0.0 %PORT%

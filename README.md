# Beer O mat #

## setup ##
* Set up a virtual env
* Activate the virtual env
* While that virtual env is active: `pip install -r requirements.txt`
* Create `setting_local.py` based on `settings_local.py.template`
* For local testing remove the DATABASE from `settings_local.py` to use Sqlite
* For local testing add `DEBUG = True`
* `./manage.py runserver` for dev server


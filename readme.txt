Set up virtual env
virtualenv .venv
// Note error occurs here do:
// pip install virtualenv; virtualenv .venv 
// if still fails try next
// "python -m venv /path/to/new/virtual/environment" instead

.venv/Scripts/Activate
// If error when activating run "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted"
pip install -r requirements.txt

//To run the app
flask run

# ***Attention***
# To run:
# Note I did set it to run creation of sqlite prior to starting server but incase anything goes wrong... Otherwise skip step 4
# 1) Activate venv: .venv/Scripts/Activate (For more info refer to readme.)
# 2) pip install -r requirements.txt
# 3) set Flask_APP=run.py
# If you cant run flask shell try this command instead:
#       $env:FLASK_APP = ".\run.py"
# 4) Set up temp db:
#       flask shell
#       from app import sa
#       sa.create_all()
#       exit()
# 5) "flask run" or "flask --debug run" for debug mode
# Ty for attention

from app import app, sa
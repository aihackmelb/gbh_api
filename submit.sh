virtualenv venv
source venv/local/bin/activate

# feed in file and version where version is the commit hash
python submit.py test_data.csv w22nasy 

deactivate
rm -r venv
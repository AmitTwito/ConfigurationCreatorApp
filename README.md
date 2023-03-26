# ConfigurationCreatorApp


How to run:

Open CMD in the main folders
```
pip install -r "requirements.txt"
cd app 
```

Then create ```.env``` to have:

```
PORT=5000
CONFIG_FILE_PATH=config.yaml
NUMBER_OF_SECTIONS_TO_RANDOMIZE=3
MAX_TESTS_NUMBER=10
```
Then:
```python main.py```

Then browse to ```http://localhost:PORT```

And if you want to open it as a desktop app:
```python start_app```

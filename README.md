# ConfigurationCreatorApp

- The application works on python 3.6.8.
- Used flask and pywebview to display the web application inside a normal window and not a browser.
- Make sure to reinstall ```requirements.txt``` when repulling this repo
- The app cannot select a report background image and get its path as it is not possible (web application), so it will
  get the name of the image and put it in the textbox.
- If you choose 0 as the number of sections to randomize, it will be reset to default (```defaults.py``` file). if you choose 5 - it will dispaly only one page with 5 of the sections.

## The App

A simple web-based application written in python using flask, that gives the user options for setting a configuration
and then saves the configurations into a ```config.yaml``` file.

## How to run

Open CMD in the main folder, then:

```
pip install -r requirements.txt
```

You can install the requirements within venv as well:

```
python -m venv venv
venv\Scripts\activate
pip install -r "requirements.txt"
```

Then:

```
python main.py
```

## How to use ConfigurationCreatorApp in your code

In your ```main.py```, which needs to be in the working directory - this repo's main folder, do the following:

```
from configuration_creator import ConfigurationCreatorApp

port = 5000
config_file_path = 
number_of_sections_to_randomize = 3 
max_tests_number = 10

configuration_creator_app = ConfigurationCreatorApp()
configuration_creator_app.run(config_file_path=config_file_path, max_tests_number=max_tests_number,
                              number_of_sections_to_randomize=number_of_sections_to_randomize, port=port, width=1200,
                              height=800, )
```

```run``` will run the application and open a window that displays the application. The function accepts 5 parameters:

- ```config_file_path``` is the full path for a valid ```config.yaml``` that the application will load the configuration
  from, and then will save the configurations into. Default is ```config.yaml```, and will be created in the same folder
  of your ```main.py```.
- ```max_tests_number``` is the max number for tests to select for the configuration file. It cannot be negative.
  Default is 10
- ```number_of_sections_to_randomize``` is the number of sections to randomize and display in the first page, and the
  rest in the last page. It cannot it cannot be negative or above 5. Default is 3
- ```width``` is the width of the application window. Default is 1200
- ```height``` is the height of the application window. Default is 800

On exit, the program will be terminated entirely.

## config.yaml

See the ```config.yaml``` file in the main directory as an example. file parameters:

- If no users or tests wanted in the config, set them as ```[]```
- ```hardware_acceleration``` is bool - true or false
- ```report_background_image``` is a string, a valid path for a report background image. if only a name of an image is
  set, it will search the main folder of this repo.
- ```mode``` is either ```Debug``` or ```Production```

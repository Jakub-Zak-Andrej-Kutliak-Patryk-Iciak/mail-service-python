### Mail Service - python

**Run**
  - app
    - Navigate to the root of your folder and create virtual environment with the following command \
    ``python3 -m venv venv/``
    - Activate your virtual environment like this \
    ``source venv/bin/activate``
    - Once done, you can deactivate the virtual environment with this command \
    ``deactivate``
    - After activating your virtual environment install all required dependencies \
    ``pip3 install -r requirements.txt``
    - If adding new dependency, run the following command to add the dependency to the requirements file \
    ``pip3 freeze > requirements.txt``
    - Create your local .env file in the same directory as config.py and configure it according to the .env.example file
    - To run the server in your terminal navigate to the root of the folder and run this command \
    ``python3 app.py``
  - docs
    - Once the application is running copy the url it printed out while starting, which defaults to port 5000, 
    however, if you already had something running on port 5000 it will grab the next available one
    - Paste the url in the top bar and add \
    ``/apidocs``
    - This opens the swagger documentation of the api
  - tests
    - To run all the tests navigate to root of the application folder and enter \
    ``pytest``
    - This command will run all the tests in the tests folder and print out their status
    - troubleshooting: if the pytest command is not available, check if your virtual environment is active
  - docker
    - To run the service as a docker container execute following command
    ```commandline
    docker run -t tag_name -p host_port:container_port --name name_of_the_container -d image_name
    ```

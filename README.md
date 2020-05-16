# COSC 603 ToDo app

This the the repository for the COSC 604 testing ToDo app.

## Setup

Git clone this repo to your machine. Copy the clone instructions in the top right and either:

```commandline
git clone git@github.com:chasebrewsky/COSC603.git
OR
https://github.com/chasebrewsky/COSC603.git
```

Your choice depends on if you want to authorize based on SSH keys or HTTP credentials.

Make sure you have at least python 3.6 installed.

Create a python virtual environment to install your dependencies into. This is done by running:

```commandline
python3 -m venv ./venv
```

This creates a "virtual" python environment that won't pollute your global python namespace when installing dependencies.

Activate your virtual environment:

```commandline
source ./venv/bin/activate
```

Install the project dependencies:

```commandline
pip install -r requirements.txt
```

## Developing

This is a Django base project, and will use the framework almost exclusively. You can learn how to develop within the framework by visiting https://www.djangoproject.com/.

Make sure to run through the tutorial to make a basic app, then come back here to develop.

We'll be using SQLite as the database since it requires minimal setup.

Each member will be responsible for their own tests. If more features need to be added to test, please contact me.

## Testing

Running the tests is done through an automated testing tool called [tox](https://tox.readthedocs.io/en/latest/). This tool will run the tests in the current environment and output the coverage results in both the console and in HTML form in the subdirectory `htmlcov`.

In order to run tox, you first have to install it by running `pip install tox`, or if you're Sonny it's `pip3 install tox` because his python environment is messed up.

After installing it, just run `tox` in the root of the project directory and it should run the tests. Contact me if you run into any issues with it.

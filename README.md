# Infinit Speech

Project Requirement

- Python 3.6 or later
- Node 10.0 or later

## Set python environment

If you're on MacOS, you can install Pipenv easily with Homebrew:

```bash
$ brew install pipenv
```

Or, if you're using Ubuntu 17.10:

```bash
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
```

Otherwise, just use pip:

```bash
$ pip install pipenv
```

```bash
cd path/to/InfiniteSpeech

# need every time
# or
# add to your shell config file, like '.zshrc' , '.bashrc' etc.
export PIPENV_VENV_IN_PROJECT=1

pipenv install
```

## Set React evironment

```bash
cd path/to/InfiniteSpeech/react_app
npm install
npm run build
```

## Set Nginx config

Edit nginx.conf file (at `/etc/nginx/nginx.conf` normally), add `include /path/to/InfiniteSpeech/nginx.conf` in block `http`.

```bash
# chech conf file syntax
nginx -t

# reload nginx
nginx -s reload
```

## Deploy python project

```bash
cd path/to/InfiniteSpeech
pipenv shell
uwsgi uwsgi.ini
```

Ready to GO!

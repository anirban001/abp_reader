#!/bin/bash
set -e
set -o pipefail

export PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd ${PROJECT_ROOT}

_setup() {
  # # http://docs.python-guide.org/en/latest/dev/virtualenvs/
  # pip install virtualenv
  return
  mkdir -p ${PROJECT_ROOT}/.cache
  cd ${PROJECT_ROOT}/.cache
  virtualenv --no-site-packages venv_01
  virtualenv venv_01
  return
}

_activate() {
  . ${PROJECT_ROOT}/.cache/venv_01/bin/activate
}

_pip_install() {
  _activate
  pip install $1
  pip freeze > ./requirements.txt
  return
  # Re-install.
  # pip install -r ./requirements.txt
}


# (_setup)
# (_pip_install beautifulsoup4)

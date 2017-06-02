#!/bin/bash
set -e
set -o pipefail

export PROJECT_ROOT=$(git rev-parse --show-toplevel)
export CACHE_DIR="${PROJECT_ROOT}/.cache"
export PHANTOMJS_DIR="${CACHE_DIR}/phantom_js"

_setup() {
  cd ${PROJECT_ROOT}
  # # http://docs.python-guide.org/en/latest/dev/virtualenvs/
  # pip install virtualenv
  # brew install wget
  return
  mkdir -p ${CACHE_DIR}
  cd ${CACHE_DIR}
  virtualenv --no-site-packages venv_01
  virtualenv venv_01
  return
}

_activate() {
  cd ${PROJECT_ROOT}
  . ${CACHE_DIR}/venv_01/bin/activate
}

_pip_install() {
  _activate
  pip install $1
  pip freeze > ./requirements.txt
  return
  # Re-install.
  # pip install -r ./requirements.txt
}

_install_phantomjs() {
  cd ${PROJECT_ROOT}
  mkdir -p /tmp/downloads
  wget  -O /tmp/downloads/phantomjs.zip \
    "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"
  cd /tmp/downloads
  unzip ./phantomjs.zip
  mv ./phantomjs-2.1.1-macosx ${PHANTOMJS_DIR}
  # cd ${PHANTOMJS_DIR}
  # upx -d bin/phantomjs
}

_run_it() {
  _activate
  python2.7 -c 'import code_dir.main; code_dir.main.do_main()'
}

# (_setup)
# (_pip_install beautifulsoup4)
# (_pip_install selenium)
# (_install_phantomjs)
(_run_it)

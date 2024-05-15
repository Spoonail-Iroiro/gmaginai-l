# first command
default:
    just -l --unsorted

# test all
test:
    python -m pytest ./test

# launch Qt designer
designer:
    pyside6-designer &

# convert from .ui to _ui.py
uic:
    python ./tools/exec_uic.py

# run app
run:
    python main.py

build:
    python ./tools/build.py

run-dist:
    ./dist/SaveBackup/save_backup

update-requirements:
    pip-compile requirements.in --no-emit-index-url --no-upgrade
    pip-compile requirements_dev.in --no-emit-index-url --no-upgrade -o requirements_dev.txt
    just sync-python-environment

sync-python-environment:
    pip-sync requirements.txt requirements_dev.txt



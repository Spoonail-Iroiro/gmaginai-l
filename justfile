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
    just compile-translation
    python main.py

build:
    just compile-translation
    python ./tools/build.py

run-dist:
    ./dist/gmaginai-l/gmaginai-l

update-requirements:
    pip-compile requirements.in --no-emit-index-url --no-upgrade
    pip-compile requirements_dev.in --no-emit-index-url --no-upgrade -o requirements_dev.txt
    just sync-python-environment

sync-python-environment:
    pip-sync requirements.txt requirements_dev.txt

update-translation-files:
    python ./tools/list_translation_targets.py
    pyside6-lupdate @.trlist -ts ./src/translation/gmaginai-l_ja.ts

compile-translation:
    pyside6-lrelease ./src/translation/gmaginai-l_ja.ts -qm ./_internal/content_translation/gmaginai-l_ja.qm


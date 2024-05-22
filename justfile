# first command
default:
    just -l --unsorted

# run main
run:
    just compile-translation
    python main.py

# build app
build:
    just compile-translation
    python ./tools/build.py

# run built app
run-dist:
    ./dist/gmaginai-l/gmaginai-l

# open Qt designer
designer:
    pyside6-designer &

# convert Qt UI file (.ui) to python script (_ui.py)
uic:
    python ./tools/exec_uic.py

# test all
test:
    python -m pytest ./test

# update translation file (.ts) and open pyside6-linguist
linguist:
    just update-translation-files
    pyside6-linguist ./src/translation/gmaginai-l_ja.ts

# generate/update translation file (.ts)
update-translation-files:
    python ./tools/list_translation_targets.py
    pyside6-lupdate @.trlist -ts ./src/translation/gmaginai-l_ja.ts

# compile translation file (.ts) to binary (.qm)
compile-translation:
    pyside6-lrelease ./src/translation/gmaginai-l_ja.ts -qm ./_internal/content_translation/gmaginai-l_ja.qm

# update requirements*.txt from requirements*.in with pip-tools
update-requirements:
    pip-compile requirements.in --no-emit-index-url --no-upgrade
    pip-compile requirements_dev.in --no-emit-index-url --no-upgrade -o requirements_dev.txt
    just sync-python-environment

# sync python environment with requests*.in
sync-python-environment:
    pip-sync requirements.txt requirements_dev.txt

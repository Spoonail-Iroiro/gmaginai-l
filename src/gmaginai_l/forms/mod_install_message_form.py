from pathlib import Path
from typing import Optional, List, Tuple, Dict
import shutil
import logging
from enum import Enum, auto
import tempfile
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QDialogButtonBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot, QCoreApplication
from .message_form_ui import Ui_MessageForm
from .message_form import MessageFormBase
from ..core.maginai_installer import MaginaiInstaller
from ..core.mod_installer import ModInstaller
from .. import funcs


logger = logging.getLogger(__name__)


class FormStateBase:
    def __init__(self):
        pass

    def enter(self, body):
        pass

    def exit(self, body):
        pass

    def btn_ok_clicked(self, body):
        pass

    def btn_cancel_clicked(self, body):
        pass


class CancelError(Exception):
    pass


class InterruptInstallError(Exception):
    def __init__(result_message: str):
        super().__init__(result_message)


class ModInstallMessageForm(MessageFormBase):
    def __init__(self, installer: ModInstaller, parent=None):
        title = self.tr("Install Mod")
        super().__init__(title, parent)

        self.installer = installer

        self.mod_dir_to_install: Path | None = None
        self.temp_dir: Path | None = None
        self.extracted_dir: Path | None = None

        self.state: FormStateBase | None = None
        self.set_state(FormStateSelectMod())

        (
            self.btn_ok,
            self.btn_cancel,
        ) = tuple(
            self.set_buttons(
                [
                    (self.tr("OK"), self.Buttons.AcceptRole),
                    (self.tr("Cancel"), self.Buttons.RejectRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.rejectDialog)

    def btn_ok_clicked(self):
        self.state.btn_ok_clicked(self)

    def btn_cancel_clicked(self):
        self.state.btn_cancel_clicked(self)

    def dispose(self):
        if self.temp_dir is not None and self.temp_dir.exists():
            try:
                shutil.rmtree(self.work_dir)
            except Exception:
                logger.exception("")

    def set_state(self, state: FormStateBase):
        if self.state is not None:
            self.state.exit(self)
        self.state = state
        self.state.enter(self)

    def move_to_finish(self):
        self.state = FormState.FINISHED
        self.btn_ok.setVisible(True)
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setVisible(True)
        self.btn_cancel.setEnabled(False)

    def acceptDialog(self):
        self.dispose()
        super().acceptDialog()

    def rejectDialog(self):
        self.dispose()
        super().rejectDialog()


class FormStateSelectMod(FormStateBase):
    def enter(self, body: ModInstallMessageForm):
        body.set_message(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                f"Select init.js in mod's main folder or distribution zip.\n"
                "(If the selected mod is already installed, it will be updated)",
            )
        )

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        try:
            selected_path = self._select_file(body)
            if selected_path is None:
                return
            self._determin_mod_dir_to_install(body, selected_path)
        except Exception as ex:
            on_error(ex, body)

    def _select_file(self, body: ModInstallMessageForm) -> Path | None:
        fdialog = QFileDialog(body)
        fdialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fdialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        fdialog.setNameFilter("zip file (*.zip);;init.js (init.js)")
        rtn = fdialog.exec()

        filepaths = fdialog.selectedFiles()
        if rtn == QDialog.DialogCode.Accepted and len(filepaths) > 0:
            return Path(filepaths[0])

        pass

    def _determin_mod_dir_to_install(self, body: ModInstallMessageForm, path: Path):
        # TODO: more suitable file classification
        if path.suffix == ".zip":
            try:
                temp_dir = Path(tempfile.mkdtemp())
                body.temp_dir = temp_dir
                body.installer.set_work_dir(temp_dir)
                extracted = body.installer.unzip_to_work_temp(path)
                body.extracted_dir = extracted
                mod_dir = body.installer.search_mod_main_folder(extracted)
                if mod_dir is None:
                    raise ValueError(f"No mod's main folder found")

            except Exception as ex:
                error_message = QCoreApplication.translate(
                    "ModInstallMessageForm",
                    (
                        "Unabled to extract a mod from the distribution zip. "
                        "Please unzip it manually and specify init.js.\n"
                        "{0}"
                    ),
                ).format(funcs.formatError(ex))
                logger.exception(error_message)
                body.set_state(FormStateFinish(error_message))
                return
        else:
            if path.name != "init.js":
                isOk = funcs.showConfirm(
                    body,
                    QCoreApplication.translate(
                        "ModInstallMessageForm",
                        "Confirm",
                    ),
                    QCoreApplication.translate(
                        "ModInstallMessageForm",
                        "The selected file is not init.js, so you might selected wrong mod's main folder. "
                        "Proceed anyway?",
                    ),
                )
                if not isOk:
                    body.rejectDialog()
                    return

            mod_dir = path.parent

        body.mod_dir_to_install = mod_dir
        body.set_state(FormStateConfirmMod())

    def btn_cancel_clicked(self, body):
        body.rejectDialog()

    # SELECT_MOD = auto()
    # FINISHED = auto()


class FormStateConfirmMod(FormStateBase):
    def __init__(self):
        self.is_update = False

    def enter(self, body: ModInstallMessageForm):
        mod_dir = body.mod_dir_to_install
        mod_name = mod_dir.name
        if body.installer.has_mod_own_folder(mod_name):
            self.is_update = True
        text_install_update = (
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Mod '{0}' will be installed.",
            ).format(mod_name)
            if not self.is_update
            else QCoreApplication.translate(
                "ModInstallMessageForm",
                "Mod '{0}' will be updated.",
            ).format(mod_name)
        )
        body.set_message(text_install_update)

        body.btn_ok.setVisible(True)
        body.btn_ok.setEnabled(True)
        body.btn_cancel.setVisible(True)
        body.btn_cancel.setEnabled(True)

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        try:
            mod_dir = body.mod_dir_to_install
            mod_name = mod_dir.name
            if self.is_update:
                body.installer.backup_existing_install_by_move(mod_name)
            body.installer.install_mod(mod_dir)
            complete_state = FormStateCompleted(self.is_update)
            if body.extracted_dir is not None:
                next_state = FormStateConfirmZip(complete_state, body.extracted_dir)
            else:
                next_state = complete_state

            body.set_state(next_state)
        except Exception as ex:
            on_error(ex, body)

    def btn_cancel_clicked(self, body: ModInstallMessageForm):
        body.rejectDialog()


class FormStateConfirmZip(FormStateBase):
    def __init__(self, next_state: FormStateBase, extracted_dir: Path):
        self.next_state = next_state
        self.extracted_dir = extracted_dir

        self.btn_open_extracted_dir: PushButton | None = None
        self._original_ok_text: str | None = None

    def enter(self, body: ModInstallMessageForm):
        body.btn_ok.setVisible(True)
        body.btn_ok.setEnabled(True)
        self._original_ok_text = body.btn_ok.text()
        body.btn_ok.setText(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Next",
            )
        )
        body.btn_cancel.setVisible(False)
        body.btn_cancel.setEnabled(False)
        body.set_message(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Usually distribution zip file includes helpful readme, other docs or utilities."
                "It's recommended to see what's inside the extracted folder.",
            )
        )
        (self.btn_open_extracted_dir,) = body.set_buttons(
            [
                (
                    QCoreApplication.translate(
                        "ModInstallMessageForm", "Open extracted folder"
                    ),
                    body.Buttons.ActionRole,
                )
            ]
        )
        self.btn_open_extracted_dir.clicked.connect(self.btn_open_extracted_dir_clicked)

    def btn_open_extracted_dir_clicked(self):
        try:
            funcs.open_directory(self.extracted_dir)
        except Exception as ex:
            logger.exception("")

    def btn_ok_clicked(self, body):
        try:
            body.set_state(self.next_state)
        except Exception as ex:
            on_error(ex, body)

    def exit(self, body: ModInstallMessageForm):
        body.btn_ok.setText(str(self._original_ok_text))
        body.btn_cancel.setVisible(True)
        if self.btn_open_extracted_dir is not None:
            body.ui.bbx_main.removeButton(self.btn_open_extracted_dir)


class FormStateFinish(FormStateBase):
    def __init__(self, message):
        self.message = message

    def enter(self, body: ModInstallMessageForm):
        body.set_message(self.message)

        body.btn_ok.setVisible(True)
        body.btn_ok.setEnabled(True)
        body.btn_cancel.setVisible(True)
        body.btn_cancel.setEnabled(False)

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        body.rejectDialog()


class FormStateCompleted(FormStateBase):
    def __init__(self, is_update):
        self.is_update = is_update

    def enter(self, body: ModInstallMessageForm):
        mod_name = body.mod_dir_to_install.name
        # TODO: update case
        text_install_update = (
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Installed '{0}' successfully.",
            )
            if not self.is_update
            else QCoreApplication.translate(
                "ModInstallMessageForm",
                "Updated '{0}' successfully.",
            )
        )
        text_install_update = text_install_update.format(mod_name)
        body.set_message(text_install_update)

        body.btn_ok.setVisible(True)
        body.btn_ok.setEnabled(True)
        body.btn_cancel.setVisible(True)
        body.btn_cancel.setEnabled(False)

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        body.acceptDialog()


def on_error(exc: Exception, body: ModInstallMessageForm):
    error_message = funcs.formatError(exc)
    logger.error("", exc_info=exc)
    result_message = QCoreApplication.translate(
        "ModInstallMessageForm",
        "An error occured during install.\n{0}",
    ).format(error_message)

    body.set_state(FormStateFinish(result_message))

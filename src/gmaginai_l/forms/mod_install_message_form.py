from pathlib import Path
from typing import Optional, List, Tuple, Dict
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
        title = f"Install Mod"
        super().__init__(self.tr(title), parent)

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
                    # (
                    #     self.tr("Yes, I want to see what's inside the zip"),
                    #     self.Buttons.AcceptRole,
                    # ),
                    # (self.tr("No, just discard it"), self.Buttons.RejectRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.rejectDialog)
        # self.btn_yes_show_extracted.setVisible(True)
        # self.btn_no_show_extracted.setVisible(False)

    def btn_ok_clicked(self):
        self.state.btn_ok_clicked(self)
        # if self.state == FormState.SELECT_MOD:
        #     selected_path = self._select_file()
        #     if selected_path is None:
        #         return
        #     self._install_new(selected_path)
        #     self.state = FormState.FINISHED
        #     self.btn_cancel.setEnabled(False)
        # elif self.state == FormState.FINISHED:
        #     self.acceptDialog()

    def btn_cancel_clicked(self):
        self.state.btn_cancel_clicked(self)

    def dispose(self):
        if self.temp_dir is not None and self.temp_dir.exists():
            logger.info(f"rmtree: {self.temp_dir}")
            # shutil.rmtree(self.work_dir)

    def _install_new(self, path: Path):
        mod_name = mod_dir.name
        isOk = funcs.showConfirm(
            self, self.tr("Confirm"), f"Mod '{mod_name}' will be installed. OK?"
        )
        if not isOk:
            self.rejectDialog()
            return

        self.installer.install_mod(mod_dir)

        self.move_to_successfully_installed(mod_name)

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

    def move_to_successfully_installed(self, mod_name):
        self.ui.txt_main.setText(f"Installed '{mod_name}' successfully.")
        self.move_to_finish()

    def acceptDialog(self):
        self.dispose()
        super().acceptDialog()

    def rejectDialog(self):
        self.dispose()
        super().rejectDialog()


class FormStateSelectMod(FormStateBase):
    def enter(self, body: ModInstallMessageForm):
        body.ui.txt_main.setText(
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
            on_error(ex)

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
                        "Unabled to extract mod from the distribution zip. "
                        "Please unzip it manually and specify init.js.\n"
                        f"{funcs.formatError(ex)}"
                    ),
                )
                logger.exception(error_message)
                body.set_state(FormStateFinish(error_message))
                return
                # body.ui.txt_main.setText(error_message)
                # logger.exception(error_message)
                # body.move_to_finish()
        else:
            if path.name != "init.js":
                isOk = funcs.showConfirm(
                    body,
                    body.tr("Confirm"),
                    "The selected file is not init.js, so you might selected wrong mod's main folder. Proceed anyway?",
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
    def enter(self, body: ModInstallMessageForm):
        body.ui.txt_main.setText(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                f"Mod '{body.mod_dir_to_install.name}' will be installed. OK?",
            )
        )

        body.btn_ok.setVisible(True)
        body.btn_ok.setEnabled(True)
        body.btn_cancel.setVisible(True)
        body.btn_cancel.setEnabled(True)

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        try:
            mod_dir = body.mod_dir_to_install
            mod_name = mod_dir.name
            body.installer.install_mod(mod_dir)
            body.set_state(FormStateCompleted(False))
        except Exception as ex:
            on_error(ex, body)

    def btn_cancel_clicked(self, body: ModInstallMessageForm):
        body.rejectDialog()


class FormStateFinish(FormStateBase):
    def __init__(self, message):
        self.message = message

    def enter(self, body: ModInstallMessageForm):
        body.ui.txt_main.setText(self.message)

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
        body.ui.txt_main.setText(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                f"Installed '{mod_name}' successfully.",
            )
        )

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
        f"An error occured during install.\n{error_message}",
    )

    body.set_state(FormStateFinish(result_message))

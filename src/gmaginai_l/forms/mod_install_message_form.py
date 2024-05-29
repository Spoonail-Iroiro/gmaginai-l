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
from .. import funcs, dirs


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

    def btn_next_clicked(self, body):
        pass


class CancelError(Exception):
    pass


class ModInstallMessageForm(MessageFormBase):
    def __init__(self, installer: ModInstaller, parent=None):
        title = self.tr("Install/Update Mod")
        super().__init__(title, parent)

        self.installer = installer

        self.mod_dir_to_install: Path | None = None
        self.temp_dir: Path | None = None
        self.extracted_dir: Path | None = None

        self.state: FormStateBase = FormStateBase()

        (
            self.btn_ok,
            self.btn_cancel,
            self.btn_action1,
            self.btn_action2,
            self.btn_next,
        ) = tuple(
            self.set_buttons(
                [
                    (self.tr("OK"), self.Buttons.AcceptRole),
                    (self.tr("Cancel"), self.Buttons.RejectRole),
                    ("Action1", self.Buttons.ActionRole),
                    ("Action2", self.Buttons.ActionRole),
                    (self.tr("Next"), self.Buttons.ActionRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.rejectDialog)
        self.btn_next.clicked.connect(self.btn_next_clicked)

        self.set_state(FormStateSelectMod())

    def btn_ok_clicked(self):
        self.state.btn_ok_clicked(self)

    def btn_cancel_clicked(self):
        self.state.btn_cancel_clicked(self)

    def btn_next_clicked(self):
        self.state.btn_next_clicked(self)

    def dispose(self):
        if self.temp_dir is not None and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
            except Exception:
                logger.exception("")

    def set_state(self, state: FormStateBase):
        if self.state is not None:
            self.state.exit(self)
        self.state = state
        self.state.enter(self)

    def set_ok_cancel_buttons(self):
        self.btn_ok.setVisible(True)
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setVisible(True)
        self.btn_cancel.setEnabled(True)
        self.btn_action1.setVisible(False)
        self.btn_action2.setVisible(False)
        self.btn_next.setVisible(False)

    def set_next_actions_buttons(self):
        # hide all actionbuttons because setVisible changes the order of action buttons
        self.set_ok_cancel_buttons()
        self.btn_ok.setVisible(False)
        self.btn_cancel.setVisible(False)
        self.btn_action1.setVisible(True)
        self.btn_action1.setEnabled(True)
        self.btn_action2.setVisible(True)
        self.btn_action2.setEnabled(True)
        self.btn_next.setVisible(True)
        self.btn_next.setEnabled(True)

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
                f"Select init.js in mod's main folder or distribution zip file.\n"
                "(If the selected mod is already installed, it will be updated)",
            )
        )
        body.set_ok_cancel_buttons()

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
        fdialog.setNameFilter("init.js or zip file (init.js *.zip)")
        rtn = fdialog.exec()

        filepaths = fdialog.selectedFiles()
        if rtn == QDialog.DialogCode.Accepted and len(filepaths) > 0:
            return Path(filepaths[0])

        return None

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
        mod_name = mod_dir.name  # type: ignore [union-attr]
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

        body.set_ok_cancel_buttons()

    def btn_ok_clicked(self, body: ModInstallMessageForm):
        try:
            mod_dir = body.mod_dir_to_install
            mod_name = mod_dir.name  # type: ignore [union-attr]
            if self.is_update:
                body.installer.backup_existing_install_by_move(mod_name)
            body.installer.install_mod(mod_dir)  # type: ignore [arg-type]
            complete_state = FormStateCompleted(self.is_update)
            if body.extracted_dir is not None:
                next_state: FormStateBase = FormStateConfirmZip(
                    complete_state, body.extracted_dir
                )
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

        self.btn_open_extracted_dir: QPushButton | None = None
        self._original_ok_text: str | None = None
        # Extracted dir copied from body.extracted_dir
        self.copied_extracted_dir: Path | None = None

    def enter(self, body: ModInstallMessageForm):
        body.set_message(
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Note: usually distribution zip file includes helpful readme, other docs or utilities. "
                "It's recommended to see what's inside the extracted folder.",
            )
        )
        body.set_next_actions_buttons()
        body.btn_action2.setVisible(False)
        self._init_action_button(body)

    def _init_action_button(self, body: ModInstallMessageForm):
        body.btn_action1.setText(
            QCoreApplication.translate("ModInstallMessageForm", "Open extracted folder")
        )
        body.btn_action1.clicked.connect(self.btn_open_extracted_dir_clicked)

    def _dispose_action_button(self, body: ModInstallMessageForm):
        body.btn_action1.setText("")
        body.btn_action1.clicked.disconnect()

    def btn_open_extracted_dir_clicked(self):
        try:
            if self.copied_extracted_dir is None:
                dst = dirs.application_dir / "temp"
                dst.mkdir(exist_ok=True)
                temp_dir = Path(tempfile.mkdtemp(dir=dst))
                shutil.copytree(self.extracted_dir, temp_dir, dirs_exist_ok=True)
                self.copied_extracted_dir = temp_dir

            funcs.open_directory(self.copied_extracted_dir)
        except Exception as ex:
            logger.exception("")

    def btn_next_clicked(self, body):
        try:
            body.set_state(self.next_state)
        except Exception as ex:
            on_error(ex, body)

    def exit(self, body: ModInstallMessageForm):
        self._dispose_action_button(body)


class FormStateFinish(FormStateBase):
    def __init__(self, message):
        self.message = message

    def enter(self, body: ModInstallMessageForm):
        body.set_message(self.message)

        body.set_next_actions_buttons()
        body.btn_action1.setVisible(False)
        body.btn_action2.setVisible(False)

        body.btn_next.setText(
            QCoreApplication.translate("ModInstallMessageForm", "Finish")
        )

    def btn_next_clicked(self, body: ModInstallMessageForm):
        body.rejectDialog()


class FormStateCompleted(FormStateBase):
    def __init__(self, is_update):
        self.is_update = is_update

    def enter(self, body: ModInstallMessageForm):
        mod_name = body.mod_dir_to_install.name  # type: ignore [union-attr]
        text_install_update = (
            QCoreApplication.translate(
                "ModInstallMessageForm",
                "Installed '{0}' successfully.",
            )
            if not self.is_update
            else QCoreApplication.translate(
                "ModInstallMessageForm",
                "Updated '{0}' successfully.\n"
                "Note: If the mod contains user-editable files, such as setting file, "
                "you should manually migrate it from old to current.",
            )
        )
        text_install_update = text_install_update.format(mod_name)
        body.set_message(text_install_update)

        body.set_next_actions_buttons()
        if self.is_update:
            self._init_action_button(body)
        else:
            body.btn_action1.setVisible(False)
            body.btn_action2.setVisible(False)

        body.btn_next.setText(
            QCoreApplication.translate("ModInstallMessageForm", "Finish")
        )

    def _init_action_button(self, body: ModInstallMessageForm):
        body.btn_action1.setText(
            QCoreApplication.translate("ModInstallMessageForm", "Open old folder")
        )

        body.btn_action1.clicked.connect(lambda: self.open_mod_dir(body, True))
        body.btn_action2.setText(
            QCoreApplication.translate("ModInstallMessageForm", "Open current folder")
        )
        body.btn_action2.clicked.connect(lambda: self.open_mod_dir(body, False))

    def _dispose_action_button(self, body):
        if self.is_update:
            body.btn_action1.clicked.disconnect()
            body.btn_action2.clicked.disconnect()

    def open_mod_dir(self, body: ModInstallMessageForm, is_old: bool):
        mod_name = body.mod_dir_to_install.name  # type: ignore [union-attr]
        if is_old:
            mod_dir = body.installer.get_mod_backup_dir(mod_name)
        else:
            mod_dir = body.installer.get_mod_own_dir(mod_name)

        funcs.open_directory(mod_dir)

    def exit(self, body: ModInstallMessageForm):
        self._dispose_action_button(body)

    def btn_next_clicked(self, body: ModInstallMessageForm):
        body.acceptDialog()


def on_error(exc: Exception, body: ModInstallMessageForm):
    error_message = funcs.formatError(exc)
    logger.error("", exc_info=exc)
    result_message = QCoreApplication.translate(
        "ModInstallMessageForm",
        "An error occured during install.\n{0}",
    ).format(error_message)

    body.set_state(FormStateFinish(result_message))

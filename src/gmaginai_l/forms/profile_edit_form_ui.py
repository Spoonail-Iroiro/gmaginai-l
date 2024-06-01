# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_edit_form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ProfileEditForm(object):
    def setupUi(self, ProfileEditForm):
        if not ProfileEditForm.objectName():
            ProfileEditForm.setObjectName(u"ProfileEditForm")
        ProfileEditForm.resize(594, 117)
        self.verticalLayout = QVBoxLayout(ProfileEditForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(ProfileEditForm)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.txt_name = QLineEdit(ProfileEditForm)
        self.txt_name.setObjectName(u"txt_name")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.txt_name)

        self.label = QLabel(ProfileEditForm)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txt_game_dir = QLineEdit(ProfileEditForm)
        self.txt_game_dir.setObjectName(u"txt_game_dir")

        self.horizontalLayout.addWidget(self.txt_game_dir)

        self.btn_open = QPushButton(ProfileEditForm)
        self.btn_open.setObjectName(u"btn_open")

        self.horizontalLayout.addWidget(self.btn_open)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_detect_steam_version = QPushButton(ProfileEditForm)
        self.btn_detect_steam_version.setObjectName(u"btn_detect_steam_version")

        self.horizontalLayout_2.addWidget(self.btn_detect_steam_version)

        self.btn_ok = QPushButton(ProfileEditForm)
        self.btn_ok.setObjectName(u"btn_ok")

        self.horizontalLayout_2.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton(ProfileEditForm)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout_2.addWidget(self.btn_cancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ProfileEditForm)

        QMetaObject.connectSlotsByName(ProfileEditForm)
    # setupUi

    def retranslateUi(self, ProfileEditForm):
        ProfileEditForm.setWindowTitle(QCoreApplication.translate("ProfileEditForm", u"Profile", None))
        self.label_4.setText(QCoreApplication.translate("ProfileEditForm", u"Name", None))
        self.label.setText(QCoreApplication.translate("ProfileEditForm", u"Game directory", None))
        self.btn_open.setText(QCoreApplication.translate("ProfileEditForm", u"Select Game.exe", None))
        self.btn_detect_steam_version.setText(QCoreApplication.translate("ProfileEditForm", u"Detect Steam version", None))
        self.btn_ok.setText(QCoreApplication.translate("ProfileEditForm", u"OK", None))
        self.btn_cancel.setText(QCoreApplication.translate("ProfileEditForm", u"Cancel", None))
    # retranslateUi


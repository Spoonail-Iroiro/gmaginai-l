# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_form.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ProfileForm(object):
    def setupUi(self, ProfileForm):
        if not ProfileForm.objectName():
            ProfileForm.setObjectName(u"ProfileForm")
        ProfileForm.resize(471, 371)
        self.horizontalLayout = QHBoxLayout(ProfileForm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(ProfileForm)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(ProfileForm)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.btnSelect = QPushButton(ProfileForm)
        self.btnSelect.setObjectName(u"btnSelect")

        self.horizontalLayout_4.addWidget(self.btnSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_add = QPushButton(ProfileForm)
        self.btn_add.setObjectName(u"btn_add")

        self.horizontalLayout_3.addWidget(self.btn_add)

        self.btn_edit = QPushButton(ProfileForm)
        self.btn_edit.setObjectName(u"btn_edit")

        self.horizontalLayout_3.addWidget(self.btn_edit)

        self.btn_delete = QPushButton(ProfileForm)
        self.btn_delete.setObjectName(u"btn_delete")

        self.horizontalLayout_3.addWidget(self.btn_delete)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(ProfileForm)

        QMetaObject.connectSlotsByName(ProfileForm)
    # setupUi

    def retranslateUi(self, ProfileForm):
        ProfileForm.setWindowTitle(QCoreApplication.translate("ProfileForm", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("ProfileForm", u"Select profile.", None))
        self.btnSelect.setText(QCoreApplication.translate("ProfileForm", u"Go", None))
        self.btn_add.setText(QCoreApplication.translate("ProfileForm", u"New", None))
        self.btn_edit.setText(QCoreApplication.translate("ProfileForm", u"Edit", None))
        self.btn_delete.setText(QCoreApplication.translate("ProfileForm", u"Delete", None))
    # retranslateUi


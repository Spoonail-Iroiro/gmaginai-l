# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
        ProfileForm.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(ProfileForm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(ProfileForm)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ProfileForm)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnSelect = QPushButton(ProfileForm)
        self.btnSelect.setObjectName(u"btnSelect")

        self.horizontalLayout_2.addWidget(self.btnSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(ProfileForm)
        self.btnSelect.clicked.connect(ProfileForm.btnSelect_clicked)

        QMetaObject.connectSlotsByName(ProfileForm)
    # setupUi

    def retranslateUi(self, ProfileForm):
        ProfileForm.setWindowTitle(QCoreApplication.translate("ProfileForm", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("ProfileForm", u"\u30d7\u30ed\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u4e0b\u3055\u3044", None))
        self.btnSelect.setText(QCoreApplication.translate("ProfileForm", u"\u9078\u629e", None))
    # retranslateUi


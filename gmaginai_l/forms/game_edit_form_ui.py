# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_edit_form.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_GameEditForm(object):
    def setupUi(self, GameEditForm):
        if not GameEditForm.objectName():
            GameEditForm.setObjectName(u"GameEditForm")
        GameEditForm.resize(594, 117)
        self.verticalLayout = QVBoxLayout(GameEditForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(GameEditForm)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.txt_name = QLineEdit(GameEditForm)
        self.txt_name.setObjectName(u"txt_name")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.txt_name)

        self.label = QLabel(GameEditForm)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txt_bak = QLineEdit(GameEditForm)
        self.txt_bak.setObjectName(u"txt_bak")

        self.horizontalLayout.addWidget(self.txt_bak)

        self.btn_bak = QPushButton(GameEditForm)
        self.btn_bak.setObjectName(u"btn_bak")

        self.horizontalLayout.addWidget(self.btn_bak)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(GameEditForm)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(GameEditForm)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(GameEditForm)

        QMetaObject.connectSlotsByName(GameEditForm)
    # setupUi

    def retranslateUi(self, GameEditForm):
        GameEditForm.setWindowTitle(QCoreApplication.translate("GameEditForm", u"\u30b2\u30fc\u30e0\u767b\u9332", None))
        self.label_4.setText(QCoreApplication.translate("GameEditForm", u"name", None))
        self.label.setText(QCoreApplication.translate("GameEditForm", u"Game.exe path", None))
        self.btn_bak.setText(QCoreApplication.translate("GameEditForm", u"Open...", None))
        self.pushButton.setText(QCoreApplication.translate("GameEditForm", u"OK", None))
        self.pushButton_2.setText(QCoreApplication.translate("GameEditForm", u"Cancel", None))
    # retranslateUi


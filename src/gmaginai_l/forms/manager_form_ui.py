# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manager_form.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

class Ui_ManagerForm(object):
    def setupUi(self, ManagerForm):
        if not ManagerForm.objectName():
            ManagerForm.setObjectName(u"ManagerForm")
        ManagerForm.resize(760, 481)
        self.verticalLayout = QVBoxLayout(ManagerForm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 11, 0, 11)
        self.lstMain = QListWidget(ManagerForm)
        self.lstMain.setObjectName(u"lstMain")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstMain.sizePolicy().hasHeightForWidth())
        self.lstMain.setSizePolicy(sizePolicy)
        self.lstMain.setMinimumSize(QSize(0, 0))
        self.lstMain.setMaximumSize(QSize(16777215, 16777215))
        self.lstMain.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.txt_header = QLabel(ManagerForm)
        self.txt_header.setObjectName(u"txt_header")

        self.verticalLayout_4.addWidget(self.txt_header)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(ManagerForm)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.txt_game_dir = QLineEdit(ManagerForm)
        self.txt_game_dir.setObjectName(u"txt_game_dir")
        self.txt_game_dir.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.txt_game_dir)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_4)

        self.stwMain = QStackedWidget(ManagerForm)
        self.stwMain.setObjectName(u"stwMain")

        self.verticalLayout_3.addWidget(self.stwMain)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(ManagerForm)

        self.stwMain.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(ManagerForm)
    # setupUi

    def retranslateUi(self, ManagerForm):
        ManagerForm.setWindowTitle(QCoreApplication.translate("ManagerForm", u"Manager", None))
        self.txt_header.setText(QCoreApplication.translate("ManagerForm", u"name", None))
        self.label.setText(QCoreApplication.translate("ManagerForm", u"Game directory:", None))
    # retranslateUi


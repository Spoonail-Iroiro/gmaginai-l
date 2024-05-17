# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mods_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ModsWidget(object):
    def setupUi(self, ModsWidget):
        if not ModsWidget.objectName():
            ModsWidget.setObjectName(u"ModsWidget")
        ModsWidget.resize(532, 329)
        self.verticalLayout_2 = QVBoxLayout(ModsWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(ModsWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(ModsWidget)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnSelect = QPushButton(ModsWidget)
        self.btnSelect.setObjectName(u"btnSelect")

        self.verticalLayout.addWidget(self.btnSelect)

        self.btn_edit_2 = QPushButton(ModsWidget)
        self.btn_edit_2.setObjectName(u"btn_edit_2")

        self.verticalLayout.addWidget(self.btn_edit_2)

        self.btn_edit = QPushButton(ModsWidget)
        self.btn_edit.setObjectName(u"btn_edit")

        self.verticalLayout.addWidget(self.btn_edit)

        self.btn_add = QPushButton(ModsWidget)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(ModsWidget)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.btn_delete_2 = QPushButton(ModsWidget)
        self.btn_delete_2.setObjectName(u"btn_delete_2")

        self.verticalLayout.addWidget(self.btn_delete_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ModsWidget)

        QMetaObject.connectSlotsByName(ModsWidget)
    # setupUi

    def retranslateUi(self, ModsWidget):
        ModsWidget.setWindowTitle(QCoreApplication.translate("ModsWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("ModsWidget", u"Mods", None))
        self.btnSelect.setText(QCoreApplication.translate("ModsWidget", u"Enable", None))
        self.btn_edit_2.setText(QCoreApplication.translate("ModsWidget", u"\u2191", None))
        self.btn_edit.setText(QCoreApplication.translate("ModsWidget", u"\u2193", None))
        self.btn_add.setText(QCoreApplication.translate("ModsWidget", u"Add", None))
        self.btn_delete.setText(QCoreApplication.translate("ModsWidget", u"Delete", None))
        self.btn_delete_2.setText(QCoreApplication.translate("ModsWidget", u"Open mods directory", None))
    # retranslateUi


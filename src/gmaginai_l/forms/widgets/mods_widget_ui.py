# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mods_widget.ui'
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

        self.txt_main = QLabel(ModsWidget)
        self.txt_main.setObjectName(u"txt_main")
        self.txt_main.setTextFormat(Qt.TextFormat.PlainText)
        self.txt_main.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.txt_main.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.txt_main)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(ModsWidget)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_enable = QPushButton(ModsWidget)
        self.btn_enable.setObjectName(u"btn_enable")

        self.verticalLayout.addWidget(self.btn_enable)

        self.btn_up = QPushButton(ModsWidget)
        self.btn_up.setObjectName(u"btn_up")

        self.verticalLayout.addWidget(self.btn_up)

        self.btn_down = QPushButton(ModsWidget)
        self.btn_down.setObjectName(u"btn_down")

        self.verticalLayout.addWidget(self.btn_down)

        self.btn_add = QPushButton(ModsWidget)
        self.btn_add.setObjectName(u"btn_add")

        self.verticalLayout.addWidget(self.btn_add)

        self.btn_delete = QPushButton(ModsWidget)
        self.btn_delete.setObjectName(u"btn_delete")

        self.verticalLayout.addWidget(self.btn_delete)

        self.btn_open_mod_own_dir = QPushButton(ModsWidget)
        self.btn_open_mod_own_dir.setObjectName(u"btn_open_mod_own_dir")

        self.verticalLayout.addWidget(self.btn_open_mod_own_dir)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ModsWidget)

        QMetaObject.connectSlotsByName(ModsWidget)
    # setupUi

    def retranslateUi(self, ModsWidget):
        ModsWidget.setWindowTitle(QCoreApplication.translate("ModsWidget", u"Mods", None))
        self.label.setText(QCoreApplication.translate("ModsWidget", u"Mods", None))
        self.txt_main.setText("")
        self.btn_enable.setText(QCoreApplication.translate("ModsWidget", u"Enable", None))
        self.btn_up.setText(QCoreApplication.translate("ModsWidget", u"\u2191", None))
        self.btn_down.setText(QCoreApplication.translate("ModsWidget", u"\u2193", None))
        self.btn_add.setText(QCoreApplication.translate("ModsWidget", u"Install/Update", None))
        self.btn_delete.setText(QCoreApplication.translate("ModsWidget", u"Delete", None))
        self.btn_open_mod_own_dir.setText(QCoreApplication.translate("ModsWidget", u"Open mod's folder", None))
    # retranslateUi


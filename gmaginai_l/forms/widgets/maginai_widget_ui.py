# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maginai_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MaginaiWidget(object):
    def setupUi(self, MaginaiWidget):
        if not MaginaiWidget.objectName():
            MaginaiWidget.setObjectName(u"MaginaiWidget")
        MaginaiWidget.resize(533, 326)
        self.verticalLayout = QVBoxLayout(MaginaiWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.txt_main = QLabel(MaginaiWidget)
        self.txt_main.setObjectName(u"txt_main")
        self.txt_main.setMinimumSize(QSize(0, 0))
        self.txt_main.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.txt_main.setWordWrap(True)
        self.txt_main.setOpenExternalLinks(True)

        self.horizontalLayout_4.addWidget(self.txt_main)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.txt_error = QLabel(MaginaiWidget)
        self.txt_error.setObjectName(u"txt_error")
        self.txt_error.setMinimumSize(QSize(0, 0))
        self.txt_error.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.txt_error.setWordWrap(True)
        self.txt_error.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.txt_error)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btn_start_game = QPushButton(MaginaiWidget)
        self.btn_start_game.setObjectName(u"btn_start_game")

        self.horizontalLayout_9.addWidget(self.btn_start_game)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_start_game_with_console = QPushButton(MaginaiWidget)
        self.btn_start_game_with_console.setObjectName(u"btn_start_game_with_console")

        self.horizontalLayout_8.addWidget(self.btn_start_game_with_console)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_install = QPushButton(MaginaiWidget)
        self.btn_install.setObjectName(u"btn_install")

        self.horizontalLayout_5.addWidget(self.btn_install)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_uninstall_only_tags = QPushButton(MaginaiWidget)
        self.btn_uninstall_only_tags.setObjectName(u"btn_uninstall_only_tags")

        self.horizontalLayout_6.addWidget(self.btn_uninstall_only_tags)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.btn_uninstall_all = QPushButton(MaginaiWidget)
        self.btn_uninstall_all.setObjectName(u"btn_uninstall_all")

        self.horizontalLayout_7.addWidget(self.btn_uninstall_all)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(MaginaiWidget)

        QMetaObject.connectSlotsByName(MaginaiWidget)
    # setupUi

    def retranslateUi(self, MaginaiWidget):
        MaginaiWidget.setWindowTitle(QCoreApplication.translate("MaginaiWidget", u"Form", None))
        self.txt_main.setText(QCoreApplication.translate("MaginaiWidget", u"...Loading", None))
        self.txt_error.setText("")
        self.btn_start_game.setText(QCoreApplication.translate("MaginaiWidget", u"Start game", None))
        self.btn_start_game_with_console.setText(QCoreApplication.translate("MaginaiWidget", u"Start game with console", None))
        self.btn_install.setText(QCoreApplication.translate("MaginaiWidget", u"Install/Update maginai (latest)", None))
        self.btn_uninstall_only_tags.setText(QCoreApplication.translate("MaginaiWidget", u"Uninstall (only tags)", None))
        self.btn_uninstall_all.setText(QCoreApplication.translate("MaginaiWidget", u"Uninstall (all)", None))
    # retranslateUi


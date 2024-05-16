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
        MaginaiWidget.resize(533, 328)
        self.verticalLayout = QVBoxLayout(MaginaiWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(MaginaiWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_install = QPushButton(MaginaiWidget)
        self.btn_install.setObjectName(u"btn_install")

        self.horizontalLayout_5.addWidget(self.btn_install)

        self.btn_update = QPushButton(MaginaiWidget)
        self.btn_update.setObjectName(u"btn_update")

        self.horizontalLayout_5.addWidget(self.btn_update)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(MaginaiWidget)

        QMetaObject.connectSlotsByName(MaginaiWidget)
    # setupUi

    def retranslateUi(self, MaginaiWidget):
        MaginaiWidget.setWindowTitle(QCoreApplication.translate("MaginaiWidget", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("MaginaiWidget", u"maginai Status", None))
        self.btn_install.setText(QCoreApplication.translate("MaginaiWidget", u"Install maginai", None))
        self.btn_update.setText(QCoreApplication.translate("MaginaiWidget", u"Update maginai", None))
    # retranslateUi


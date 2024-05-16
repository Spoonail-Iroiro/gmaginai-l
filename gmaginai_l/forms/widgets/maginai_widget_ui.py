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
        self.pushButton = QPushButton(MaginaiWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(MaginaiWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_5.addWidget(self.pushButton_2)

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
        self.pushButton.setText(QCoreApplication.translate("MaginaiWidget", u"Install maginai", None))
        self.pushButton_2.setText(QCoreApplication.translate("MaginaiWidget", u"Update maginai", None))
    # retranslateUi


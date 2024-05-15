# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_select_form.ui'
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

class Ui_GameSelectForm(object):
    def setupUi(self, GameSelectForm):
        if not GameSelectForm.objectName():
            GameSelectForm.setObjectName(u"GameSelectForm")
        GameSelectForm.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(GameSelectForm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(GameSelectForm)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(GameSelectForm)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_select = QPushButton(GameSelectForm)
        self.btn_select.setObjectName(u"btn_select")

        self.horizontalLayout_2.addWidget(self.btn_select)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.btn_new = QPushButton(GameSelectForm)
        self.btn_new.setObjectName(u"btn_new")

        self.horizontalLayout_4.addWidget(self.btn_new)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.btn_delete = QPushButton(GameSelectForm)
        self.btn_delete.setObjectName(u"btn_delete")

        self.horizontalLayout_5.addWidget(self.btn_delete)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(GameSelectForm)

        QMetaObject.connectSlotsByName(GameSelectForm)
    # setupUi

    def retranslateUi(self, GameSelectForm):
        GameSelectForm.setWindowTitle(QCoreApplication.translate("GameSelectForm", u"\u30b2\u30fc\u30e0", None))
        self.label.setText(QCoreApplication.translate("GameSelectForm", u"\u30b2\u30fc\u30e0\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044", None))
        self.btn_select.setText(QCoreApplication.translate("GameSelectForm", u"\u9078\u629e", None))
        self.btn_new.setText(QCoreApplication.translate("GameSelectForm", u"\u65b0\u898f\u4f5c\u6210", None))
        self.btn_delete.setText(QCoreApplication.translate("GameSelectForm", u"\u524a\u9664", None))
    # retranslateUi


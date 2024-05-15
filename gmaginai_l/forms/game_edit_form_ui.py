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
    QWidget)

class Ui_GameEditForm(object):
    def setupUi(self, GameEditForm):
        if not GameEditForm.objectName():
            GameEditForm.setObjectName(u"GameEditForm")
        GameEditForm.resize(525, 175)
        self.formLayout = QFormLayout(GameEditForm)
        self.formLayout.setObjectName(u"formLayout")
        self.txt_name = QLineEdit(GameEditForm)
        self.txt_name.setObjectName(u"txt_name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txt_name)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txt_bak = QLineEdit(GameEditForm)
        self.txt_bak.setObjectName(u"txt_bak")

        self.horizontalLayout.addWidget(self.txt_bak)

        self.btn_bak = QPushButton(GameEditForm)
        self.btn_bak.setObjectName(u"btn_bak")

        self.horizontalLayout.addWidget(self.btn_bak)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txt_restore = QLineEdit(GameEditForm)
        self.txt_restore.setObjectName(u"txt_restore")

        self.horizontalLayout_2.addWidget(self.txt_restore)

        self.btn_restore = QPushButton(GameEditForm)
        self.btn_restore.setObjectName(u"btn_restore")

        self.horizontalLayout_2.addWidget(self.btn_restore)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.txt_game = QLineEdit(GameEditForm)
        self.txt_game.setObjectName(u"txt_game")

        self.horizontalLayout_3.addWidget(self.txt_game)

        self.btn_game = QPushButton(GameEditForm)
        self.btn_game.setObjectName(u"btn_game")

        self.horizontalLayout_3.addWidget(self.btn_game)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label = QLabel(GameEditForm)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(GameEditForm)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(GameEditForm)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(GameEditForm)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)


        self.retranslateUi(GameEditForm)

        QMetaObject.connectSlotsByName(GameEditForm)
    # setupUi

    def retranslateUi(self, GameEditForm):
        GameEditForm.setWindowTitle(QCoreApplication.translate("GameEditForm", u"\u30b2\u30fc\u30e0\u767b\u9332", None))
        self.btn_bak.setText(QCoreApplication.translate("GameEditForm", u"\u53c2\u7167", None))
        self.btn_restore.setText(QCoreApplication.translate("GameEditForm", u"\u53c2\u7167", None))
        self.btn_game.setText(QCoreApplication.translate("GameEditForm", u"\u53c2\u7167", None))
        self.label.setText(QCoreApplication.translate("GameEditForm", u"\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u30d5\u30a9\u30eb\u30c0", None))
        self.label_2.setText(QCoreApplication.translate("GameEditForm", u"\u5fa9\u5143\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u30d5\u30a9\u30eb\u30c0", None))
        self.label_3.setText(QCoreApplication.translate("GameEditForm", u"\u30b2\u30fc\u30e0\u30d5\u30a9\u30eb\u30c0", None))
        self.label_4.setText(QCoreApplication.translate("GameEditForm", u"\u540d\u524d", None))
    # retranslateUi


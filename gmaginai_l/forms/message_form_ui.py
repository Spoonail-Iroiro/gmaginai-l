# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'message_form.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MessageForm(object):
    def setupUi(self, MessageForm):
        if not MessageForm.objectName():
            MessageForm.setObjectName(u"MessageForm")
        MessageForm.resize(410, 142)
        self.verticalLayout = QVBoxLayout(MessageForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.txt_main = QLabel(MessageForm)
        self.txt_main.setObjectName(u"txt_main")
        self.txt_main.setScaledContents(False)
        self.txt_main.setWordWrap(True)
        self.txt_main.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.txt_main)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.bbx_main = QDialogButtonBox(MessageForm)
        self.bbx_main.setObjectName(u"bbx_main")
        self.bbx_main.setOrientation(Qt.Horizontal)
        self.bbx_main.setStandardButtons(QDialogButtonBox.NoButton)

        self.verticalLayout.addWidget(self.bbx_main)


        self.retranslateUi(MessageForm)

        QMetaObject.connectSlotsByName(MessageForm)
    # setupUi

    def retranslateUi(self, MessageForm):
        MessageForm.setWindowTitle(QCoreApplication.translate("MessageForm", u"Message", None))
        self.txt_main.setText("")
    # retranslateUi


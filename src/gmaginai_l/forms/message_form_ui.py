# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'message_form.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MessageForm(object):
    def setupUi(self, MessageForm):
        if not MessageForm.objectName():
            MessageForm.setObjectName(u"MessageForm")
        MessageForm.resize(480, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MessageForm.sizePolicy().hasHeightForWidth())
        MessageForm.setSizePolicy(sizePolicy)
        MessageForm.setMinimumSize(QSize(480, 150))
        MessageForm.setMaximumSize(QSize(16777215, 16777215))
        MessageForm.setModal(False)
        self.verticalLayout = QVBoxLayout(MessageForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.txt_main = QLabel(MessageForm)
        self.txt_main.setObjectName(u"txt_main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.txt_main.sizePolicy().hasHeightForWidth())
        self.txt_main.setSizePolicy(sizePolicy1)
        self.txt_main.setMinimumSize(QSize(460, 0))
        self.txt_main.setMaximumSize(QSize(460, 16777215))
        self.txt_main.setTextFormat(Qt.TextFormat.PlainText)
        self.txt_main.setScaledContents(False)
        self.txt_main.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.txt_main.setWordWrap(True)
        self.txt_main.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.txt_main)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.bbx_main = QDialogButtonBox(MessageForm)
        self.bbx_main.setObjectName(u"bbx_main")
        self.bbx_main.setOrientation(Qt.Orientation.Horizontal)
        self.bbx_main.setStandardButtons(QDialogButtonBox.StandardButton.NoButton)

        self.verticalLayout.addWidget(self.bbx_main)


        self.retranslateUi(MessageForm)

        QMetaObject.connectSlotsByName(MessageForm)
    # setupUi

    def retranslateUi(self, MessageForm):
        MessageForm.setWindowTitle(QCoreApplication.translate("MessageForm", u"Message", None))
        self.txt_main.setText("")
    # retranslateUi


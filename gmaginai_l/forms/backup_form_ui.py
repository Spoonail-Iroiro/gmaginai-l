# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backup_form.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_BackupForm(object):
    def setupUi(self, BackupForm):
        if not BackupForm.objectName():
            BackupForm.setObjectName(u"BackupForm")
        BackupForm.resize(668, 507)
        self.horizontalLayout = QHBoxLayout(BackupForm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lstMain = QListWidget(BackupForm)
        self.lstMain.setObjectName(u"lstMain")

        self.horizontalLayout.addWidget(self.lstMain)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(BackupForm)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.txtGameSaveDir = QLineEdit(BackupForm)
        self.txtGameSaveDir.setObjectName(u"txtGameSaveDir")

        self.verticalLayout.addWidget(self.txtGameSaveDir)

        self.label_2 = QLabel(BackupForm)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.txtSaveBackupRoot = QLineEdit(BackupForm)
        self.txtSaveBackupRoot.setObjectName(u"txtSaveBackupRoot")

        self.verticalLayout.addWidget(self.txtSaveBackupRoot)

        self.groupBox = QGroupBox(BackupForm)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.txtSaveTag = QLineEdit(self.groupBox)
        self.txtSaveTag.setObjectName(u"txtSaveTag")

        self.verticalLayout_2.addWidget(self.txtSaveTag)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnSave = QPushButton(self.groupBox)
        self.btnSave.setObjectName(u"btnSave")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.btnSave)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(BackupForm)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.btnRestore = QPushButton(self.groupBox_2)
        self.btnRestore.setObjectName(u"btnRestore")

        self.horizontalLayout_3.addWidget(self.btnRestore)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.lblSpecial = QLabel(BackupForm)
        self.lblSpecial.setObjectName(u"lblSpecial")
        self.lblSpecial.setStyleSheet(u"color: rgb(255, 0, 0);\n"
"font: 75 11pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.verticalLayout.addWidget(self.lblSpecial)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(BackupForm)
        self.btnSave.clicked.connect(BackupForm.btnSave_clicked)
        self.btnRestore.clicked.connect(BackupForm.btnRestore_clicked)

        QMetaObject.connectSlotsByName(BackupForm)
    # setupUi

    def retranslateUi(self, BackupForm):
        BackupForm.setWindowTitle(QCoreApplication.translate("BackupForm", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("BackupForm", u"\u30b2\u30fc\u30e0\u30bb\u30fc\u30d6\u30d5\u30a9\u30eb\u30c0\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("BackupForm", u"\u30bb\u30fc\u30d6\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u30d5\u30a9\u30eb\u30c0\u30eb\u30fc\u30c8\uff1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("BackupForm", u"GroupBox", None))
        self.label_3.setText(QCoreApplication.translate("BackupForm", u"\u30bb\u30fc\u30d6\u30bf\u30b0", None))
        self.btnSave.setText(QCoreApplication.translate("BackupForm", u"\u4fdd\u5b58", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("BackupForm", u"GroupBox", None))
        self.label_4.setText(QCoreApplication.translate("BackupForm", u"\u9078\u629e\u3057\u305f\u30bb\u30fc\u30d6\u3092", None))
        self.btnRestore.setText(QCoreApplication.translate("BackupForm", u"\u5fa9\u5143", None))
        self.lblSpecial.setText(QCoreApplication.translate("BackupForm", u"Save method: Preview", None))
    # retranslateUi


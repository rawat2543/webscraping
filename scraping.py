from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.request
from bs4 import BeautifulSoup
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.widget_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loaddata)#connect a method to click event
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEditUrl")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.gridLayout_2.addWidget(self.widget_3, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ชื่อสินค้า"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ราคา"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "น้ำหนัก"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "stock"))
        self.pushButton.setText(_translate("MainWindow", "TakeOver"))
        self.label.setText(_translate("MainWindow", "Url : "))
        

    def loaddata(self):
        btv_url = urllib.request.urlopen(self.lineEdit.text())
        btv_html = btv_url.read()
        #btv_html_decode = mybytes.decode("utf8")
        btv_url.close()

        soup = BeautifulSoup(btv_html, "lxml")
        self.tableWidget.setRowCount(0)
        count_p = 0
        for index, product_data in enumerate(soup.findAll('li', id=re.compile('^product_list_item_'))):
            if str(product_data).find('Pre-order') != -1 or str(product_data).find('ซื้อได้ที่สาขาเท่านั้น') != -1 or str(product_data).find('สินค้าหมด') != -1:
                self.progressBar.setProperty("value", (index+1)*100/36)
                continue
            product_url = product_data.find("a", {"class": "product-image"}).get('href')
            Product_get = urllib.request.urlopen(product_url)
            Product_html = Product_get.read()
            Product_get.close()

            soupproduct = BeautifulSoup(Product_html, "lxml")
            #Start Get Name Title
            name_title = soupproduct.find("p", {"class": "h1 product-name"}).getText()
            #End Get Name Title

            #Start Get availability in-stock
            instock = soupproduct.find("p", {"class": "availability in-stock"}).getText()
            if str(instock).find('สินค้าพร้อมส่ง') != -1:
                instock = 'สินค้าพร้อมส่ง'
            else:
                instock = 'ไม่พร้อมส่ง'
                #continue
            #End Get availability in-stock

            #Start Get price
            price = soupproduct.find('span', id=re.compile('^product-price-')).getText()
            price = re.sub("[^\d\.]", "", price)
            #End Get price


            #Start Get Image
            image = soupproduct.find("div", {"id": "amasty_gallery"})
            p = re.compile('data-zoom-image="(.*)" rel="group" title="">')
            image_arr = p.findall(str(image))
            #End Get Image


            #Start Get product detail
            p_detail = soupproduct.find("table", {"id": "product-attribute-specs-table"})
            p_detail_list = str(p_detail).split("<tr>")

            my_dict={}
            for p_detailIndex, p_detail_data in enumerate(p_detail_list):
                
                p = re.compile('<th class="label">(.*?)<\/th>')
                p_name = p.findall(str(p_detail_data))

                if(p_name):
                    obj_name = p_name[0]
                    my_dict.update({obj_name : 1})
                


            print(my_dict['รหัสสินค้า'])
            #End Get product detail


            #print(p_detail)
            self.tableWidget.insertRow(count_p)
            self.tableWidget.setItem(count_p, 0, QtWidgets.QTableWidgetItem(name_title))
            self.tableWidget.setItem(count_p, 1, QtWidgets.QTableWidgetItem(price))
            self.tableWidget.setItem(count_p, 3, QtWidgets.QTableWidgetItem(instock))
            self.tableWidget.update()
            count_p = count_p+1
            
            print('################################################################')
            self.progressBar.setProperty("value", (index+1)*100/36)
       
            #self.tableWidget.insertRow(row_number)
            #self.tableWidget.setItem(row_number, 0, QtWidgets.QTableWidgetItem(link.get('href')))
            #self.progressBar.setProperty("value", (row_number+1)*100/36)


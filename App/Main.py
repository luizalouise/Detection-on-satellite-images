import sys
import json
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QFileDialog, QPushButton, QLabel, QMainWindow, QMessageBox, QVBoxLayout)
from PyQt5.QtGui import (QPixmap, QCursor)
from PyQt5.QtCore import Qt
import info
import torch
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import (QtGui, QtCore, QtWidgets)
import cv2
import os
import pathlib
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QDialog, QApplication
import Detection
import Copernicus
from folium.plugins.draw import Draw
import io
import codecs

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.image = None
        self.setAlignment(Qt.AlignCenter)
        # self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setText('\n\n Upuść tutaj zdjęcie \n\n')
        self.setStyleSheet("color: #27187E")
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class GoogleEarthApp(QDialog):
    def __init__(self):
        super(GoogleEarthApp, self).__init__()

        #self.setWindowTitle("Rozpoznawanie obiektów - zdjęcia satelitarne")

        #self.resize(1100, 650)
        #self.setStyleSheet("background-color: #180e52")
        self.setAcceptDrops(True)

        self.buttons()



        self.labelImage = QLabel(self)
        self.labelImage.resize(700, 465)
        self.labelImage.move(300, 50)
        self.labelImage.setStyleSheet(
            "color: #758BFD;"
            'font: bold 15px; '
            'min-width: 10em; '
            'border-style: dashed; '
            "border-color: #FF8600; "
            'border-radius: 10px; '
            'border-width: 4px; '

        )
        self.labelImage.setText('\n\n Upuść tutaj zdjęcie \n\n')
        self.labelImage.setAlignment(Qt.AlignCenter)

        self.file_path = None
        self.image = None
        pathlib.PosixPath = pathlib.WindowsPath
        menu = MenuApp()

        self.model = menu.returnModel()

        self.model.eval()
        #self.flag = None

    def buttons(self):
        button1 = QPushButton('Wybierz zdjęcie', self)
        button1.resize(200, 64)
        button1.move(50, 50)
        button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button1.clicked.connect(self.get_image_file)

        button1.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button2 = QPushButton('Detekcja obiektów', self)
        button2.resize(200, 64)
        button2.move(50, 150)
        button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button2.clicked.connect(self.detection)
        button2.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button3 = QPushButton('Zapisz zdjęcie', self)
        button3.resize(200, 64)
        button3.move(50, 250)
        button3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button3.clicked.connect(self.image_save)
        button3.setShortcut("Ctrl+S")
        button3.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")
        button4 = QPushButton('Usuń zdjęcie', self)
        button4.resize(200, 64)
        button4.move(50, 350)
        button4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button4.clicked.connect(self.delete_image)

        button4.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button5 = QPushButton('Informacje', self)
        button5.resize(200, 64)
        button5.move(50, 450)
        button5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button5.clicked.connect(self.go_to_info)

        button5.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button6 = QPushButton('Menu', self)
        button6.resize(200, 64)
        button6.move(550, 550)
        button6.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button6.clicked.connect(self.go_to_menu)

        button6.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

    def go_to_menu(self):
        menu_screen = MenuApp()
        widget.addWidget(menu_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_info(self):
        info_screen = InfoApp()
        widget.addWidget(info_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def detection(self):
        modelClass = Detection.Detection()
        self.image = modelClass.making_detection(self.file_path, self.model)
        #self.flag = 1

        if self.image == None:
            self.set_image(self.file_path)
            msg = QMessageBox()
            msg.setWindowTitle("Komunikat")
            msg.setText("Nie znaleziono żadnego obiektu")
            x = msg.exec_()
        else:
            #self.image.save("image2.png")
            self.set_image(self.image)

    #def returnflag(self):
       # return self.flag

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.file_path = file_path

        self.labelImage.setPixmap(QPixmap(file_path).scaled(700, 465, Qt.KeepAspectRatio))

    def get_image_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>",
                                                   "Image files (*.jpg *.jpeg *.png)")

        self.set_image(file_name)

    #def closeMyApp_OpenNewApp(self):
     #   self.close()
      #  self.Open = info.InfoApp()
       # self.Open.show()

    def delete_image(self):
        self.labelImage.clear()
        self.labelImage.setAlignment(Qt.AlignCenter)
        self.labelImage.setText('\n\n Upuść tutaj zdjęcie \n\n')
        self.labelImage.setStyleSheet(
            "color: #758BFD;"
            'font: bold 15px; '
            'min-width: 10em; '
            'border-style: dashed; '
            "border-color: #FF8600; "
            'border-radius: 10px; '
            'border-width: 4px; '

        )
        self.file_path = None
        self.image = None

    #def infoBox(self):
     #   msg = QMessageBox()
      #  msg.setWindowTitle("Informacje")
       # msg.setText("Program umożliwa detekcje statków, samochodów i samolotów ze zdjęć satelitarnych")
        #x = msg.exec_()

    def image_save(self):
        if self.file_path is not None:
            file_name = QFileDialog.getSaveFileName(self, 'Save File')
            file_name = file_name[0]

            file_name = file_name + '.jpg'
            image = self.image.save(file_name)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Komunikat")
            msg.setText("Musisz najpierw wybrać zdjęcie")
            x = msg.exec_()


class MenuApp(QDialog):
    def __init__(self):
        super(MenuApp, self).__init__()
        text = QLabel(self)
        text.move(150, 50)
        text.setText("Wybierz zbiór na jakim był trenowany model")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet(
            "color: #FFEAEE;"
            'font: bold 35px; '

        )

        # self.Open = None

        #self.setWindowTitle("Rozpoznawanie obiektów - zdjęcia satelitarne")
        #self.resize(1100, 650)
        #self.setStyleSheet("background-color: #180e52")
        self.buttons()

        pathlib.PosixPath = pathlib.WindowsPath
        self.model = torch.load("best_google.pth", map_location=torch.device('cpu'))
        print(type(self.model))

    def buttons(self):
        button1 = QPushButton('Google', self)
        button1.resize(300, 300)
        button1.clicked.connect(self.gotoGoogle)

        button1.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 30px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button1.move(550, 200)

        button2 = QPushButton('Copernicus', self)
        button2.resize(300, 300)
        button2.clicked.connect(self.gotoMap)

        button2.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 30px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button2.move(150, 200)

    def gotoGoogle(self):
        googlescreen = GoogleEarthApp()
        widget.addWidget(googlescreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoMenu(self):
        mainwindow = MenuApp()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoMap(self):
        mapscreen = Map()
        widget.addWidget(mapscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def returnModel(self):
        return self.model

#wybierz zbiór na jakim był trenowany model


class CopernicusApp(QDialog):
    def __init__(self):
        super(CopernicusApp, self).__init__()

        #self.setWindowTitle("Rozpoznawanie obiektów - zdjęcia satelitarne")
        #self.resize(1100, 650)
        #self.setStyleSheet("background-color: #180e52")
        self.image = None

        self.buttons()

        self.showImage()

        self.file_path = str((os.path.dirname(os.path.abspath(__file__)))) + "\\" + "cop_img.png"

        pathlib.PosixPath = pathlib.WindowsPath
        self.model = torch.load("best_copernicus.pth", map_location=torch.device('cpu'))
        self.model.eval()

        detection = Detection.Detection()

        self.image = detection.making_detection(self.file_path, self.model)

        if self.image == None:
            self.set_image(self.file_path)
            msg = QMessageBox()
            msg.setWindowTitle("Komunikat")
            msg.setText("Nie znaleziono żadnego obiektu")
            x = msg.exec_()
        else:

            self.set_image(self.image)
            #self.labelImage.setPixmap(self.image)

    def showImage(self):
        copernicus = Copernicus.Copernicus()
        self.image = copernicus.download_image()

        # self.labelImage.setPixmap("test.png")
        self.set_image("cop_img.png")  # co jak nie będzie pobranego zdjęcia trzeba dać wyjątek
        #self.labelImage.setPixmap("cop_img.png")

    def buttons(self):
        button1 = QPushButton('Zapisz zdjęcie', self)
        button1.resize(200, 64)
        button1.move(50, 100)
        button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button1.clicked.connect(self.image_save)

        button1.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button2 = QPushButton('Powrót', self)
        button2.resize(200, 64)
        button2.move(50, 200)
        button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button2.clicked.connect(self.go_to_mapy_screen)
        button2.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button3 = QPushButton('Menu', self)
        button3.resize(200, 64)
        button3.move(50, 300)
        button3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button3.clicked.connect(self.go_to_menu)
        button3.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button4 = QPushButton('Informacje', self)
        button4.resize(200, 64)
        button4.move(50, 400)
        button4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button4.clicked.connect(self.go_to_info)
        button4.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        #usunąć self
        self.labelImage = QLabel(self)
        self.labelImage.resize(700, 465)
        self.labelImage.move(300, 50)
        self.labelImage.setStyleSheet(
            "color: #758BFD;"
            'font: bold 15px; '
            'min-width: 10em; '
            'border-style: dashed; '
            "border-color: #FF8600; "
            'border-radius: 10px; '
            'border-width: 4px; '

        )


    def image_save(self):
        if self.file_path is not None:
            file_name = QFileDialog.getSaveFileName(self, 'Save File')
            file_name = file_name[0]

            file_name = file_name + '.png'
            image = self.image.save(file_name)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Komunikat")
            msg.setText("Musisz najpierw wybrać zdjęcie")
            x = msg.exec_()

    def go_to_menu(self):
        menu_screen = MenuApp()
        widget.addWidget(menu_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        # widget.setStyleSheet(menuscreen)

    def go_to_info(self):
        info_screen = InfoApp()
        widget.addWidget(info_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

   # def tmp(self):
    #    print('tmp')

    def set_image(self, file_path):
        self.file_path = file_path
        self.labelImage.setPixmap(QPixmap(file_path).scaled(700, 465, Qt.KeepAspectRatio))

    def go_to_mapy_screen(self):
        main_window = Map()
        widget.addWidget(main_window)
        widget.setCurrentIndex(widget.currentIndex() + 1)

   # def image_save(self):
    #    if self.file_path is not None:
     #       file_name = QFileDialog.getSaveFileName(self, 'Save File')
      #      file_name = file_name[0]

       #     file_name = file_name + '.png'
        #    image = self.image
         #   image.save(file_name)

    #def go_to_menu(self):
     ##  widget.addWidget(main_window)
      #  widget.setCurrentIndex(widget.currentIndex() + 1)


class Map(QDialog):
    def __init__(self):
        super(Map, self).__init__()
        self.path_geojson = None
        self.webEngineView = None

        self.layout = QVBoxLayout(self)
        self.map_interface()
        self.button()

    def button(self):
        button1 = QPushButton('Detekcja', self)
        self.layout.addWidget(button1)
        button1.resize(200, 64)
        button1.clicked.connect(self.go_to_copernicus)

        button1.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button2 = QPushButton('Menu', self)
        self.layout.addWidget(button2)
        button2.resize(200, 64)
        button2.clicked.connect(self.go_to_menu)

        button2.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

    def map_interface(self):
        self.webEngineView = QWebEngineView()
        self.webEngineView.page().profile().downloadRequested.connect(
            self.handle_download_requested

        )
        self.load_page()

        self.layout.addWidget(self.webEngineView)

        self.setWindowTitle("mapy")

    def go_to_copernicus(self):
        copernicus_screen = CopernicusApp()
        widget.addWidget(copernicus_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_menu(self):
        menu_screen = MenuApp()
        widget.addWidget(menu_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    #def go_to_main_screen(self):
     #   main_window = Map()
      #  widget.addWidget(main_window)
       # widget.setCurrentIndex(widget.currentIndex() + 1)

    def load_page(self):
        m = folium.Map(location=[51.7687323, 19.4569911], zoom_start=5)
        Draw(
            export=True,
            filename="my_data.geojson",
            position="topleft",
            draw_options={
                "polyline": False,
                "rectangle": True,
                "circle": False,
                "circlemarker": False,
                "marker": False,
                "circlemarker": False,
                "polygon": False
            },
            edit_options={"poly": {"allowIntersection": False}},
        ).add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webEngineView.setHtml(data.getvalue().decode())

    def handle_download_requested(self, item):
        path = str((os.path.dirname(os.path.abspath(__file__)))) + "\\" + "file.geojson"
        path = path.replace(os.sep, '/')

        item.setPath(path)
        self.path_geojson = path

        item.accept()

class InfoApp(QDialog):
    def __init__(self):
        super(InfoApp,self).__init__()
        # self.Open = None
        #self.setWindowTitle("Rozpoznawanie obiektów - zdjęcia satelitarne")
        #self.resize(1100, 650)
        #self.setStyleSheet("background-color: #180e52")

        button1 = QPushButton('Powrót', self)
        button1.resize(200, 64)
        button1.clicked.connect(self.go_to_menu)

        button1.setStyleSheet("*{ background-color: #758BFD;" +
                              'border-style: outset; ' +
                              'border-width: 2px; ' +
                              'border-radius: 10px; ' +
                              "border-color: #FF8600; " +
                              'font: bold 15px; ' +
                              'min-width: 10em; ' +
                              'padding: 6px;' +
                              "color: #27187E}" +
                              "*:hover{background-color: '#FFEAEE';}")

        button1.move(450, 350)
        f = codecs.open("info.txt", 'r', 'utf-8')
        info = f.read()
        f.close()
        text = QLabel(self)
        text.setText(info)

        text.resize(950, 300)
        text.setStyleSheet("*{ font: bold 15px; " +
                           'min-width: 10em; ' +
                           'padding: 6px;' +
                           "color: #758BFD}")

        text.move(50, 50)

    def go_to_menu(self):
        menu_screen = MenuApp()
        widget.addWidget(menu_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

   # def get_filename(self):
    #    return str(self.path_geojson)

   # def open_json(self):
    #    if self.get_filename() != 'None':
     #       with open(self.get_filename()) as json_file:
      #          data = json.load(json_file)

    #def return_model(self):
     #   return self.model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_window = MenuApp()

    widget.addWidget(main_window)

    widget.setWindowTitle("Rozpoznawanie obiektów na zdjęciach satelitarnych")
    widget.setStyleSheet("background-color: #180e52")
    widget.setFixedHeight(650)
    widget.setFixedWidth(1100)
    widget.show()

    sys.exit(app.exec_())

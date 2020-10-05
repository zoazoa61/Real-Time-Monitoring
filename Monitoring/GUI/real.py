# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from couchbase.cluster import Cluster, PasswordAuthenticator
from functools import partial
import pyqtgraph as pg
import time, random, datetime
import numpy as np
import sys
import pyautogui
from urllib.request import urlopen, Request
import urllib
import bs4

pg.setConfigOption('background', (245,245,245))
pg.setConfigOption('foreground', (0,0,0))
#pg.TextItem()
cluster = Cluster('YOURIPADDRESS')
cluster.authenticate(PasswordAuthenticator('YOURID', 'YOURPW'))

s = cluster.open_bucket('second')
q = cluster.open_bucket('quarterly')
h = cluster.open_bucket('hourly')
d = cluster.open_bucket('daily')
g = cluster.open_bucket('gist')

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs): # the meaning of *args is *argument (여러개의 인자를 함수로 받을 때 사용 즉, 몇개를 받을지 모를때) 튜플 형태로 저장된다. , **kwargs is keyword argument so, when we use dictionary? (딕셔너리로 쓸때)
        super().__init__(*args, **kwargs)
        #self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)
        font = QtGui.QFont()
        font.setPixelSize(13)
        font.setBold(True)
        self.tickFont = font
        self.setTickSpacing(3600*3, 3600)
    def tickStrings(self, values, scale, spacing): #현재 time을 나타내는 전체숫자를 시간 데이터로 바꿔준다.
           #override 하여, tick 옆에 써지는 문자를 원하는대로 수정함.
           # values --> x축 값들   ; 숫자로 이루어진 Itarable data --> ex) List[int]
        # print("--tickStrings valuse ==>", values)
        return [time.strftime("%H:%M", time.localtime(local_time)) for local_time in values]


class TimeAxisItem2(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableAutoSIPrefix(False)
        font = QtGui.QFont()
        font.setPixelSize(13)
        font.setBold(True)
        self.tickFont = font
        self.setTickSpacing(86400,86400)
    def tickStrings(self, values, scale, spacing):
        return [time.strftime("%m/%d ", time.localtime(local_time-9*3600)) for local_time in values]

class Main_Window(QtWidgets.QMainWindow):
     def __init__(self, parent=None):
         super(Main_Window, self).__init__(parent)
         #super().__init__()

         self.building_names = {"building9":"Mechanical Engineering","building26":"Artificial Turf Field",
          "building18": "Oryonggwan","building20":"International Dormitory","building19":"Graduate Dormitory 1~9",
         "building24":"Student Hall 1","building32":"Administration Center","building37":"DASAN Building"
          ,"building38":"Student Hall 2","building11":"APRI", "building36":"RISE", "building7":"Life Science"
           ,"building8":"Environmental Engineering","building14":"Kumho Research" ,"building6":"Material Science and Engineering"
        ,"building10":"SAMSUNG Research","building33":"Undegraduate A","building34":"Undergraduate B"
        ,"building35":"Undergraduate C","building2":"EECS A","building13":"KUMHO"}

         self.buildings = {}
         self.plotdata = {'x': [],'x2':[]}
         self.temperature = "null"

         for i in range(43):
             i_str = str(i)
             self.plotdata["building"+i_str] = [np.array([]),np.array([])]
             self.buildings["building"+i_str] = False

         self.timestamp1 = 0
         self.timestamp2 = 0

         self.mecha = Mecha_Widget()
         self.main = Main_Widget()

         self.setGeometry(QtCore.QRect(250, 250, 1920, 1080))
         self.get_data()
         self.mainset()
         self.showFullScreen()

     def exit(self):
         sys.exit(app.exec_())

     def mainset(self,num = 0):

         unit = " kW"

         num_str = str(num)
         self.maincheck = True
         self.buildings["building"+num_str] = False
         self.main.setup(self)

         grad_power = int(self.plotdata['building0'][0][-1])
         undergrad_power = int(self.plotdata['building1'][0][-1])
         total_power = str(grad_power + undergrad_power) + unit
         grad_power = str(grad_power) + unit
         undergrad_power = str(undergrad_power) + unit

         self.main.subbox_title[3].setText(total_power)
         self.main.subbox_title[4].setText(grad_power)
         self.main.subbox_title[5].setText(undergrad_power)

         for i in range(43):
             self.main.button_list[i].clicked.connect(partial(self.mechaset,i))

         self.main.btnend.clicked.connect(self.exit)
         self.main.btnend_sub.clicked.connect(self.exit)

     def mechaset(self,num):
         num_str = str(num)
         self.buildings["building"+num_str] = True
         self.maincheck = False
         self.mecha.setup(self)
         self.mecha.btn.clicked.connect(partial(self.mainset,num))
         self.mecha.btn_sub.clicked.connect(partial(self.mainset,num))

     def get_data(self):

         try:
             location = '오룡동'
             enc_location = urllib.parse.quote(location + '+날씨')

             url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

             req = Request(url)
             page = urlopen(req)
             html = page.read()
             soup = bs4.BeautifulSoup(html, 'html5lib')
             self.temperature = soup.find('p', class_='info_temperature').find('span',class_='todaytemp').text
         except:
             print("..")

         timestamp_present = time.time()#-86400
         time_format = '%Y-%m-%d %H:%M:%S'
         time_format2 = '%Y-%m-%d'
         time_format3 = '%Y-%m-%d %H:%M'

         results = []
         date2 = time.strftime(time_format2, time.localtime(timestamp_present))
         for i in range(6,-1,-1):
             date = time.strftime(time_format2,time.localtime(timestamp_present-i*86400))
             try :
                results.append(g.get("gist_buildings_" + date + ".csv"))
             except:
                results.append(g.get("gist_buildings_" + date2 + ".csv"))

         big_data = []
         self.plotdata['x2'] = []
         self.plotdata['x'] = []
         for i in range(43):
             i_str = str(i)
             self.plotdata["building"+i_str] = [np.array([]),np.array([])]

         for i in range(7):
             result = list(results[i].value.items())
             del result[0]
             print(result[1])
             for j in result:
                 try:
                     now = time.strptime(j[0], time_format)
                 except:
                     now = time.strptime(j[0], time_format3)
                 now2 = time.mktime(now)
                 big_data.append((int(now2)+3600*9,j[1]))

         big_data.sort()

         for i in big_data:
             self.plotdata['x2'].append(i[0])
             for j in range(43):
                 j_str = str(j)
                 self.plotdata['building' + j_str][1] = np.append(self.plotdata['building' + j_str][1],
                                                                  float(i[1][j]))

         result2 = list(results[6].value.items())

         del result2[0]

         print(result2)
         start_time = result2[0][0]
         exam1 = start_time
         exam1 = exam1[0:10]+" 00:00:00"
         exam2 = exam1[0:10] + " 23:55:00"
         print(start_time)
         self.timestamp1 = time.mktime(time.strptime(exam1,time_format))
         self.timestamp2 = time.mktime(time.strptime(exam2, time_format))

         for i in range(len(result2)):
             result2[i] = list(result2[i])
             try:
                 result2[i][0] = time.mktime(time.strptime(result2[i][0], time_format))
             except:
                 result2[i][0] = time.mktime(time.strptime(result2[i][0], time_format3))

         result2.sort()

         for at in result2:
             self.plotdata['x'].append(int(at[0]))
             for j in range(43):
                 j_str = str(j)
                 self.plotdata['building' + j_str][0] = np.append(self.plotdata['building' + j_str][0], float(at[1][j]))

     def mousecheck(self):
        #print(pyautogui.position())
        unit = " kW"
        if self.maincheck == True:
            x,y = pyautogui.position()
            if 650<x and x<734 and y>620 and y<678:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Mechanical  \n Engineering")
                    self.main.speechbubble9.move(640, 530)
                    self.main.speechbubble9_2.move(644, 525)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 190<x and x<370 and y>770 and y<897:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Artificial \n Turf Field")
                    self.main.speechbubble9.move(240,660)
                    self.main.speechbubble9_2.move(255, 655)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 360<x and x<480 and y>697 and y<748:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Oryonggwan ")
                    self.main.speechbubble9.move(370,597)
                    self.main.speechbubble9_2.move(374, 592)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 412<x and x<459 and y>603 and y<641:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" International \n   Dormitory ")
                    self.main.speechbubble9.move(390,503)
                    self.main.speechbubble9_2.move(394, 498)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 274<x and x<387 and y>565 and y<625:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("   Graduate \n   Dormitory\n       1~9 ")
                    self.main.speechbubble9.move(284,465)
                    self.main.speechbubble9_2.move(288,460)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 645<x and x<693 and y>507 and y<540:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Student Hall \n        1")
                    self.main.speechbubble9.move(620,400)
                    self.main.speechbubble9_2.move(625,395)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 754<x and x<830 and y>670 and y<711:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("Admin Center")
                    self.main.speechbubble9.move(739,563)
                    self.main.speechbubble9_2.move(744,558)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1041<x and x<1126 and y>560 and y<620:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("     DASAN\n    Building")
                    self.main.speechbubble9.move(1021,478)
                    self.main.speechbubble9_2.move(1026,470)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1368<x and x<1483 and y>573 and y<632:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Student Hall \n        2")
                    self.main.speechbubble9.move(1375,475)
                    self.main.speechbubble9_2.move(1380,470)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1151<x and x<1273 and y>761 and y<827:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("      APRI")
                    self.main.speechbubble9.move(1170,660)
                    self.main.speechbubble9_2.move(1175,655)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1148<x and x<1267 and y>579 and y<632:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("      RISE")
                    self.main.speechbubble9.move(1145,475)
                    self.main.speechbubble9_2.move(1150,470)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 928<x and x<963 and y>721 and y<773:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("Material Sci..")
                    self.main.speechbubble9.move(890,620)
                    self.main.speechbubble9_2.move(895,615)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 853<x and x<912 and y>689 and y<737:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Environ.. \n Engineering")
                    self.main.speechbubble9.move(835,585)
                    self.main.speechbubble9_2.move(840,580)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 799<x and x<875 and y>744 and y<798:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Life Science")
                    self.main.speechbubble9.move(780,625)
                    self.main.speechbubble9_2.move(785,620)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 894<x and x<940 and y>802 and y<842:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("    KUMHO\n   Reserach  ")
                    self.main.speechbubble9.move(880,700)
                    self.main.speechbubble9_2.move(885,695)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 987<x and x<1082 and y>627 and y<680:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("  SAMSUNG\n   Reserach  ")
                    self.main.speechbubble9.move(980,520)
                    self.main.speechbubble9_2.move(985,515)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1195<x and x<1310 and y>530 and y<590:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Undergradu..\n        A  ")
                    self.main.speechbubble9.move(1195,450)
                    self.main.speechbubble9_2.move(1200,445)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1247<x and x<1347 and y>500 and y<530:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Undergradu..\n        B  ")
                    self.main.speechbubble9.move(1247,420)
                    self.main.speechbubble9_2.move(1252,415)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 1311<x and x<1390 and y>472 and y<500:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText(" Undergradu..\n        C  ")
                    self.main.speechbubble9.move(1300,390)
                    self.main.speechbubble9_2.move(1305,385)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 795<x and x<830 and y>509 and y<532:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("    KUMHO")
                    self.main.speechbubble9.move(780,415)
                    self.main.speechbubble9_2.move(785,410)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            elif 830<x and x<871 and y>532 and y<573:
                if self.main.speechbubble9.isVisible() == False:
                    self.main.speechbubble9_2.setText("     EECS ")
                    self.main.speechbubble9.move(800,425)
                    self.main.speechbubble9_2.move(805,420)
                    self.main.speechbubble9.show()
                    self.main.speechbubble9_2.show()
            else:
                if self.main.speechbubble9.isVisible() == True:
                    self.main.speechbubble9.hide()
                    self.main.speechbubble9_2.hide()

     def dayinform(self):
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        dayinform = year + "-" + month + "-" + day
        return dayinform

     def get_plot(self):
         unit = " kW"
         for key in self.buildings:
             if self.buildings[key] == True:
                 self.mecha.title.setText(self.building_names[key])
                 daily_maxvalue = int(np.max(self.plotdata[key][0]))
                 daily_minvalue = int(np.min(self.plotdata[key][0]))
                 daily_meanvalue = int(np.mean(self.plotdata[key][0]))
                 weekly_maxvalue = int(np.max(self.plotdata[key][1]))
                 weekly_minvalue = int(np.min(self.plotdata[key][1]))
                 weekly_meanvalue = int(np.mean(self.plotdata[key][1]))
                 self.mecha.subbox_title[3].setText(":   "+str(weekly_maxvalue) + unit+"\n"+":   "+str(weekly_meanvalue)+unit+"\n"+":   "+str(weekly_minvalue)+unit)
                 self.mecha.subbox_title[4].setText(":   " + str(daily_maxvalue) + unit + "\n" + ":   " + str(daily_meanvalue) + unit + "\n" + ":   " + str(daily_minvalue) + unit)
                 self.mecha.subbox_title[5].setText(self.temperature+"°C")
                 #self.mecha.pw.setXRange(self.timestamp1-86400*6+3600*9, self.timestamp2+3600*10)
                 #self.mecha.pw.setXRange(timedata - 10, timedata + 1, padding=0)  # 마우스 클릭에 따라 실시간이랑 전체보기.
                 self.mecha.weekplot.setData(self.plotdata['x2'], self.plotdata[key][1])
                 #self.mecha.pdi2.setData(self.plotdata['x2'], self.plotdata[key][1])

                 #self.mecha.pa.enableAutoRange()
                 self.mecha.pb.setXRange(self.timestamp1, self.timestamp2)
                 #self.mecha.pdib.setData(self.plotdata['x'], self.plotdata[key][0])
                 self.mecha.dailyplot.setData(self.plotdata['x'], self.plotdata[key][0])
                 extra = [x+3600*9 for x in self.plotdata['x']]
                 self.mecha.dailyplot2.setData(extra, self.plotdata[key][0])

     def update(self):
        self.get_data()
        self.get_plot()



class Main_Widget(object):
    def setup(self, mainwindow):
        mainwindow.setStyleSheet("background-color: white")
        mainwindow.setObjectName("Fm")
        mainwindow.setWindowTitle("EMS (Energy monitoring system)")
        mainwindow.setWindowIcon(QtGui.QIcon("icon.png"))

        self.background = QtGui.QPixmap("images/campus.png")
        self.logo = QtGui.QPixmap("images/logo.png")
        self.building = QtGui.QPixmap("images/speech.png")
        self.back1 = QtGui.QIcon('images/back1.png')
        self.back2 = QtGui.QIcon('images/exit1.png')

        pixmap4_re = self.building.scaled(100, 100)

        myFont = QtGui.QFont()
        myFont.setBold(True)

        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.image3 = QtWidgets.QLabel(self.centralwidget)
        self.image3.setPixmap(self.background)
        self.image3.move(40,110)

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.resize(1920,200)
        self.image.setStyleSheet("background: rgb(128,128,128);color: white;") #rgb   ; x

        a = " "*10
        self.image.setText(a+"Energy Monitoring System by ISP Lab")
        new_font = QtGui.QFont("Arial", 60, QtGui.QFont.Bold)
        self.image.setFont(new_font)
        self.image.move(0,0)

        self.image2 = QtWidgets.QLabel(self.centralwidget)
        self.image2.resize(220,200)
        self.image2.setPixmap(self.logo)
        self.image2.move(-20,0)

        self.subboxicon = QtGui.QIcon('images/sub1.png')
        self.subboxicon2 = QtGui.QIcon('images/sub2.png')
        self.subboxicon3 = QtGui.QIcon('images/sub3.png')

        self.subbox = []
        self.subbox_title = []
        new_fon = QtGui.QFont("Arial", 20)
        new_fon2 = QtGui.QFont("Arial", 20,QtGui.QFont.Bold)

        self.subboxx = QtWidgets.QPushButton(self.centralwidget)
        self.subboxx.setIcon(self.subboxicon3)
        self.subboxx.setIconSize(QtCore.QSize(1300, 350))
        self.subboxx.setStyleSheet("background:none;border:none")
        self.subboxx.move(-5,80)

        for i in range(6):
            if i<3:
                 subbox = QtWidgets.QPushButton(self.centralwidget)
                 subbox_title = QtWidgets.QLabel(self.centralwidget)
                 subbox.setIcon(self.subboxicon2)
                 subbox.setIconSize(QtCore.QSize(130, 100))
                 subbox_title.setFont(new_fon)
                 subbox_title.setText("Total Power Consumption ")
                 subbox.setStyleSheet("background:none;border:none")
                 self.subbox.append(subbox)
            else :
                 subbox_title = QtWidgets.QLabel(self.centralwidget)
                 subbox_title.setFont(new_fon2)
                 subbox_title.resize(QtCore.QSize(120, 120))
                 subbox_title.setText("Null")

            subbox_title.setStyleSheet("background:none;border:none")
            self.subbox_title.append(subbox_title)


        self.subbox[0].move(125, 220)
        self.subbox_title[0].move(45, 205)
        self.subbox_title[3].move(140, 210)

        self.subbox[1].move(575, 220)
        self.subbox_title[1].move(540, 205)
        self.subbox_title[1].setText("Graduate School")
        self.subbox_title[4].move(590, 210)

        self.subbox[2].move(1015,220)
        self.subbox_title[2].move(940, 205)
        self.subbox_title[2].setText("Undergraduate School")
        self.subbox_title[5].move(1030, 210)

        self.button_list = []
        for i in range(43):
            button = QtWidgets.QPushButton("", self.centralwidget)
            button.setStyleSheet("background:none;border: none")
            self.button_list.append(button)
        # #self.btn1.setStyleSheet("background:(217,217,217);border: none")

        self.button_list[9].resize(100,50)
        self.button_list[9].move(630, 627)

        self.button_list[18].resize(120, 50)
        self.button_list[18].move(360, 697)

        self.button_list[19].resize(113, 60)
        self.button_list[19].move(274, 565)

        self.button_list[20].resize(47, 38)
        self.button_list[20].move(412, 603)

        self.button_list[26].resize(170,110)
        self.button_list[26].move(195, 780)

        self.button_list[24].resize(50,40)
        self.button_list[24].move(645, 507)

        self.button_list[32].resize(76,41)
        self.button_list[32].move(754, 670)

        self.button_list[37].resize(85,48)
        self.button_list[37].move(1046, 578)

        self.button_list[38].resize(115,59)
        self.button_list[38].move(1368, 573)

        self.button_list[11].resize(122,66)
        self.button_list[11].move(1151, 761)

        self.button_list[36].resize(119,53)
        self.button_list[36].move(1148, 579)

        self.button_list[6].resize(35,52)
        self.button_list[6].move(928, 721)

        self.button_list[8].resize(59,48)
        self.button_list[8].move(853, 689)

        self.button_list[7].resize(76,68)
        self.button_list[7].move(799, 730)

        self.button_list[14].resize(46,40)
        self.button_list[14].move(894, 802)

        self.button_list[10].resize(100,65)
        self.button_list[10].move(987, 614)

        self.button_list[33].resize(115,60)
        self.button_list[33].move(1195, 530)

        self.button_list[34].resize(100,30)
        self.button_list[34].move(1247, 501)

        self.button_list[35].resize(80,52)
        self.button_list[35].move(1311, 472)

        self.button_list[13].resize(23,23)
        self.button_list[13].move(795, 509)

        self.button_list[2].resize(41,41)
        self.button_list[2].move(830, 532)

        self.btnend = QtWidgets.QPushButton(self.centralwidget)
        self.btnend.resize(250,250)
        self.btnend.setStyleSheet("background:white;border:none")
        self.btnend.setIcon(self.back1)
        self.btnend.setIconSize(QtCore.QSize(200,200))
        self.btnend.move(1600,250)

        self.btnend_sub = QtWidgets.QPushButton(self.centralwidget)
        #new_font2 = QFont("Times", 30, QFont.Bold)
        #self.btnend.setFont(new_font2)
        self.btnend_sub.resize(150,150)
        self.btnend_sub.setStyleSheet("background:none;border:none")
        self.btnend_sub.setIcon(self.back2)
        self.btnend_sub.setIconSize(QtCore.QSize(150,150))
        self.btnend_sub.move(1650,300)

        self.speechbubble9 = QtWidgets.QLabel("asdas",self.centralwidget)
        self.speechbubble9.resize(100, 100)
        self.speechbubble9.setPixmap(pixmap4_re)
        self.speechbubble9.setStyleSheet("background:none")

        self.speechbubble9_2 = QtWidgets.QLabel(self.centralwidget)
        self.speechbubble9_2.resize(100, 100)
        self.speechbubble9_2.setFont(myFont)
        self.speechbubble9_2.setStyleSheet("background:none")

        self.speechbubble9.hide()
        self.speechbubble9_2.hide()

        mainwindow.setCentralWidget(self.centralwidget)

class Mecha_Widget(object):
    def setup(self, mainwindow):
        mainwindow.setStyleSheet("background-color: white")
        #mainwindow.setGeometry(QtCore.QRect(250, 250, 1920, 1080))
        mainwindow.setObjectName("Fm")
        mainwindow.setWindowTitle("ISP EMS (Energy monitoring system)")
        mainwindow.setWindowIcon(QtGui.QIcon("icon.png"))

        self.logo = QtGui.QPixmap("images/logo.png")
        self.back1 = QtGui.QIcon('images/back1.png')
        self.back2 = QtGui.QIcon('images/exit2.png')
        self.subboxicon = QtGui.QIcon('images/sub1.png')
        self.subboxicon2 = QtGui.QIcon('images/sub2.png')
        self.weather = QtGui.QIcon('images/weather.png')

        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)

        self.subbox = []
        self.subbox_title = []
        new_fon = QtGui.QFont("Arial", 20)
        new_fon2 = QtGui.QFont("Arial", 18,QtGui.QFont.Bold)
        new_fon3 = QtGui.QFont("Arial", 17)
        new_fon4 = QtGui.QFont("Arial", 22,QtGui.QFont.Bold)
        #Making the boxes and titles for displaying the power consumption data on the top of the screen
        for i in range(9):
            if i<6:
                subbox = QtWidgets.QPushButton(self.centralwidget)
            subbox_title = QtWidgets.QLabel(self.centralwidget)
            if i<3 :
                 subbox.setIcon(self.subboxicon)
                 subbox.setIconSize(QtCore.QSize(600, 200))
                 subbox_title.setFont(new_fon)
                 subbox_title.setText("Weekly Power Consumption")
            else :
                 subbox.setIcon(self.subboxicon2)
                 subbox.setIconSize(QtCore.QSize(500, 100))
                 subbox_title.setFont(new_fon2)
                 subbox_title.setText("Null")

            subbox.setStyleSheet("background:none;border:none")
            subbox_title.setStyleSheet("background:none;border:none")
            if i < 6:
                self.subbox.append(subbox)
            self.subbox_title.append(subbox_title)

        #Box1 and Title1
        self.subbox[0].move(-25,215)
        self.subbox[3].move(110, 290)
        self.subbox_title[0].move(100, 230)
        self.subbox_title[3].move(340, 295)
        self.subbox_title[6].move(275, 300)
        self.subbox_title[6].setFont(new_fon3)
        self.subbox_title[6].setText(" Max\nMean \n Min")

        # Box2 and Title2
        self.subbox[1].move(410,215)
        self.subbox[4].move(545, 290)
        self.subbox_title[1].move(555, 230)
        self.subbox_title[1].setText("Daily Power Consumption")
        self.subbox_title[4].move(780, 295)
        self.subbox_title[7].move(715, 300)
        self.subbox_title[7].setFont(new_fon3)
        self.subbox_title[7].setText(" Max\nMean \n Min")

        # Box3 and Title3
        self.subbox[2].move(845,215)
        self.subbox[5].move(980,290)
        self.subbox_title[2].move(1030, 230)
        self.subbox_title[2].setText("Today's weather")
        self.subbox_title[5].setFont(new_fon4)
        self.subbox_title[5].move(1170, 320)
        weathimage = QtWidgets.QPushButton(self.centralwidget)
        weathimage.move(730, 235)
        weathimage.setIcon(self.weather)
        weathimage.setIconSize(QtCore.QSize(600, 200))
        weathimage.setStyleSheet("background:none;border:none")

        self.box = QtWidgets.QPushButton(self.widget2)
        self.box.move(55, 425)
        self.box.resize(1310, 610)
        self.box.setStyleSheet("background:none;border:  5px solid rgb(145,97,97)")

        self.box2 = QtWidgets.QPushButton(self.widget2)
        self.box2.move(60, 430)
        self.box2.resize(1300, 600)
        self.box2.setStyleSheet("background:none;border: 5px solid gray")

        self.title = QtWidgets.QLabel(self.widget2)
        self.title.setText("The Building of Dep. ME")
        new_font1 = QtGui.QFont("Arial", 30)
        self.title.setFont(new_font1)
        self.title.move(480,455)

        self.pw = pg.PlotWidget(
            title="",
            labels={'left': 'Power consumption [kW]'},
            axisItems={'bottom': TimeAxisItem2(orientation='bottom')}
        )

        self.pb = pg.PlotWidget(
            title="",
            labels={'left': 'Power consumption [kW]'},
            axisItems={'bottom': TimeAxisItem(orientation='bottom')}

        )

        #n = pg.LegendItem(size = (100, 100), offset = (30, 30))
        #self.pb.addLegend(size = (100, 50))

        self.error = QtWidgets.QLabel("MAPE %: \n  ")
        self.hbox = QtWidgets.QGridLayout(self.widget3)

        self.hbox.addWidget(self.pb, 0, 0,1,3)  # 만든 box에 추가
        #self.hbox.addWidget(self.pa, 0, 1)  # 만든 box에 추가
        self.hbox.addWidget(self.pw, 1, 0, 1, 3)

        #self.widget3.setGeometry(QtCore.QRect(110, 500, 1200, 500))
        self.widget3.setGeometry(QtCore.QRect(110, 500, 1200, 500))
        self.hbox.setGeometry(QtCore.QRect(250, 250, 1000, 400))

        #real = pg.mkPen(color=(50, 50, 50),width = 3, style=QtCore.Qt.DotLine)
        real = pg.mkPen(color=(25, 37, 53), width=3)
        real2 = pg.mkPen(color=(242, 184, 0),width = 3)

        self.weekplot = self.pw.plot(pen=real, name='')
        self.dailyplot2 = self.pw.plot(pen=real2,name='')  # PlotDataItem obj 반환.
        #self.pdi2 = self.pw.plot(pen=real2, name='Predictive model')  # PlotDataItem obj 반환.
        #self.pdib = self.pb.plot(pen=real, name='Actual load')
        self.dailyplot = self.pb.plot(pen=real2, name='')

        mainwindow.get_plot()
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.resize(1920,200)
        self.image.setStyleSheet("background: rgb(128,128,128);color: white;") #rgb   ; x

        a = " "*10
        self.image.setText(a+"Energy Monitoring System by ISP Lab")
        new_font = QtGui.QFont("Arial", 60, QtGui.QFont.Bold)
        self.image.setFont(new_font)
        self.image.move(0,0)
        self.mecha = False

        self.image2 = QtWidgets.QLabel(self.centralwidget)
        self.image2.resize(220,200)
        self.image2.setPixmap(self.logo)
        self.image2.move(-20,0)

        self.btn_sub = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sub.resize(250,150)
        self.btn_sub.setStyleSheet("background:white;border:none")
        self.btn_sub.setIcon(self.back1)
        self.btn_sub.setIconSize(QtCore.QSize(200,150))
        self.btn_sub.move(1640,240)

        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.resize(150, 150)
        self.btn.setStyleSheet("background:none;border:none")
        self.btn.setIcon(self.back2)
        self.btn.setIconSize(QtCore.QSize(150, 130))
        self.btn.move(1690, 240)
        mainwindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":

    print("Starting........***")
    app = QtWidgets.QApplication(sys.argv)
    Main = Main_Window()

    mytimer2 = QtCore.QTimer()
    mytimer2.start(10)
    mytimer2.timeout.connect(Main.mousecheck)

    mytimer = QtCore.QTimer()
    mytimer.start(240000)  #
    mytimer.timeout.connect(Main.update)

    sys.exit(app.exec_())
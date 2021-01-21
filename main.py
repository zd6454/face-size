# coding: utf-8
import sys
import datetime
import pymysql
import sqlheper
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QHeaderView, QTableWidgetItem
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtCore import Qt, QMetaMethod
from PyQt5.QtGui import QPixmap
from openpyxl import Workbook
from z_ui import Ui_zwin
from cx_ui import Ui_cx
from face_shibie import Face


obj = sqlheper.sqlHelper()

class MainWindow(QWidget):
    face = Face()

    def __init__(self):
        super().__init__()
        self.start_ui()

    def start_ui(self):
        self.zui = Ui_zwin()
        self.zui.setupUi(self)
        self.zui.camera_label.setScaledContents(True)

        # 初始化信息
        self.zui.label_xuehao.setText("工号：")
        self.zui.label_mingzi.setText("姓名：")
        self.zui.label_time.setText("签到时间：")

        # 查询按钮
        self.zui.cxbtn.clicked.connect(self.cx_ui)
        # 注册按钮
        self.zui.zcbtn.clicked.connect(self.zq_zc)
        # 签到按钮
        self.zui.qdbtn.clicked.connect(self.zq_qd)
        # 删除按钮
        self.zui.del_btn.clicked.connect(self.del_yg)
        # 导出按钮
        self.zui.out_btn.clicked.connect(self.out_ex)

        # 摄像头控制
        camera = QCamera(self)  # 创建摄像头
        cameraviewfinder = QCameraViewfinder(self.zui.camera_label)  # 创建显示窗口
        cameraviewfinder.resize(752, 420)
        self.cameraImageCapture = QCameraImageCapture(camera)  # 绑定获取的摄像头
        self.cameraImageCapture.setCaptureDestination(QCameraImageCapture.CaptureToFile)  # 获取数据类型
        camera.setCaptureMode(QCamera.CaptureStillImage)
        camera.setViewfinder(cameraviewfinder)  # 绑定窗口
        camera.start()  # 开启摄像头

    def out_ex(self):
        """
        导出考勤记录
        :return:
        """
        wk = Workbook()
        wb = wk.active
        wb.append(['姓名', '工号', '打卡时间', '状态'])
        result = obj.get_list("select name, no, ctime, st from qds",[])
        for i in result:
            wb.append(i)
        wk.save(r'kaoqing.xlsx')
        return QMessageBox.information(self, "提示", '导出成功...', QMessageBox.Yes, QMessageBox.Yes)

    def del_yg(self):
        """
        删除员工
        :return:
        """
        gh = self.zui.gonghao.text()
        if not gh:
            return QMessageBox.information(self, "提示", '请填写工号...', QMessageBox.Yes, QMessageBox.Yes)
        if obj.get_list('select no from user where no=%s',[gh,]):
            obj.modify('delete from user where no=%s', [gh, ])
            return QMessageBox.information(self, "提示", '删除成功...', QMessageBox.Yes, QMessageBox.Yes)
        else:
            return QMessageBox.information(self, "提示", '删除失败...', QMessageBox.Yes, QMessageBox.Yes)

    def zc(self, xx, image):
        """
        注册
        :return:
        """
        self.cameraImageCapture.disconnect()
        pximap = QPixmap.fromImage(image)  # 获取摄像头图片
        pximap.save('image.jpg')  # 保存图片

        name = self.zui.mingzi.text()
        no = self.zui.xuehao.text()

        if not name or not no:
            QMessageBox.information(self, "提示", '请填写工号跟姓名...', QMessageBox.Yes, QMessageBox.Yes)
            return self.zui.zcbtn.setDisabled(False)

        path = 'image.jpg'
        print(103)
        face_token = self.face.C_addFace(name, no, path)
        print(105, face_token)

        if face_token:
            try:
                obj.modify("insert into user(name,no,face_token) values (%s,%s,%s)" ,[name,no,face_token,])
            except Exception as e:
                obj.rollback()
                self.zui.zcbtn.setDisabled(False)
                return QMessageBox.information(self, "提示", '用户已存在...', QMessageBox.Yes, QMessageBox.Yes)
            QMessageBox.information(self, "提示", '注册成功...', QMessageBox.Yes, QMessageBox.Yes)
            obj.modify("insert into qds_month(name,no,st_no) values (%s,%s,0)" ,[name,no,])
        else:
            QMessageBox.information(self, "提示", '注册失败...', QMessageBox.Yes, QMessageBox.Yes)
        self.zui.zcbtn.setDisabled(False)

    def qd(self, xx, image):
        """
        签到
        :return:
        """
        self.cameraImageCapture.disconnect()
        pximap = QPixmap.fromImage(image)  # 获取摄像头图片
        pximap.save('image.jpg')  # 保存图片

        t = self.face.C_searchFace('image.jpg')
        if t:
            no = t[1]
            name = t[0]
            face_token = t[2]

            res = obj.get_list("select no from user where face_token=%s" ,[face_token,])
            if len(res) <= 0:
                QMessageBox.information(self, "提示", '数据库无此人信息...', QMessageBox.Yes, QMessageBox.Yes)
                return self.zui.qdbtn.setDisabled(False)
            ctime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.zui.label_xuehao.setText("工号：" + str(no))
            self.zui.label_mingzi.setText("姓名：" + str(name))
            self.zui.label_time.setText("签到时间：" + ctime)
            hour = datetime.datetime.today().hour
            st = '异常'
            if hour < 8 or hour > 17:
                st = '正常'
            # 执行sql语句
            obj.modify("insert into qds(name,no,ctime,st) values (%s,%s,%s,%s)",[name,no,ctime,st,])
            QMessageBox.information(self, "提示", '签到成功...', QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", '查无此人...', QMessageBox.Yes, QMessageBox.Yes)

        self.zui.qdbtn.setDisabled(False)

    def zq_zc(self):
        """注册抓取"""
        self.zui.zcbtn.setDisabled(True)
        self.cameraImageCapture.imageCaptured.connect(self.zc)  # 截取图片后链接显示方法
        self.cameraImageCapture.capture()  # 抓取方法

    def zq_qd(self):
        """签到抓取"""
        self.zui.qdbtn.setDisabled(True)
        self.cameraImageCapture.imageCaptured.connect(self.qd)  # 截取图片后链接显示方法
        self.cameraImageCapture.capture()  # 抓取方法

    def cx_ui(self):
        # 查询窗口
        self.cxui = Ui_cx()
        self.cxw = QDialog()
        self.cxui.setupUi(self.cxw)

        # 设置表格
        self.cxui.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.cxui.tableWidget.setColumnWidth(0, 120)
        self.cxui.tableWidget.setColumnWidth(1, 120)
        # self.cxui.tableWidget.setColumnWidth(2, 100)
        self.cxui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cxui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cxui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.cxui.tableWidget.setRowCount(0)  # 设置行=0
        self.cxui.tableWidget.clearContents()  # 清除内容

        # 查询按钮
        self.cxui.btn_cx.disconnect()
        self.cxui.btn_cx.clicked.connect(self.cx)
        self.cxw.exec_()

    def cx(self):
        """查询数据"""
        self.cxui.tableWidget.setRowCount(0)  # 设置行=0
        self.cxui.tableWidget.clearContents()  # 清楚内容
        no = self.cxui.xuehao_cx.text()
        name = self.cxui.mingzi_cx.text()
        print(no, name, 'xxxxxx')
        if name == 'admin':
            data = obj.get_list("select name, no, ctime, st_no from qds_month order by st_no desc",[])
            if len(data) <= 0:
                return QMessageBox.information(self, "提示", '查询无记录...', QMessageBox.Yes, QMessageBox.Yes)
            for k, i in enumerate(data):
                name = i[0]
                no = i[1]
                ctime = i[2]
                st = i[3]
                self.cxui.tableWidget.insertRow(k)
                self.cxui.tableWidget.setItem(k, 0, QTableWidgetItem(str(no)))
                self.cxui.tableWidget.item(k, 0).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 1, QTableWidgetItem(str(name)))
                self.cxui.tableWidget.item(k, 1).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 2, QTableWidgetItem(str(ctime)))
                self.cxui.tableWidget.item(k, 2).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 3, QTableWidgetItem(str(st)))
                self.cxui.tableWidget.item(k, 3).setTextAlignment(Qt.AlignCenter)
                print(i)
            return;
        if not no and not name:
            time = datetime.datetime.now()
            sql = "select name, no, ctime, st from qds where st = '异常' " + 'order by ctime desc limit 7'
            print(sql)
            data = obj.get_list(sql, [])
            print(data)
            if len(data) <= 0:
                return QMessageBox.information(self, "提示", '查询无记录...', QMessageBox.Yes, QMessageBox.Yes)
            for k, i in enumerate(data):
                name = i[0]
                no = i[1]
                ctime = i[2]
                st = i[3]
                print(type(ctime))
                now = str(ctime)
                cur = str(time)
                now = now[:10]
                cur = cur[:10]
                if now != cur:
                    continue
                self.cxui.tableWidget.insertRow(k)
                self.cxui.tableWidget.setItem(k, 0, QTableWidgetItem(str(no)))
                self.cxui.tableWidget.item(k, 0).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 1, QTableWidgetItem(str(name)))
                self.cxui.tableWidget.item(k, 1).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 2, QTableWidgetItem(str(ctime)))
                self.cxui.tableWidget.item(k, 2).setTextAlignment(Qt.AlignCenter)
                self.cxui.tableWidget.setItem(k, 3, QTableWidgetItem(str(st)))
                self.cxui.tableWidget.item(k, 3).setTextAlignment(Qt.AlignCenter)
                print(i)
            return;
            #return QMessageBox.information(self, "提示", '请出入查询条件...', QMessageBox.Yes, QMessageBox.Yes)
        s = ''
        if no:
            s += "and no like '%%{}%%'".format(no, )
        if name:
            s += "and name like '%%{}%%'".format(name, )
        sql = "select name, no, ctime,st from qds where 1=1" + ' ' + s + 'order by ctime desc limit 7'
        print(sql)
        data = obj.get_list(sql,[])
        if len(data) <= 0:
            return QMessageBox.information(self, "提示", '查询无记录...', QMessageBox.Yes, QMessageBox.Yes)
        for k, i in enumerate(data):
            name = i[0]
            no = i[1]
            ctime = i[2]
            st = i[3]
            self.cxui.tableWidget.insertRow(k)
            self.cxui.tableWidget.setItem(k, 0, QTableWidgetItem(str(no)))
            self.cxui.tableWidget.item(k, 0).setTextAlignment(Qt.AlignCenter)
            self.cxui.tableWidget.setItem(k, 1, QTableWidgetItem(str(name)))
            self.cxui.tableWidget.item(k, 1).setTextAlignment(Qt.AlignCenter)
            self.cxui.tableWidget.setItem(k, 2, QTableWidgetItem(str(ctime)))
            self.cxui.tableWidget.item(k, 2).setTextAlignment(Qt.AlignCenter)
            self.cxui.tableWidget.setItem(k, 3, QTableWidgetItem(str(st)))
            self.cxui.tableWidget.item(k, 3).setTextAlignment(Qt.AlignCenter)
            print(i)


if __name__ == "__main__":
    time = datetime.datetime.now()
    now = str(time)
    # 删除所有之前的每日记录
    #cu.execute("delete from qds")
    #con.commit()
    print(now)
    now = now[8:10]
    print(now)
    # 如果是每个月的第一天将月记录表清空
    if now == '01':
        for i in range(1, 1000):
            obj.modify("update qds_month set st_no = 0 where id = %d", [i,])
            #cu.execute("insert into qds(name,no,ctime,st) values ('%s', '%s', '%s', '%s')" % (name, no, ctime, st))
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
obj.close()
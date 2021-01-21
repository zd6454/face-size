# coding: utf-8
import shelve
import requests
from json import JSONDecoder

FACESET_FILEPATH = "faceset.txt"
# FACELIST_FILEPATH = "facelist.txt"
API_KEY = "6BK6yT-fzRSCwVSIPXF-RVvBDVrfYgG8"
API_SECRET = "P6BpIkxVyPqxQWK3n32ElAKUwLbcHnTi"

import os


def save(l):
    with shelve.open(r'data', writeback=True) as f:
        if f.get('user'):
            f['user'].append(l)
        else:
            f.update({'user': [l]})

def read():
    with shelve.open(r'data') as f:
        return f.get('user', [])

class Face(object):
    def __init__(self):
        # self.list = []
        self.checkFacesetFile()
        # self.checklistFile()

    def menu(self):
        print("--------人脸识别项目---------")
        print("1.人脸采集")
        print("2.人脸识别")
        print("3.退出")
        print("---------------------------")
        flag = int(input("请选择:"))
        return flag

    def checkFacesetFile(self):
        if os.path.exists(FACESET_FILEPATH):
            file = open(FACESET_FILEPATH, "r")
            self.faceset_token = file.readline()
            print("faceset_token:%s" % self.faceset_token)
            file.close()
        else:
            file = open(FACESET_FILEPATH, "w")
            self.faceset_token = self.createFace()
            print("faceset_token:%s" % self.faceset_token)
            file.write(self.faceset_token)
            file.close()
            # 通过face++平台创建一个faceset_token
            # self.faceset = self.createFace()
            # 创建文件，保存faceset

    def createFace(self):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
        data = {"api_key": API_KEY, "api_secret": API_SECRET}
        response = requests.post(http_url, data=data)
        req_con = response.content.decode('utf-8')
        #  Json解析-->字典
        req_dict = JSONDecoder().decode(req_con)
        print(req_dict)  # key：value
        return req_dict["faceset_token"]

    # def checklistFile(self):
    #     if os.path.exists(FACELIST_FILEPATH):
    #         file = open(FACELIST_FILEPATH, "r")
    #         tlist = file.readlines()
    #         print(tlist)
    #         for node in tlist:
    #             node = node[0:-1:1]
    #             t = node.split(" ")
    #             self.list.append(t)
    #         file.close()

    def detectFace(self, imgFile):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        data = {"api_key": API_KEY, "api_secret": API_SECRET}
        files = {"image_file": open(imgFile, "rb")}
        # 2  发送http请求post     网址       表单数据    文件-图像
        response = requests.post(http_url, data=data, files=files)

        # 3 response 返回处理
        #                  内容     字符编码
        req_con = response.content.decode('utf-8')
        #  Json解析-->字典
        req_dict = JSONDecoder().decode(req_con)
        print(req_dict)  # key：value
        # 返回这张imgFile图片的face_token
        if len(req_dict['faces'])>0:
            return req_dict['faces'][0]['face_token']
        else:
            return ''

    def addFace(self, face_token):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
        data = {"api_key": API_KEY, "api_secret": API_SECRET, "faceset_token": self.faceset_token,
                "face_tokens": face_token}
        # 2  发送http请求post     网址       表单数据    文件-图像
        response = requests.post(http_url, data=data)
        4
        # 3 response 返回处理
        #                  内容     字符编码
        req_con = response.content.decode('utf-8')
        #  Json解析-->字典
        req_dict = JSONDecoder().decode(req_con)
        print('='*50)
        print(req_dict)  # key：value
        if req_dict["face_added"] == 1:
            print("ok")
            return True
        else:
            return False

        # 传入face_token增加到你的faceset中
        pass

    def searchFace(self, imgFile):
        http_url = "https://api-cn.faceplusplus.com/facepp/v3/search"
        data = {"api_key": API_KEY, "api_secret": API_SECRET, "faceset_token": self.faceset_token}
        files = {"image_file": open(imgFile, "rb")}
        # 2  发送http请求post     网址       表单数据    文件-图像
        response = requests.post(http_url, data=data, files=files)

        # 3 response 返回处理
        #                  内容     字符编码
        req_con = response.content.decode('utf-8')
        #  Json解析-->字典
        req_dict = JSONDecoder().decode(req_con)
        print(req_dict)  # key：value
        try:
            face_token = req_dict["results"][0]["face_token"]
            confidence = req_dict["results"][0]["confidence"]
        except Exception as e:
            print("失败")
            return False, ""
        y = req_dict["thresholds"]["1e-5"]
        if confidence > y:
            print("成功")
            return True, face_token
        else:
            print("失败")
            return False, ""

    def searchName(self, face_token):
        for node in read():
            if (node[2] == face_token):
                print(node)
                return node
        return False
        # 根据face_token返回名字和学号

    # def saveListFile(self):
    #     file = open(FACELIST_FILEPATH, "w")
    #     for node in self.list:
    #         file.write(node[0] + " " + node[1] + " " + node[2] + "\n")
    #     file.close()

    def C_searchFace(self, path):
        ret, face_token = self.searchFace(path)
        if ret:
            print("查找成功", face_token)
            node = self.searchName(face_token)
            print('node: ', node)
            return node
        else:
            print("查无此人")
            return False

    def C_addFace(self, name, no, path):
        face_token = self.detectFace(path)
        if self.addFace(face_token):
            print("增加成功")
            save([name, no, face_token])
            # self.list.append([name, no, face_token])
            # self.saveListFile()
            return face_token
        else:
            print("增加失败")
            return False


def main():
    face = Face()

    while True:
        flag = face.menu()
        if flag == 1:
            name = input("输入姓名:")
            no = input("输入学号:")
            path = input("输入照片路径:")
            face.C_addFace(name, no, path)

        elif flag == 2:
            path = input("输入照片路径:")
            face.C_searchFace(path)
        elif flag == 3:
            break


if __name__ == '__main__':
    main()

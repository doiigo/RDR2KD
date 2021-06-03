# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget , QFileDialog 
from RDR2cg import Ui_MainWindow  
import threading
import shutil
import subprocess
class MainForm( QMainWindow , Ui_MainWindow):  
	def __init__(self):  
		super(MainForm,self).__init__()  
		self.setupUi(self)
		self.pushButtonset.clicked.connect(self.btnstate)
		self.pushButtonsea.clicked.connect(self.ButtonClicked) #按钮单击信号绑定到槽
		self.pushButtonsub.clicked.connect(self.keylogin)
		self.actionsingle.triggered.connect(self.copy_file)
		self.actionmulti.triggered.connect(self.del_file)
		
	def copy_file(self):
		with open(r'lj.txt','a+',encoding='utf-8') as copylj:
			copylj.seek(0,0)
			copy_lj = copylj.read()
			#print(copy_lj)
			dz = str(copy_lj) + 'x64\data'
			#print(dz)
			dz2 = str(copy_lj) + 'x64'
			#print(dz2)			
			shutil.copy('startup.meta',  dz)
			shutil.copy('boot_launcher_flow.ymt',dz2)
			
			

	def del_file(self):
		#print("heheh")
		with open(r'lj.txt','a+',encoding='utf-8') as copylj:
			copylj.seek(0,0)
			copy_lj = copylj.read()
			ddz = str(copy_lj) + 'x64\data\startup.meta'
			ddz2 = str(copy_lj) + r'x64\boot_launcher_flow.ymt'
			os.remove(ddz)
			os.remove(ddz2)
                        
	
		
	def keylogin(self):
		keynum = self.lineEdit.text()
		print(keynum)
		new_str = '</CDataFileMgr__ContentsOfDataFileXml>'+str(keynum)
		file_path = 'startup.meta'
		#print(file_path)
		line_num = 53
		with open(file_path,"r") as f:
			res = f.readlines()
		res[line_num-1] = (new_str+"\n")
		with open(file_path,"w")as f:
			f.write("".join(res))
			f.close()

	
		
		
	def openMsg(self):  
		file,ok= QFileDialog.getOpenFileName(self,"打开","C:/","All Files (*);;Text Files (*.txt)") 
		# 在状态栏显示文件地址  		
		self.statusbar.showMessage(file)

	def btnstate(self):#手动选择文件夹
		if self.pushButtonset.isChecked():
			print("button released" ) 
		else:
			directory1 = QFileDialog.getExistingDirectory(self)
			#print(directory1)
			file = open("lj.txt","a")
			with open(r'lj.txt','a+',encoding='utf-8') as test:
				test.truncate(0)
				test.write(directory1)
				test.close()
	def ButtonClicked(self):
        # 创建新线程，将自定义信号sinOut连接到slotAdd()槽函数
		keyword = 'PlayRDR2.exe'#self.key.text()
		#self.result.clear()
		self.thread=fileSearchThread(keyword)
		#self.thread.sinOut.connect(self.slotAdd)
		self.thread.start()
	#def slotAdd(self,filename):
		#print("sbsbsb")
		#self.result.addItem(str(filename))			

        
                
	
##################################之下是搜索的类，线程和具体搜索
class fileSearchThread(QThread):
    sinOut = pyqtSignal(str)
    # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self,key):
        super().__init__()
        self.key = key
        
    def run(self):
        threads=[]
        path = [r"c:\\", r"d:\\", r"e:\\", r"f:\\"]
        #通过多线程对windows下的多个盘符进行文件的遍历查找
        
        for each in path:
            t = threading.Thread(target=self.search, args=(self.key,each,))
            threads.append(t)
            t.start()

        for i in range(len(threads)): #将主线程阻塞
            threads[i].join()
        print("搜索结束")

    def search(self,keyword, path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.__contains__(keyword):
                    alu = os.path.join(dirpath, filename)
                    #print(os.path.join(dirpath, filename))
                    exejc = alu
                    exejc = exejc[:-12]
                    print(exejc)
                    file = open("lj.txt","a")
                    with open(r'lj.txt','a+',encoding='utf-8') as test:
                        test.truncate(0)
                        test.write(exejc)
                        test.close()
                    #self.sinOut.emit(os.path.join(dirpath, filename))
            #for folder in dirnames:
             #   if folder.__contains__(keyword):
              #      print(os.path.join(dirpath,folder))
               #     self.sinOut.emit(os.path.join(dirpath,folder))
                    
	

	




                       
		     



            
if __name__=="__main__":  
	app = QApplication(sys.argv)  
	win = MainForm()  
	win.show()  
	sys.exit(app.exec_())


    
    




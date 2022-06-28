# 네이버 영화 검색용 UI 실행
import json
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json #검색결과를 json type로 받음
import urllib.request #URL openAPI 검색을 위한 라이브러리 
from urllib.parse import quote 
import webbrowser #웹브라우저 열기 위한 패키지

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./windows/ui/navermovie.ui',self)
        self.setWindowIcon(QIcon('naver_icon.png'))
        
        #signal connection
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        self.show()
    
    def tblResultSelected(self):
        selected = self.tblResult.currentRow() #현재 선택된 열의 index
        url = self.tblResult.item(selected, 2).text()
        webbrowser.open(url)
    
    def btnSearchClicked(self):
        jsonResult = []
        totalResult = []

        keyword = 'news' #검색 키워드
        search_word = self.txtSearch.text() 
        
        #한 번에 검색할 개수를 미리 지정해둬야 한다. 
        display_count = 50

        jsonResult = self.getNaverSearch(search_word, 1, display_count)
        print(jsonResult)
        
   
        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        self.makeTable(totalResult)
    
    def makeTable(self,result):
        #table widget 설정 
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) #하나씩 선택하도록 한다. 
        self.tblResult.setColumnCount(3) #title, url 함께 보낸다.
        self.tblResult.setRowCount(len(result)) #50개
        self.tblResult.setHorizontalHeaderLabels(['영화 제목', '상영 년도', '영화 링크'])

        #너비 조정
        self.tblResult.setColumnWidth(0,250) 
        self.tblResult.setColumnWidth(1,100)
        self.tblResult.setColumnWidth(2,100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) #read only  #더블클릭 했을 때, 수정되지 않도록 함

        i = 0
        for item in result: #50번 반복
            title = self.strip_tag(item[0]['title']) 
            subtitle = item[0]['subtitle']
            self.tblResult.setItem(i,0, QTableWidgetItem(f'{title} / {subtitle}'))
            self.tblResult.setItem(i,1, QTableWidgetItem(item[0]['pubDate']))
            self.tblResult.setItem(i,2, QTableWidgetItem(item[0]['link']))
            i += 1

    #html tag
    def strip_tag(self, title): # 웹 관련해서 자주 만드는 함수
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')

        return ret
        


    def getPostData(self, post):
        temp = []
        title = post['title']
        link = post['link']
        subtitle = post['subtitle']        
        pubDate = post['pubDate']

        temp.append({'title':title, 'link':link, 'subtitle':subtitle,
                    'pubDate': pubDate})

        return temp 

    #핵심 함수
    def getNaverSearch(self, search, start, display):
        #search url
        url = f'https://openapi.naver.com/v1/search/movie' \
              f'?query={quote(search)}&start={start}&display={display}]'
        req = urllib.request.Request(url)

        #인증 추가
        req.add_header('X-Naver-Client-Id', '') #key
        req.add_header('X-Naver-Client-Secret', '') #id
        
        res = urllib.request.urlopen(req)      #res = response  #request에 대한 response
        if res.getcode() == 200:
            print('URL request success!')

        else : 
            print('URL request failed!')
        
        ret = res.read().decode('utf-8') #return 
        if ret == None :
            return None
        else : 
            return json.loads(ret)
       




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()

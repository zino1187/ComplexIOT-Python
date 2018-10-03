import tkinter
import threading 
import time
from socket import *

class Client(threading.Thread):
    flag=True #전등의 상태를 처리하기 위한 변수
    threadFlag=True
    count=0

    #네트워크 관련
    ip="172.30.1.51"
    port=7777
    serverAddr=(ip, port)
    sock=None

    def __init__(self):#생성자
        threading.Thread.__init__(self) #부모생성자 호출
        self.win=tkinter.Tk() #윈도우 생성
        
        self.txt=tkinter.StringVar(value="on")#제어변수 선언은 반드시  윈도우 생성 이후에 가능하다

        self.win.geometry("300x400") #윈도우 창 크기
        self.bt=tkinter.Button(self.win, text="on", textvariable=self.txt , command=self.send, background="gray", width=20,height=10)

        self.bt.pack() #배치관리자 중 하나 
        self.connect() #쓰레드 가동보다 앞서서 접속이 되어 있어야 한다
        self.start() #쓰레드 가동 , 여기서 처리해야 하는 이유는 mainloop() 이후에 오는 코드는 윈도우 창을 닫아야 실행될수 있으므로 mainloop() 이전에 호출해야 한다      
        self.win.protocol("WM_DELETE_WINDOW", self.close_window) #윈도우 닫을때 이벤트 구현하기       
        self.win.mainloop()

    #-------------------------------------------------------------------------------------
    # 서버접속 메서드 정의
    #-------------------------------------------------------------------------------------
    def connect(self):
        self.sock=socket(AF_INET, SOCK_STREAM) #IPV4 주소체계, TCP/IP 프로토콜 사용
        self.sock.connect(self.serverAddr)
        print("connected server!!")

    #-------------------------------------------------------------------------------------
    # 서버측에 출력스트림으로 데이터 전송하기
    #-------------------------------------------------------------------------------------
    def send(self):      
        if self.flag==True:
            print("I will LED OFF")
            self.txt.set("off") #제어변수의 값은 set() 메서드로 변경할 수 있다.            
            self.bt["background"]="yellow"
            self.sock.send(bytes("on\n","UTF-8"))#서버에 메세지 전송
        else:
            print("I will LED On")                    
            self.txt.set("on")
            self.bt["background"]="gray"
            self.sock.send(bytes("off\n", "UTF-8"))#서버에 메세지 전송

        self.flag = not(self.flag) #부정 논리연산자 사용시 not() 사용함

    #-------------------------------------------------------------------------------------
    # 서버측 메세지 청취하기
    #-------------------------------------------------------------------------------------
    def listen(self):
        data=self.sock.recv(1024)
        msg=data.decode()

        if msg=="on":
            self.txt.set("off")
            self.bt["background"]="yellow"
        else:
            self.txt.set("on")
            self.bt["background"]="gray"

    #-------------------------------------------------------------------------------------
    #쓰레드 run 메서드 재정의 
    #-------------------------------------------------------------------------------------
    def run(self):    
        while True:   
            self.count+=1 
            print(self.count)
            self.listen()
            time.sleep(1.0)

            if self.threadFlag==False:
                break

    #-------------------------------------------------------------------------------------
    # 윈도우 종료 이벤트 처리 메서드
    #-------------------------------------------------------------------------------------
    def close_window(self):
        self.threadFlag = False # 쓰레드 break 시키기 위함
        self.sock.send(bytes("close", "UTF-8"))
        self.sock.close() #소켓 닫기, 소켓을 닫을때도 최후에 send 가 동작되므로 소켓을 닫는 다는 것을 서버에게 알려주지 않으면, 서버는 계속 브로드케스팅을 시도하게 되어 에러가 발생한다
        self.win.destroy() #프로세스 죽이기
        print("Window closed") 

client=Client() #인스턴스 생성    
from mainui import *

app = QApplication(sys.argv)
app.setStyleSheet(MainStyleSheet)

splash = SplashScreen(app)
status, new_project = splash.Run()

if (status == False): 
    exit()
else:
    splash.close()
    del splash

if __name__ == '__main__':
    window = MainWindow(app, new_project) 
    window.show()
    sys.exit(app.exec_())
    del window
    del app

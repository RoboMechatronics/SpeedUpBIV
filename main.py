from mainui import *

app = QApplication(sys.argv)
app.setStyleSheet(MainStyleSheet)

def main():
    splash = SplashScreen(app)

    status, new_project = splash.Run()

    if (status == False):
        exit()
    else:
        splash.close()
        del splash
    
    window = MainWindow(app, new_project) 
    window.show()    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
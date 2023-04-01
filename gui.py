import pandas as pd
from random import sample
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi(r"ui\main_menu.ui", self)
        self.playButton.clicked.connect(self.gotoGameScreen)
    
    def gotoGameScreen(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class GameScreen(QDialog):
    def __init__(self):
        super(GameScreen, self).__init__()
        loadUi(r"ui\game_screen.ui", self)
        self.endButton.clicked.connect(self.gotoEndScreen)
        self.input.returnPressed.connect(self.check)
        
        self.data = pd.read_excel("data/capitals.xlsx")
        self.data = self.data.drop(["NOM_ALPHA", "CODE", "NOM_LONG"], axis=1)

        self.nb_of_countries = 196

        self.random_list = sample(range(0, self.data.shape[0] - 1), self.nb_of_countries)
        
        self.score = 0
        self.loupés = []
        self.i = 0
        self.play_a_round(self.i)
    
    def play_a_round(self, i = int):
        self.random_num = self.random_list[i]
        if " | " in self.data.CAPITALE[self.random_num]:
            self.capitale = self.data.CAPITALE[self.random_num].split(" | ")
        else:
            self.capitale = [self.data.CAPITALE[self.random_num]]
        
        self.article = self.get_article(self.data.ARTICLE[self.random_num])
        self.nom = self.data.NOM[self.random_num]
        
        self.question_label.setText(
            f"Quelle est la capitale {self.article}{self.nom} ?")
        self.i += 1
    
    
    def get_article(self, article: str):
        articles = {
            "le": "du ",
            "la": "de la ",
            "les": "des ",
            "l'": "de l'"
        }
        return articles[article] if type(article) == str else "de "
    
    def check(self):
        self.answer = self.input.text()
        if self.i == self.nb_of_countries:
            self.gotoEndScreen()
        elif self.answer in self.capitale:
            self.score += 1
            self.result_label.setStyleSheet("QLabel { color: green }")
            self.result_label.setText("Bravo !")
            self.play_a_round(self.i)
        else:
            self.loupés.append([self.nom, self.capitale, self.article])
            self.result_label.setStyleSheet("QLabel { color: red }")
            self.result_label.setText(f"Loupé ! C'était {' ou '.join(self.capitale)}")
            self.play_a_round(self.i)
        self.progressBar.setValue(round(self.i / self.nb_of_countries * 100))
        self.score_label.setText(f"{self.score}/{self.i - 1}")
        self.input.setText("")
    
    def gotoEndScreen(self):
        global end_screen
        end_screen = EndScreen(self.score, self.i - 1)
        widget.addWidget(end_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class EndScreen(QDialog):
    global score
    def __init__(self, score, i):
        super(EndScreen, self).__init__()
        loadUi(r"ui\end_screen.ui", self)
        self.rejouerButton.clicked.connect(self.gotoGameScreen)
        self.score_label.setText(f"Vous avez {score} pt(s)")
        self.percentage_label.setText(f"Pourcentage de bonnes réponses : {round(score / i * 100, 1)}% ({score}/{i})")
    
    def gotoGameScreen(self):
        global game_screen
        widget.removeWidget(game_screen)
        game_screen = GameScreen()
        widget.addWidget(game_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    game_screen = GameScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_menu)
    widget.addWidget(game_screen)
    widget.setWindowTitle("Jeu des capitales (v3.0)")
    widget.setWindowIcon(QIcon(r"assets\icon.ico"))
    widget.setFixedWidth(1000)
    widget.setFixedHeight(600)
    widget.show()    
    try:
        sys.exit(app.exec_())
    except:
        print("Arrêt en cours...")
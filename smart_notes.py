from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import *
import json


app = QApplication([])
app.setWindowIcon(QtGui.QIcon('icon of notes.png'))
app.setStyle('Windows')

notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')


button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])

def add_note():
    name_note, result = QInputDialog.getText(
        notes_win, 'Добавить заметку', 'Название заметки:'
    )
    if name_note != '':
        notes[name_note] = {
            'текст': '',
            'теги': []
        }
        list_notes.addItem(name_note)
        list_tags.addItems(notes[name_note]['теги'])

def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('f.json', 'w', encoding= 'utf8') as file:
            json.dump(notes, file, ensure_ascii = False)

def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = field_text.toPlainText()
        with open('f.json', 'w', encoding= 'utf8') as file:
            json.dump(notes, file, ensure_ascii = False)

def add_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[name]['теги']:
            notes[name]['теги'].append(tag)
            list_tags.addItem(tag)
        with open('f.json', 'w', encoding= 'utf8') as file:
            json.dump(notes, file, ensure_ascii = False)

def del_tag():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[name]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])
        with open('f.json', 'w', encoding= 'utf8') as file:
            json.dump(notes, file, ensure_ascii= False)
    else:
        pass

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать по тегу' and tag:
        notes_filtered = dict()
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_tags.clear()
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать по тегу')

with open('f.json', 'r', encoding= 'utf8') as file:
    notes = json.load(file)

button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)

button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

list_notes.addItems(notes)

list_notes.itemClicked.connect(show_note)

notes_win.show()
app.exec_()

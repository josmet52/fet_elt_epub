#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fet_main.py
===========
Programme qui adapte au format epub3 les fichiers générés par la plateforme Publiwide 
Ce programme initialise quelques variables et lance la fonction new_job de la classe fet_class.py
fichiers : fet_main.py, fet_class.py
           fet_main <-- fet_class
auteur : josmet
date : 26.03.2018

modifications :
VERSION 0.18a - corrigé (anticipé) l'initialisation du chemin du fichier log
VERSION 0.19a - remplacé le fichier "validation_fr.js" par "validations_fr_jo.js" pour afficher les solutions des exercices en utilisant mieux la surface de l'écran
              - dans la function dir_job, remplacé le walk par un dir ainsi les sous répertoires ne sont pas parcourus
VERSION 0.19b - corrigé une erreur dans le nom du fichier de validation.js
VERSION 0.20a - correction pour le cover : l'image du cover est désormais la première image contenant le mot cover dans le nom 
VERSION 0.21a - mai-juin 2018 - Beaucoup de changement autant dans la présentation, dans la logique et dans les corrections des EPUBs
Version 0.21b - 13.06.2018 - Nettoyage phase 1 terminé
Version 0.21c - 21.06.2018 - Nettoyage phase 2 terminé, validation des commentaires en cours
Version 0.21d - 24.6.2018 - génération TOC en cours
Version 0.22a - 25.6.2018 - génération TOC et NCX a tester
Version 0.22b - 25.6.2018 - génération TOC et NCX a tester et mathml en cours
Version 0.22c - 25.6.2018 - tests et corrections diverses
Version 0.22d - 25.6.2018 - tests avec des fichiers provenant directement du site Publiwide
Version 0.22e - 29.6.2018 - correction de la gestion du fichier NAV et de ses entrées dans le content.opf
Version 0.23a - 03.02.2018 - ajout du management des boutons de navigation en cours
Version 0.24a - 08.04.2018 - btn nav ok + corrections sur improve file (affichage des fichiers non traités
Version 0.25b - 13.04.2018 - fet_add_nav_btn.py nettoyé
Version 0.25c - 13.04.2018 - fet_class.py nettoyé
Version 0.25d - 14.04.2018 - beautify: <h1>...</h1> and <h2>...</h2> on one line
Version 0.26a - 14.04.2018 - avec ajout btn pour nav dans Moodle
version 0.27a - 07.10.2019 - avec ajout btn file et dir et beautify finalisé
version 0.28a - 11.10.2019 - avec ajout nav btn, mise à jour des fichiers .js et .css automatique et beauty stable
version 0.28b - 11.10.2019 - avec ajout nav btn, mise à jour des fichiers .js et .css automatique et beauty stable
version 0.28c - 11.10.2019 - fet_class.px --> verify_file --> nouvelle version
version 0.28c - 11.10.2019 - fet_class.px --> verify_file --> nouvelle version finalisée stable
version 0.28d - 12.10.2019 - css pour menu ok et tous les fichiers .css révisés en v02_01
version 0.28e - 15.10.2019 - correction pour la mise à jour des liens dans les pages du rpertoire text
version 0.28f - 15.10.2019 - amélioration mise en page script
version 0.29a - 15.10.2019 - CSS pour TOC amélioré
"""

VERSION_FILE = "fet_main.py"
VERSION_NO = "0.29a"
VERSION_DATE = "15.10.2019"
VERSION_AUTEUR = "Joseph Métrailler"
VERSION_DESCRIPTION = "Préparation pour import Moodle en cours"
VERSION_STATUS = "stable"


# external libraries
# from shutil import copyfile
import tkinter as tk
import time
import os
from tkinter import *
from PIL import Image, ImageTk

# this programm files
# from fet_class import ClasseFet
# from fet_lib import ClassFetLib
from fet_class import ClasseFet
from fet_lib import ClasseFetLib
from fet_add_nav_btn import ClasseNavBtn
from fet_xml_formatter import ClasseFetXmlFormatter


def clean_quit(window_2_close):
    print("bye from QUIT button")
    window_2_close.destroy()
    sys.exit(0)

def ask_2_quit():
    lblInfo = tk.Label(btnFrame, text="waiting for the cancellation", textvariable="lblInfo", fg="green", bg="yellow", padx=2)
    lblInfo.grid(row=0, column=0)
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.configure(state="disabled")
    msgDisplay.update()
    # time.sleep(1)
    x.ask_2_quit()

def ask_addbtn_2_quit():
    lblInfo = tk.Label(btnFrame, text="waiting for the cancellation", textvariable="lblInfo", fg="green", bg="yellow", padx=2)
    lblInfo.grid(row=0, column=0)
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.configure(state="disabled")
    msgDisplay.update()
    # time.sleep(1)
    z.ask_2_quit()


def test_soft_go():
    btnStop = tk.Button(btnFrame, text="CANCEL", textvariable="btnStop", command=lambda: ask_2_quit(),
                        bg="light blue", state="disabled").grid(row=0, column=1, ipadx=15, padx=2, pady=5)
    x.test_soft()
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.destroy()



def dir_add_nav_btn_go():
    btnStop = tk.Button(btnFrame, text="CANCEL", textvariable="btnStop", command=lambda: ask_2_quit(),
                        bg="light blue", state="disabled").grid(row=0, column=1, ipadx=15, padx=2, pady=5)
    z.dir_add_nav_btn()
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.destroy()

def file_add_nav_btn_go():
    z.file_add_nav_btn()

def file_remove_nav_btn_go():
    z.file_remove_nav_btn()


def dir_btn_job_go():
    btnStop = tk.Button(btnFrame, text="CANCEL", textvariable="btnStop", command=lambda: ask_addbtn_2_quit(),
                        bg="light blue", state="disabled").grid(row=0, column=1, ipadx=15, padx=2, pady=5)
    z.dir_add_nav_btn()
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.destroy()

def dir_police_job_go():
    btnStop = tk.Button(btnFrame, text="CANCEL", textvariable="btnStop", command=lambda: ask_addbtn_2_quit(),
                        bg="light blue", state="disabled").grid(row=0, column=1, ipadx=15, padx=2, pady=5)
    z.change_police_dir_job()
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.destroy()

def dir_js_css_job_go():
    btnStop = tk.Button(btnFrame, text="CANCEL", textvariable="btnStop", command=lambda: ask_addbtn_2_quit(),
                        bg="light blue", state="disabled").grid(row=0, column=1, ipadx=15, padx=2, pady=5)
    z.js_css_dir_job()
    for b in btnFrame.winfo_children():
        if str((b.cget("textvariable"))).strip() == "btnStop" or str((b.cget("textvariable"))).strip() == "lblInfo":
            b.destroy()


def file_job_go():
    x.file_job()


def update_js_and_css_go():
    z.file_js_css_job()

def verify_job_go():
    x.verify_job()

def change_police_go():
    z.file_change_police_job()

def prepare_for_moodle_go():
    z.file_prepare_for_moodle()

def all_2_3_4_go():
    z.file2_3_4()

def all_1_2_3_4_go():
    z.file_1_2_3_4()

def remove_nav_btn_go():
    z.remove_nav_btn_job()

def xml_format_btn_go():
    f.beautify_xml()

def view_log_file_check():
    log_file_path_name = "".join([str(os.getcwd()).replace("\\", "/").replace("\n", ""), "/log/"])
    cmd = "".join(["notepad ", log_file_path_name, "epub_prob.txt"])
    os.system(cmd)

def view_log_dir_check():
    log_file_path_name = "".join([str(os.getcwd()).replace("\\", "/").replace("\n", ""), "/log/"])
    cmd = "".join(["notepad ", log_file_path_name, "epub_check_result.txt"])
    os.system(cmd)

def edit_options():
    prg_file_path_name = "".join([str(os.getcwd()).replace("\\", "/").replace("\n", ""), "/"])
    cmd = "".join(["notepad ", prg_file_path_name, "fet_epub.ini"])
    os.system(cmd)

def prg_essais():
    y.update_manifest_properties("blabla")

def hello():
    print ("hello!")

def about():
    tk.messagebox.showinfo \
        ("FET EPUB optimizer", "".join([ \
        "FET EPUB optimizer", "\n\n" \
        "Version no : ", VERSION_NO, " du ", VERSION_DATE, "\n", \
        "Status : ", VERSION_STATUS, "\n", \
        "Auteur : ", VERSION_AUTEUR, "\n\n", \
        "Remarque : \n", VERSION_DESCRIPTION, "\n"])
        )

def aide():
    tk.messagebox.showwarning \
        ("FET EPUB optimizer", "".join([ \
        "FET EPUB optimizer", "\n\n" \
        "Aide pas encore rédigée !"]))

# declare the display
msgDisplay = tk.Tk()
# fix the dimensions of the application window
WIN_WIDTH = 800
# WIN_WIDTH = 800
WIN_HEIGHT = 500
TOOL_BAR_HEIGHT = 80
# Get screen width and height
screenWidth = msgDisplay.winfo_screenwidth()  # width of the screen
screenHeight = msgDisplay.winfo_screenheight()  # height of the screen
# Calculate the smaller dimention between screen and application
maxWidth = min(WIN_WIDTH, screenWidth)
maxHeight = min(WIN_HEIGHT, screenHeight - TOOL_BAR_HEIGHT)
# open the application window in the center horizontaly and to the top verticaly
winPosX = (screenWidth / 2) - (int(maxWidth / 2))
winPosY = (screenHeight / 2) - (int(maxHeight / 2)) - int(TOOL_BAR_HEIGHT / 2)
# fix the geometry os the formular
msgDisplay.geometry('%dx%d+%d+%d' % (maxWidth, maxHeight, winPosX, winPosY))
msgDisplay.title("".join(["FET epub optimizer version : ", VERSION_NO, " - ", VERSION_DATE, " - ", VERSION_DESCRIPTION]))
img_tmp="C:/Users/jmetr/_data/mandats/FET_new/fet_elt_epub/ressources/logo_fet.png"
img=ImageTk.PhotoImage(Image.open(img_tmp))
msgDisplay.call('wm','iconphoto',msgDisplay,img)

beauty_yes_no = tk.BooleanVar()
beauty_yes_no.set = False
debug_yes_no = False
log_yes_no = False
verbose_yes_no = False


# create a frame in the display formular
# lblHead = tk.Label(msgDisplay, text="Welcome in fet_epub app", fg='black', font='"Segoe UI" 9 italic').pack(anchor=W, ipadx=1, ipady=2)
# print (tkFont.Font(font='TkDefaultFont').configure())
# create a frame in the display formular

msgFrame = tk.Frame(msgDisplay)
msgFrame.pack(fill=tk.Y, expand=1)
# add listBox and scrollbar for it
varMsg = StringVar()
msgList = tk.Listbox(msgFrame)
msgList.config(width=maxWidth)
msgSbar = tk.Scrollbar(msgFrame)
msgSbar.config(command=msgList.yview)
msgList.config(yscrollcommand=msgSbar.set)
msgSbar.pack(side=tk.RIGHT, fill=tk.Y)
msgList.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

menubar = Menu(msgDisplay)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=msgDisplay.quit)
menubar.add_cascade(label="File", menu=filemenu)

variable = StringVar(menubar)
variable.set('USER') # default value



# create a pulldown menu, and add it to the menu bar
singleepubmenu = Menu(menubar, tearoff=0)
singleepubmenu.add_command(label="Correct", command=lambda: file_job_go())
singleepubmenu.add_separator()
singleepubmenu.add_command(label="1-2-3-4", command=lambda: all_1_2_3_4_go())
singleepubmenu.add_command(label="2-3-4", command=lambda: all_1_2_3_4_go())
singleepubmenu.add_separator()
singleepubmenu.add_command(label="1-Add nav btn -> new_nav", command=lambda: add_nav_btn_go())
singleepubmenu.add_command(label="2-Update js and cs - > new_nav", command=lambda: update_js_and_css_go())
singleepubmenu.add_command(label="3-Change police -> new_tiptop", command=lambda: change_police_go())
singleepubmenu.add_command(label="4-Prepare for Moodle -> new_moodle", command=lambda: prepare_for_moodle_go())
menubar.add_cascade(label="single epub", menu=singleepubmenu)


# create a pulldown menu, and add it to the menu bar
task_epub_menu = Menu(menubar, tearoff=0)
task_epub_menu.add_command(label="Add nav btn file", command=lambda: file_add_nav_btn_go())
task_epub_menu.add_command(label="Add_nav_btn_dir", command=lambda: dir_add_nav_btn_go())
task_epub_menu.add_command(label="Remove nav btn", command=lambda: file_remove_nav_btn_go())
menubar.add_cascade(label="Nav btn", menu=task_epub_menu)

# create a pulldown menu, and add it to the menu bar
direpubmenu = Menu(menubar, tearoff=0)
direpubmenu.add_command(label="Correct dir", command=lambda: dir_add_nav_btn_go())
direpubmenu.add_command(label="Update js and css dir", command=lambda: dir_js_css_job_go())
direpubmenu.add_command(label="Add nav btn dir", command=lambda: dir_btn_job_go())
direpubmenu.add_command(label="Change police dir", command=lambda: dir_police_job_go())
menubar.add_cascade(label="all epub in dir", menu=direpubmenu)

utilmenu = Menu(menubar, tearoff=0)
utilmenu.add_command(label="Verify file", command=verify_job_go)
utilmenu.add_command(label="Beautify file", command=xml_format_btn_go)
utilmenu.add_separator()
utilmenu.add_command(label="View og file check", command=view_log_file_check)
utilmenu.add_command(label="View log dir check", command=view_log_dir_check)
utilmenu.add_separator()
utilmenu.add_command(label="Edit init file", command=edit_options)
# utilmenu.add_command(label="Test (prototype)", command=test_soft_go)
# utilmenu.add_command(label="Essai (prototype)", command=prg_essais)
menubar.add_cascade(label="Util", menu=utilmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Aide", command=aide)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
msgDisplay.config(menu=menubar)


# prepare the formular to be displayed
btnFrame = tk.Frame(msgDisplay)
btnFrame.pack(side=tk.BOTTOM)

# file jobs
col_no = 2
btnFileJob = tk.Button(btnFrame, text="Correct file", textvariable="btnFileJob", command=lambda: file_job_go(),
                       bg="azure3").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)
col_no += 1
btnJsCss = tk.Button(btnFrame, text="js+css file", textvariable="btnJsCss", command=lambda: update_js_and_css_go(),
                     bg="azure3").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)
col_no += 1
btnAddNav = tk.Button(btnFrame, text="Add btn file", textvariable="btnAddNav", command=lambda: add_nav_btn_go(),
                     bg="azure3").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)

# dir jobs
col_no += 1
btnDirJob = tk.Button(btnFrame, text="Correct dir", textvariable="btnDirJob", command=lambda: dir_add_nav_btn_go(),
                      bg="azure").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)
col_no += 1
btnJsCssJob = tk.Button(btnFrame, text="js+css dir", textvariable="btnDirJsCss", command=lambda: dir_js_css_job_go(),
                      bg="azure").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)
col_no += 1
btnDirBtnJob = tk.Button(btnFrame, text="Add btn dir", textvariable="btnDirBtnJob", command=lambda: dir_btn_job_go(),
                      bg="azure").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)

# quit
col_no += 1
btnQuit = tk.Button(btnFrame, text="QUIT", textvariable="btnQuit", command=lambda: clean_quit(msgDisplay),
                    bg="light blue").grid(row=0, column=col_no, ipadx=15, padx=2, pady=5)


nav_bar_choice = StringVar(msgDisplay)
nav_bar_choice.set("For the nav bar choose") # default value

# optionNavBtn = OptionMenu(msgDisplay, nav_bar_choice, "top fix", "bottom fix", "no nav bar")
# optionNavBtn.pack(side=tk.BOTTOM)

y = ClasseFetLib()
# initialisation of the class c_Fet
x = ClasseFet(varMsg, msgList, msgDisplay, btnFrame)
z = ClasseNavBtn(varMsg, msgList, msgDisplay, btnFrame, nav_bar_choice.get())
f = ClasseFetXmlFormatter(varMsg, msgList, msgDisplay, btnFrame, nav_bar_choice.get())
# display the formular and wait until somebody push a button
x.manage_info("To start click on a button", 1, 1)


msgDisplay.mainloop()

# Quit pressed, bye bye
print("... bye ...")
sys.exit(0)

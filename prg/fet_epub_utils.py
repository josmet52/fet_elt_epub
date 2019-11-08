#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fet_nav_btn.py
============
Cette classe contient les procedures nécessaires au management des boutons de navigation dans les fichiers EPUB
Il doit se trouver dans le même directory que le programme fet_main.py

fichier : fet_nav_btn.py
utilisé par : fet_main.py
auteur : josmet
date : 09.03.2019
version 0.7
"""

import os
import time
import uuid
import zipfile
import shutil
import tkinter as tk

from datetime import datetime
from tkinter import *
from tkinter import filedialog

from fet_class import ClasseFet
from fet_lib import ClasseFetLib
from fet_ini import ClasseIni

y = ClasseFetLib()
ini = ClasseIni()

class ClasseNavBtn:

    def __init__(self, var_msg, msg_list, msg_display, btn_frame, option_nav_btn_position):

        # menu_bar_font_size
        self.menu_bar_font_size = "12px"
        self.FONT_NAME = "Comic sans MS"

        # initialisation variables
        self.var_msg = var_msg
        self.msg_list = msg_list
        self.msg_display = msg_display
        self.btn_frame = btn_frame
        self.option_nav_btn_position = option_nav_btn_position
        self.asked_2_quit = False

        # self.pos_nav_bar = "TOP"
        self.pos_nav_bar = "BOTTOM"
        self.second_try = 0

        self.CONTENT_OPF_FILE_NAME = "content.opf"
        self.INI_FILE_NAME = "fet_epub.ini"
        self.LOG_FILE_NAME = "fet_log.txt"
        self.ERROR_WAIT_TIME = 0.5

        # init variables
        self.cwd = "".join([str(os.getcwd()).replace("\\", "/").replace("\n", ""), "/"])
        self.log_path = "".join([self.cwd, "log/"])
        self.log_path_file_name = "".join([self.log_path, self.LOG_FILE_NAME])

        # initialisation des variable de la classe à partir de la classe ini qui le fichier fet_epub.ini
        self.strings_names_js = ini.strings_names_js
        self.strings_names_css = ini.strings_names_css
        self.mandatory_names_js = ini.mandatory_names_js
        self.mandatory_names_css = ini.mandatory_names_css
        self.org_path = ini.org_path
        self.new_path = ini.new_path
        self.tmp_path = ini.tmp_path
        self.new_nav_path = ini.new_nav_path
        self.new_js_path = ini.new_js_path
        self.new_moo_path = ini.new_moo_path
        self.new_police_path = ini.new_police_path
        self.js_css_path = ini.js_css_path
        self.DEBUG = ini.DEBUG
        self.LOG_THIS_RUN = ini.LOG_THIS_RUN
        self.VERBOSE = ini.VERBOSE
        self.WITH_DIR = ini.WITH_DIR
        self.WITH_ZIP = ini.WITH_ZIP
        self.IMG_SIZE_MAX = ini.IMG_SIZE_MAX
        self.TOC_DEEP = ini.TOC_DEEP
        self.FONT_NAME = ini.FONT_NAME
        self.VERIF_EPUB = ini.VERIF_EPUB

        # # lecture des répertoires dans le fichier .ini
        # self.ini_path_file_name = "".join([self.cwd, self.INI_FILE_NAME])
        # if os.path.isfile(self.ini_path_file_name):
        #
        #     with open(self.ini_path_file_name, "r", encoding="utf-8") as f_init:
        #         r = f_init.readlines()
        #         for p in r:
        #             x = p.split("=")
        #             x[0] = x[0].strip().lower()
        #             if len(x) > 1 :
        #                 x[1] = x[1].strip().lower()
        #
        #                 # ne pas traiter les commentaires
        #                 if x[0][:1] != "#":
        #
        #                     if x[0] == "short_strings_names_js":
        #                         x_js = x[1].split(" ")
        #                         for x_js_strings in x_js:
        #                             self.strings_names_js.append(x_js_strings)
        #
        #                     if x[0] == "short_strings_names_css":
        #                         x_css = x[1].split(" ")
        #                         for x_css_strings in x_css:
        #                             self.strings_names_css.append(x_css_strings)
        #
        #                     if x[0] == "short_mandatory_files_js":
        #                         x_js = x[1].split(" ")
        #                         for x_js_strings in x_js:
        #                             self.mandatory_names_js.append(x_js_strings)
        #
        #                     if x[0] == "short_mandatory_files_css":
        #                         x_css = x[1].split(" ")
        #                         for x_css_strings in x_css:
        #                             self.mandatory_names_css.append(x_css_strings)
        #
        #                     if x[0] == "ini_org_dir":
        #                         self.org_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_new_dir":
        #                         self.new_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_tmp_dir":
        #                         self.tmp_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_new_nav_dir":
        #                         self.new_nav_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_new_js_css_dir":
        #                         self.new_js_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_new_moodle_dir":
        #                         self.new_moo_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_new_police_dir":
        #                         self.new_police_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_js_css_ok_dir":
        #                         self.js_css_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
        #                                             "").replace("//", "/")
        #
        #                     elif x[0] == "ini_var_debug" :
        #                         if x[1].replace("\n", "") == "true" : self.DEBUG = True
        #                         else : self.DEBUG = False
        #
        #                     elif x[0] == "ini_var_log_this_run" :
        #                         if x[1].replace("\n", "") == "true" : self.LOG_THIS_RUN = True
        #                         else : self.LOG_THIS_RUN = False
        #
        #                     elif x[0] == "ini_var_verbose" :
        #                         if x[1].replace("\n", "") == "true" : self.VERBOSE = True
        #                         else : self.VERBOSE = False
        #
        #                     elif x[0] == "ini_var_with_dir" :
        #                         if x[1].replace("\n", "") == "true" : self.WITH_DIR = True
        #                         else : self.WITH_DIR = False
        #
        #                     elif x[0] == "ini_var_with_zip" :
        #                         if x[1].replace("\n", "") == "true" : self.WITH_ZIP = True
        #                         else : self.WITH_ZIP = False
        #
        #                     elif x[0] == "ini_var_img_size_max" :
        #                         if x[1].isnumeric() : self.IMG_SIZE_MAX = int(x[1])
        #                         else : self.IMG_SIZE_MAX = 20000
        #
        #                     elif x[0] == "ini_var_toc_deep" :
        #                         self.TOC_DEEP = x[1]
        #
        #                     elif x[0] == "ini_var_font" :
        #                         self.FONT_NAME = x[1]
        #
        #                     elif x[0] == "ini_var_verif_epub" :
        #                         if x[1].replace("\n", "") == "true" : self.VERIF_EPUB = True
        #                         else : self.VERIF_EPUB = False

    def ask_2_quit(self):
        """
        this function l....
        """
        self.asked_2_quit = True
        self.msg_display.update_idletasks()
        # print("arret demandé")

    def file_1_2_3(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier pour : addnav, js-css, police, moodle",
                                                     initialdir=self.new_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")
        file_name = os.path.basename(in_path_file_name)

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            #1
            dir_name = self.new_path
            work_in_path_file_name = "".join([dir_name, file_name])
            self.update_js_and_css(work_in_path_file_name)  # start the optimisation
            #2
            dir_name = self.new_js_path
            fn = file_name.split(".")
            file_name = "".join([fn[0], "_js.", fn[1]])
            work_in_path_file_name = "".join([dir_name, file_name])
            self.change_police(work_in_path_file_name)  # start the optimisation
            #3
            dir_name = self.new_police_path
            file_name = "".join([fn[0], "_js_pol.", fn[1]])
            work_in_path_file_name = "".join([dir_name, file_name])
            self.add_nav_btn(work_in_path_file_name)  # start the optimisation

            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["1-2-3 terminated: ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            self.msg_list.insert(tk.END, "Select a epub to improve")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")

    def file_1_2_3_4(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier auquel il faut ajouter la barre de navigations",
                                                     initialdir=self.new_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")
        file_name = os.path.basename(in_path_file_name)
        dir_name = os.path.dirname(in_path_file_name)

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            #1 js_css
            dir_name = self.new_path
            work_in_path_file_name = "".join([dir_name, file_name])
            self.update_js_and_css(work_in_path_file_name)  # start the optimisation
            #2 police
            dir_name = self.new_js_path
            fn = file_name.split(".")
            file_name = "".join([fn[0], "_js.", fn[1]])
            work_in_path_file_name = "".join([dir_name, file_name])
            self.change_police(work_in_path_file_name)  # start the optimisation
            #3 nav btn
            dir_name = self.new_police_path
            file_name = "".join([fn[0], "_js_pol.", fn[1]])
            work_in_path_file_name = "".join([dir_name, file_name])
            self.add_nav_btn(work_in_path_file_name)  # start the optimisation
            #4 moodle
            dir_name = self.new_nav_path
            file_name = "".join([fn[0], "_js_pol_wnav.", fn[1]])
            work_in_path_file_name = "".join([dir_name, file_name])
            self.prepare_for_moodle(work_in_path_file_name)  # start the optimisation

            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["1-2-3-4 terminated: ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            self.msg_list.insert(tk.END, "Select a epub to improve")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")

    def dir_update_js_and_css(self):

        """
        Cette fonction permet de vérifier tous les epub's contenus dans un répertoire
        Elle parcoure le répertoire choisi, vérifie qu'il y ait bien des fichiers epub puis,
        pour chaque ficheir epub, elle appelle la fonction file_job pour exécuter l'amélioration de façon individelle
        """
        # variable qui permet de savoir si l'utilisateur a demandé à interrompre la procédure
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # disable all buttons that can not be used during this task
        u.manage_buttons("btnDirJob", "in")
        self.asked_2_quit = False

        dirjob_tstart = time.time()
        # variable pour que la fonction sache que l'appel vient d'ici et gère les messages en conséquence
        self.dir_job_status = True
        # demande le nom du répertoire à travailler
        file_options = {}
        file_options['initialdir'] = self.new_path
        file_options['title'] = 'Please select a directory with epub(s)'
        dir_name = filedialog.askdirectory(**file_options)

        file_output_result_path_name = "".join([self.log_path, "epub_check_result.txt"])
        with open(file_output_result_path_name, "w", encoding="utf-8") as prob_file:
            prob_file.write(str(datetime.now()))

        # erreurs totales
        fatal_tot = 0
        error_tot = 0
        warn_tot = 0
        recap_tot = []

        # On controle que le répertoire n'est pas vide
        if dir_name != "":
            # only the .epub files
            only_epub_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                               and os.path.splitext(f)[1] == ".epub"]
            if len(only_epub_files) > 0:
                # there is .epub files
                for test_file in only_epub_files:
                    t_start = time.time()
                    in_path_file_name = "/".join([dir_name, test_file])
                    in_file_name = os.path.basename(in_path_file_name)
                    out_path_file_name = self.update_js_and_css(in_path_file_name)

                    if self.VERIF_EPUB:
                        u.manage_info("---------------------------------------------------------", u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["VERIFICATION EPUB : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Fichier : ", os.path.basename(in_file_name)]), u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        u.manage_info("en cours de vérification. Patientez SVP ...", u.DISPLAY_AND_LOG, u.COLOR_PURPLE)

                        ret_status, n_fatal, n_error,  n_warn = u.check_epub(out_path_file_name, file_output_result_path_name)
                        fatal_tot += n_fatal
                        error_tot += n_error
                        warn_tot += n_warn
                        recap_tot.append("".join([test_file, " : ",str(n_fatal), " fatals / ", str(n_error), " errors / ", str(n_warn), " warnings\n"]))

                        u.manage_info(ret_status, u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        msg = " "
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                        if self.asked_2_quit:
                            break
                        else:
                            time.sleep(u.pause_time)
                msg_err = "".join(["Check status total : ", str(fatal_tot), " fatal / ", str(error_tot), " error / ", str(warn_tot), " warn"])
                if not self.asked_2_quit:
                    elapsed_time = int(time.time() - dirjob_tstart)
                    elapsed_min = elapsed_time // 60
                    elapsed_sec = elapsed_time % 60
                    if elapsed_min > 0 :
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_min), " min ", str(elapsed_sec), " sec"])
                    else:
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_sec), " sec"])

                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                        u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                else:
                    msg = "".join(["Job terminated by user !"])
                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                # there is no .epub files
                tk.messagebox.showinfo("Répertoire d'entrée \n", "Il n'y a pas de fichiers .epub dans ce répertoire. \nRefaites votre choix", icon='info')

        # rétablir l'état normal des boutons'
        u.manage_buttons("btnDirJob", "out")

    def file_update_js_and_css(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier auquel il faut ajouter la barre de navigations",
                                                     initialdir=self.new_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            # self.in_file_name = os.path.basename(in_path_file_name)
            self.update_js_and_css(in_path_file_name)  # start the optimisation
        else:
            self.msg_list.insert(tk.END, "Select a epub to improve")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")

    def update_js_and_css(self, in_path_file_name):
        """
            This function add nav buttons in the selected Epub
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        if len(in_path_file_name) != 0:

            # create the out_file_name with the in_file_name
            if "_js" not in in_path_file_name:
                out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_js.epub")
            else:
                out_file_name = os.path.basename(in_path_file_name)

            # the out filename goes in the wnav directory
            out_path_file_name = "".join([self.new_js_path, out_file_name])
            # prepare the text to display in and out files
            txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
            txt_out_file = "".join(["Dst file : ", out_path_file_name])

            # display the files status
            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["Change .js and .css file with \"à jour\" files : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
            u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(in_path_file_name, "r") as z:
                z.extractall(temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, ops_dir = u.get_ops_dir(temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
            css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
            js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
            font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])

            f_ok = True
            t_start = time.time()  # store the start time
            u.manage_info("... remplacement des fichiers .js et .css en cours . Patientez SVP ...", u.DISPLAY_AND_LOG)

            # créer le dictionnaire des fichiers js et css existants
            # js_files_string = {}
            # css_files_string = {}
            # new_js_files_names = {}
            # new_css_files_names = {}
            # for root, dirs, files in os.walk(self.js_css_path):
            #     # pour tous les fichiers js et css à jour
            #     for jscss_new_file in files:
            #         f_l = jscss_new_file.split(".")
            #         jscss_file_name = f_l[0]
            #         jscss_file_ext = f_l[1]
            #         # fichiers javascript
            #         if jscss_file_ext == "js":
            #             for js_strings_names in self.strings_names_js: # parcourir la liste des string extraite du fichier .ini
            #                 if js_strings_names in jscss_file_name: # c'est un fichier à remplacer
            #                     js_files_string[js_strings_names] = False # ajouter le string au dictionnaire des strings
            #                     new_js_files_names[js_strings_names] = jscss_new_file # ajouter le nom du nopuveau fichier au dictionnaire des fichiers
            #                     new_name = new_js_files_names[js_strings_names]
            #
            #         if jscss_file_ext == "css":
            #             for css_strings_names in self.strings_names_css:
            #                 if css_strings_names in jscss_file_name:
            #                     css_files_string[css_strings_names] = False
            #                     new_css_files_names[css_strings_names] = jscss_new_file
            #
            # # remplacer les fichiers .js par ceux à jour
            # for existing_string in js_files_string:
            #     # chercher old_js_file_name dans le répertoire/misc/... du epub
            #     for r_js, d_js, f_js in os.walk(js_path_dir): # répertoire js du epub
            #         # pour tous les fichiers anciens
            #         for old_js_file_name in f_js:
            #             if existing_string in old_js_file_name: # c'est le fichier à remplacer
            #                 old_file_name = old_js_file_name
            #                 new_file_name = new_js_files_names[existing_string]
            #                 # remplacer seulement si c'est une nouvelle version
            #                 if old_file_name != new_file_name:
            #                     # noter que le fichier est nouveau
            #                     js_files_string[existing_string] = True
            #                     # supprimer le fichier old
            #                     os.remove("".join([js_path_dir, old_file_name])) # supprimer le fichier js existant
            #                     # copier le fichier new
            #                     sce = "".join([self.js_css_path, new_file_name])
            #                     dst = "".join([js_path_dir, new_js_files_names[existing_string]])
            #                     shutil.copy2(sce, dst)
            #                     v_msg = "remplacement du fichier " + old_file_name + " par " + new_file_name
            #                     u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            # u.manage_info(" ", u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            #
            # # remplacer les fichiers .css par ceux à jour
            # for existing_string in css_files_string:
            #     # chercher old_css_file_name dans le répertoire /styles/... du epub
            #     for r_css, d_css, f_css in os.walk(css_path_dir): # répertoire css du epub
            #         # pour tous les fichiers anciens
            #         for old_css_file_name in f_css:
            #             if existing_string in old_css_file_name: # c'est le fichier à remplacer
            #                 old_file_name = old_css_file_name
            #                 new_file_name = new_css_files_names[existing_string]
            #                 # remplacer seulement si c'est une nouvelle version
            #                 if old_file_name != new_file_name:
            #                     # noter que le fichier est nouveau
            #                     css_files_string[existing_string] = True
            #                     # supprimer le fichier old
            #                     os.remove("".join([css_path_dir, old_file_name])) # supprimer le fichier css existant
            #                     # copier le fichier new
            #                     sce = "".join([self.js_css_path, new_file_name])
            #                     dst = "".join([css_path_dir, new_css_files_names[existing_string]])
            #                     shutil.copy2(sce, dst)
            #                     v_msg = "remplacement du fichier " + old_file_name + " par " + new_file_name
            #                     u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            # u.manage_info(" ", u.DISPLAY_AND_LOG, u.COLOR_BLUE)

            # open opf file and read <spine> elements
            v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
            if v_return != "":
                u.manage_info(v_return, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            else:
                # verif si nav.xhtml est dans la Spine si non l'ajouter
                nav_found = False
                for v_file in spine_list:
                    if v_file == "nav.xhtml":
                        nav_found = True
                        break
                if not nav_found:
                    with open(ops_path_filename, "r", encoding="utf-8") as opf_file:
                        opf_data = opf_file.readlines()
                        index = 0
                        break_ok = False
                    index_pos_for_nav = 0
                    for line in opf_data:
                        if "</spine>" in line:
                            index_pos_for_nav = index
                        index += 1
                    opf_data.insert(index_pos_for_nav , "<itemref idref=\"nav.xhtml\"/>\n")

                    with open(ops_path_filename, "w", encoding="utf-8") as opf_file:
                        for line in opf_data:
                            opf_file.writelines(line)

                self.update_js_and_css_heart(ops_path_filename, js_path_dir, css_path_dir, text_path_dir)

                #     # relire la spinelist mise à jour
                #     v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
                #
                # # pour tous les fichiers inclus dans la Spine_list
                # for current_page_number in range(len(spine_list)):
                #     v_msg = spine_list[current_page_number] + " : mise à jour des ref js et css"
                #     u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                #     working_file = "".join([text_path_dir, spine_list[current_page_number]])
                #     data = []
                #     data_new = []
                #
                #     # replace all modified .js references
                #     # read the xhtml file
                #     with open(working_file, "r", encoding="utf-8") as rFile:
                #         data = rFile.readlines()
                #     end_head_found = False
                #     begin_head_found = False
                #
                #     for l in data:
                #         if "<head>" in l :
                #             begin_head_found = True
                #         if begin_head_found and not end_head_found:
                #             for exist_str in js_files_string:
                #                 if js_files_string[exist_str] and exist_str in l and "<script" in l:
                #                     # to_replace = True
                #                     if "</script>" in l:
                #                         txt_to_insert = self.get_link_js_string("".join(["Misc/",new_js_files_names[exist_str]]))
                #                     else: # <script et </script sur la même ligne
                #                         txt_to_insert = self.get_link_js_string("".join(["Misc/",new_js_files_names[exist_str]])).replace("</script>", "")
                #                     l = txt_to_insert
                #         if "</head>" in l :
                #             end_head_found = True
                #         data_new.append(l)
                #
                #     with open(working_file, "w", encoding="utf-8") as txt_file:
                #         for l in data_new:
                #             txt_file.writelines(l)
                #
                #     # replace all modified .css references
                #     data_new = []
                #     # read the xhtml file
                #     with open(working_file, "r", encoding="utf-8") as rFile:
                #         data = rFile.readlines()
                #     end_head_found = False
                #     begin_head_found = False
                #
                #     for l in data:
                #         if "<head>" in l :
                #             begin_head_found = True
                #         if begin_head_found and not end_head_found:
                #             for exist_str in css_files_string:
                #                 if css_files_string[exist_str] and exist_str in l and "<link" in l:
                #                     l = self.get_link_css_string("".join(["Styles/",new_css_files_names[exist_str]]))
                #         if "</head>" in l :
                #             end_head_found = True
                #         data_new.append(l)
                #
                #     with open(working_file, "w", encoding="utf-8") as txt_file:
                #         for l in data_new:
                #             txt_file.writelines(l)
                #
                # # traitement du manifest de content.opf
                # opf_file = ops_path_filename
                # self.update_manifest_line(opf_file, ".js", "Misc/", js_files_string, new_js_files_names)
                # self.update_manifest_line(opf_file, ".css", "Styles/", css_files_string, new_css_files_names)

                # FINAL TASKS
                # ===================
                # beautify all xhtml files
                u.manage_info("pretifying the xhtml", u.LOG_ONLY, u.COLOR_PURPLE)
                y.pretify_xhtml(text_path_dir)

                # add <br/> at the end of <body>
                u.manage_info("adding <br/> at the end of each body section", u.LOG_ONLY, u.COLOR_PURPLE)
                y.add_br(text_path_dir)

                # creating the zipped epub file
                msg = "... creating the final zipped epub file"
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                u.zip_epub(temp_path_dir, out_path_file_name)

                if u.WITH_ZIP:
                    # create also the zip file
                    u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))

                if u.WITH_DIR:
                    # and also the directory with all the epub files
                    out_dir_name = out_path_file_name.replace(".epub", "")

                    # if exist delete the directory
                    if os.path.exists(out_dir_name):
                        shutil.rmtree(out_dir_name, ignore_errors=True)
                    # create the new dir
                    shutil.copytree(temp_path_dir, out_dir_name)
                    os.chdir(self.cwd)

                # info that all its finished and deleting temporary files and directories
                u.manage_info("... putzing", u.DISPLAY_AND_LOG)
                # remove temporary files and directories
                if os.path.exists(temp_path_dir):
                    v_return = u.empty_dir(temp_path_dir)
                    if v_return != "":
                        v_msg = "".join([self.log_path_file_name, v_return])
                        u.write_in_logfile(v_msg)
                    f_msg = "function new_job, final tasks : remove temp dir"
                    try:
                        os.rmdir(temp_path_dir)
                    except:
                        try:
                            time.sleep(self.ERROR_WAIT_TIME)
                            self.second_try += 1
                            u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                            u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                            os.rmdir(temp_path_dir)
                        except:
                            u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

            elapsed_time = time.time() - t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Mise à jour .js et .css dans le fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(in_path_file_name)])
                u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !"])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                msg_info = "".join(
                    ["Traitements des erreurs"])
                u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            # no file selected so do nothing
            u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
            u.manage_info("Select a epub", u.DISPLAY_ONLY, u.COLOR_BLUE)
        return out_path_file_name

    def update_js_and_css_heart(self, ops_path_filename, js_path_dir, css_path_dir, text_path_dir):

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        # créer le dictionnaire des fichiers js et css existants
        js_files_string = {}
        css_files_string = {}
        new_js_files_names = {}
        new_css_files_names = {}
        for root, dirs, files in os.walk(self.js_css_path):
            # pour tous les fichiers js et css à jour
            for jscss_new_file in files:
                f_l = jscss_new_file.split(".")
                jscss_file_name = f_l[0]
                jscss_file_ext = f_l[1]
                # fichiers javascript
                if jscss_file_ext == "js":
                    for js_strings_names in self.strings_names_js: # parcourir la liste des string extraite du fichier .ini
                        if js_strings_names in jscss_file_name: # c'est un fichier à remplacer
                            js_files_string[js_strings_names] = False # ajouter le string au dictionnaire des strings
                            new_js_files_names[js_strings_names] = jscss_new_file # ajouter le nom du nopuveau fichier au dictionnaire des fichiers
                            new_name = new_js_files_names[js_strings_names]
                # fichiers css
                if jscss_file_ext == "css":
                    for css_strings_names in self.strings_names_css:
                        if css_strings_names in jscss_file_name:
                            css_files_string[css_strings_names] = False
                            new_css_files_names[css_strings_names] = jscss_new_file

        # remplacer les fichiers .js par ceux à jour
        for existing_string in js_files_string:
            # chercher old_js_file_name dans le répertoire/misc/... du epub
            for r_js, d_js, f_js in os.walk(js_path_dir): # répertoire js du epub
                # pour tous les fichiers anciens
                for old_js_file_name in f_js:
                    if existing_string in old_js_file_name: # c'est le fichier à remplacer
                        old_file_name = old_js_file_name
                        new_file_name = new_js_files_names[existing_string]
                        # remplacer seulement si c'est une nouvelle version
                        if old_file_name != new_file_name:
                            # noter que le fichier est nouveau
                            js_files_string[existing_string] = True
                            # supprimer le fichier old
                            os.remove("".join([js_path_dir, old_file_name])) # supprimer le fichier js existant
                            # copier le fichier new
                            sce = "".join([self.js_css_path, new_file_name])
                            dst = "".join([js_path_dir, new_js_files_names[existing_string]])
                            shutil.copy2(sce, dst)
                            v_msg = "remplacement du fichier " + old_file_name + " par " + new_file_name
                            u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
        u.manage_info(" ", u.DISPLAY_AND_LOG, u.COLOR_BLUE)

        # remplacer les fichiers .css par ceux à jour
        for existing_string in css_files_string:
            # chercher old_css_file_name dans le répertoire /styles/... du epub
            for r_css, d_css, f_css in os.walk(css_path_dir): # répertoire css du epub
                # pour tous les fichiers anciens
                for old_css_file_name in f_css:
                    if existing_string in old_css_file_name: # c'est le fichier à remplacer
                        old_file_name = old_css_file_name
                        new_file_name = new_css_files_names[existing_string]
                        # remplacer seulement si c'est une nouvelle version
                        if old_file_name != new_file_name:
                            # noter que le fichier est nouveau
                            css_files_string[existing_string] = True
                            # supprimer le fichier old
                            os.remove("".join([css_path_dir, old_file_name])) # supprimer le fichier css existant
                            # copier le fichier new
                            sce = "".join([self.js_css_path, new_file_name])
                            dst = "".join([css_path_dir, new_css_files_names[existing_string]])
                            shutil.copy2(sce, dst)
                            v_msg = "remplacement du fichier " + old_file_name + " par " + new_file_name
                            u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
        u.manage_info(" ", u.DISPLAY_AND_LOG, u.COLOR_BLUE)

        # lire la spinelist mise à jour
        v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)

        # pour tous les fichiers xhtml inclus dans la Spine_list
        for current_page_number in range(len(spine_list)):
            v_msg = spine_list[current_page_number] + " : mise à jour des ref js et css"
            u.manage_info(v_msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            working_file = "".join([text_path_dir, spine_list[current_page_number]])
            data = []
            data_new = []

            # replace all modified .js references
            # read the xhtml file
            with open(working_file, "r", encoding="utf-8") as rFile:
                data = rFile.readlines()
            end_head_found = False
            begin_head_found = False

            for l in data:
                if "<head>" in l :
                    begin_head_found = True
                if begin_head_found and not end_head_found:
                    for exist_str in js_files_string:
                        # if js_files_string[exist_str] and exist_str in l and "<script" in l:
                        if exist_str in l and "<script" in l:
                            # to_replace = True
                            if "</script>" in l: # <script et </script sur la même ligne
                                txt_to_insert = self.get_link_js_string("".join(["Misc/",new_js_files_names[exist_str]]))
                            else: # <script et </script sur deux lignes
                                txt_to_insert = self.get_link_js_string("".join(["Misc/",new_js_files_names[exist_str]])).replace("</script>", "")
                            l = txt_to_insert
                if "</head>" in l :
                    end_head_found = True
                data_new.append(l)

            with open(working_file, "w", encoding="utf-8") as txt_file:
                for l in data_new:
                    txt_file.writelines(l)

            # replace all modified .css references
            data_new = []
            # read the xhtml file
            with open(working_file, "r", encoding="utf-8") as rFile:
                data = rFile.readlines()
            end_head_found = False
            begin_head_found = False

            for l in data:
                if "<head>" in l :
                    begin_head_found = True
                if begin_head_found and not end_head_found:
                    for exist_str in css_files_string:
                        # if css_files_string[exist_str] and exist_str in l and "<link" in l:
                        if exist_str in l and "<link" in l:
                            l = self.get_link_css_string("".join(["Styles/",new_css_files_names[exist_str]]))
                if "</head>" in l :
                    end_head_found = True
                data_new.append(l)

            with open(working_file, "w", encoding="utf-8") as txt_file:
                for l in data_new:
                    txt_file.writelines(l)

        # traitement du manifest de content.opf
        opf_file = ops_path_filename
        self.update_manifest_line(opf_file, ".js", "Misc/", js_files_string, new_js_files_names)
        self.update_manifest_line(opf_file, ".css", "Styles/", css_files_string, new_css_files_names)

        return ""

    def dir_change_police(self):

        """
        Cette fonction permet de vérifier tous les epub's contenus dans un répertoire
        Elle parcoure le répertoire choisi, vérifie qu'il y ait bien des fichiers epub puis,
        pour chaque ficheir epub, elle appelle la fonction file_job pour exécuter l'amélioration de façon individelle
        """
        # variable qui permet de savoir si l'utilisateur a demandé à interrompre la procédure
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # disable all buttons that can not be used during this task
        u.manage_buttons("btnDirJob", "in")
        self.asked_2_quit = False

        dirjob_tstart = time.time()
        # variable pour que la fonction sache que l'appel vient d'ici et gère les messages en conséquence
        self.dir_job_status = True
        # demande le nom du répertoire à travailler
        file_options = {}
        file_options['initialdir'] = self.new_js_path #self.org_path
        file_options['title'] = 'Please select a directory with epub(s)'
        dir_name = filedialog.askdirectory(**file_options)

        file_output_result_path_name = "".join([self.log_path, "epub_check_result.txt"])
        with open(file_output_result_path_name, "w", encoding="utf-8") as prob_file:
            prob_file.write(str(datetime.now()))

        # erreurs totales
        fatal_tot = 0
        error_tot = 0
        warn_tot = 0
        recap_tot = []

        # On controle que le répertoire n'est pas vide
        if dir_name != "":
            # only the .epub files
            only_epub_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                               and os.path.splitext(f)[1] == ".epub"]
            if len(only_epub_files) > 0:
                # there is .epub files
                for test_file in only_epub_files:
                    t_start = time.time()
                    in_path_file_name = "/".join([dir_name, test_file])
                    in_file_name = os.path.basename(in_path_file_name)
                    out_path_file_name = self.change_police(in_path_file_name)

                    if self.VERIF_EPUB:
                        u.manage_info("---------------------------------------------------------", u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Changement police : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Fichier : ", os.path.basename(in_file_name)]), u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        u.manage_info("en cours de vérification. Patientez SVP ...", u.DISPLAY_AND_LOG, u.COLOR_PURPLE)

                        ret_status, n_fatal, n_error,  n_warn = u.check_epub(out_path_file_name, file_output_result_path_name)
                        fatal_tot += n_fatal
                        error_tot += n_error
                        warn_tot += n_warn
                        recap_tot.append("".join([test_file, " : ",str(n_fatal), " fatals / ", str(n_error), " errors / ", str(n_warn), " warnings\n"]))

                        u.manage_info(ret_status, u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        msg = " "
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                        if self.asked_2_quit:
                            break
                        else:
                            time.sleep(u.pause_time)
                msg_err = "".join(["Check status total : ", str(fatal_tot), " fatal / ", str(error_tot), " error / ", str(warn_tot), " warn"])
                if not self.asked_2_quit:
                    elapsed_time = int(time.time() - dirjob_tstart)
                    elapsed_min = elapsed_time // 60
                    elapsed_sec = elapsed_time % 60
                    if elapsed_min > 0 :
                        msg = "".join(["Police job terminated with ok code in ", str(elapsed_min), " min ", str(elapsed_sec), " sec"])
                    else:
                        msg = "".join(["Police job terminated with ok code in ", str(elapsed_sec), " sec"])

                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                        u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                else:
                    msg = "".join(["Job terminated by user !"])
                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info("\n", u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info("\n", u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                # there is no .epub files
                tk.messagebox.showinfo("Répertoire d'entrée \n", "Il n'y a pas de fichiers .epub dans ce répertoire. \nRefaites votre choix", icon='info')

        # rétablir l'état normal des boutons'
        u.manage_buttons("btnDirJob", "out")

    def file_change_police(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier auquel il faut adapter la police",
                                                     initialdir=self.new_js_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            # self.in_file_name = os.path.basename(in_path_file_name)
            self.change_police(in_path_file_name)  # start the optimisation
        else:
            self.msg_list.insert(tk.END, "Sélectionnez le fichier auquel il faut adapter la police")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")

    def change_police(self, in_path_file_name):
        """
            This function add nav buttons in the selected Epub
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        if len(in_path_file_name) != 0:

            # create the out_file_name with the in_file_name
            if "_pol" not in in_path_file_name:
                out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_pol.epub")
            else:
                out_file_name = os.path.basename(in_path_file_name)

            # the out filename goes in the wnav directory
            out_path_file_name = "".join([self.new_police_path, out_file_name])
            # prepare the text to display in and out files
            txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
            txt_out_file = "".join(["Dst file : ", out_path_file_name])

            # display the files status
            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["Change police : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
            u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(in_path_file_name, "r") as z:
                z.extractall(temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, ops_dir = u.get_ops_dir(temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
            css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
            js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
            font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])

            f_ok = True
            t_start = time.time()  # store the start time
            u.manage_info("... changement de la police en cours ... patientez SVP ...", u.DISPLAY_AND_LOG)

            # changer le nom de la police dans tous les fichiers css
            for file in os.listdir(css_path_dir):
                working_file="".join([css_path_dir, file])
                u.manage_info(file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                with open(working_file, "r", encoding="utf-8") as css_file:
                    css_data = css_file.readlines()
                with open(working_file, "w", encoding="utf-8") as new_css_file:
                    for l in css_data:
                        if "font-family" in l and "/*" not in l:
                            new_css_file.writelines("".join(["    font-family: ", self.FONT_NAME, "\n"]))
                        else:
                            new_css_file.writelines(l)

            # adapter tous les fichiers texte pour que les boutons reprennent la police choisie (par le exercises.css
            for file in os.listdir(text_path_dir):
                working_file="".join([text_path_dir, file])
                u.manage_info(file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                with open(working_file, "r", encoding="utf-8") as xhtml_file:
                    xhtml_data = xhtml_file.readlines()
                with open(working_file, "w", encoding="utf-8") as new_xhtml_file:
                    for l in xhtml_data:
                        new_xhtml_file.writelines(l.replace("<button style=\"margin-top:15px\"", "<button class=\"exercise_button\" style=\"margin-top:15px\""))


            # FINAL TASKS
            # ===================
            # creating the zipped epub file
            msg = "... creating the final zipped epub file"
            u.manage_info(msg, u.DISPLAY_AND_LOG)
            u.zip_epub(temp_path_dir, out_path_file_name)

            if u.WITH_ZIP:
                # create also the zip file
                u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))

            if u.WITH_DIR:
                # and also the directory with all the epub files
                out_dir_name = out_path_file_name.replace(".epub", "")

                # if exist delete the directory
                if os.path.exists(out_dir_name):
                    shutil.rmtree(out_dir_name, ignore_errors=True)
                # create the new dir
                shutil.copytree(temp_path_dir, out_dir_name)
                os.chdir(self.cwd)

            # info that all its finished and deleting temporary files and directories
            u.manage_info("... putzing", u.DISPLAY_AND_LOG)
            # remove temporary files and directories
            if os.path.exists(temp_path_dir):
                v_return = u.empty_dir(temp_path_dir)
                if v_return != "":
                    v_msg = "".join([self.log_path_file_name, v_return])
                    u.write_in_logfile(v_msg)
                f_msg = "function new_job, final tasks : remove temp dir"
                try:
                    os.rmdir(temp_path_dir)
                except:
                    try:
                        time.sleep(self.ERROR_WAIT_TIME)
                        self.second_try += 1
                        u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                        u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                        os.rmdir(temp_path_dir)
                    except:
                        u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

            elapsed_time = time.time() - t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Adaptation de la police dans le fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(in_path_file_name)])
                u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !\n"])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                msg_info = "".join(
                    ["Traitements des erreurs"])
                u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            # no file selected so do nothing
            u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
            u.manage_info("Select a epub to verify", u.DISPLAY_ONLY, u.COLOR_BLUE)
        return out_path_file_name

    def dir_prepare_for_moodle(self):

        """
        Cette fonction permet de vérifier tous les epub's contenus dans un répertoire
        Elle parcoure le répertoire choisi, vérifie qu'il y ait bien des fichiers epub puis,
        pour chaque ficheir epub, elle appelle la fonction file_job pour exécuter l'amélioration de façon individelle
        """
        # variable qui permet de savoir si l'utilisateur a demandé à interrompre la procédure
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # disable all buttons that can not be used during this task
        u.manage_buttons("btnDirJob", "in")
        self.asked_2_quit = False

        dirjob_tstart = time.time()
        # variable pour que la fonction sache que l'appel vient d'ici et gère les messages en conséquence
        self.dir_job_status = True
        # demande le nom du répertoire à travailler
        file_options = {}
        file_options['initialdir'] = self.new_nav_path #self.org_path
        file_options['title'] = 'Please select a directory with epub(s)'
        dir_name = filedialog.askdirectory(**file_options)

        file_output_result_path_name = "".join([self.log_path, "epub_check_result.txt"])
        with open(file_output_result_path_name, "w", encoding="utf-8") as prob_file:
            prob_file.write(str(datetime.now()))

        # erreurs totales
        fatal_tot = 0
        error_tot = 0
        warn_tot = 0
        recap_tot = []

        # On controle que le répertoire n'est pas vide
        if dir_name != "":
            # only the .epub files
            only_epub_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                               and os.path.splitext(f)[1] == ".epub"]
            if len(only_epub_files) > 0:
                # there is .epub files
                for test_file in only_epub_files:
                    t_start = time.time()
                    in_path_file_name = "/".join([dir_name, test_file])
                    in_file_name = os.path.basename(in_path_file_name)
                    out_path_file_name = self.prepare_for_moodle(in_path_file_name)

                    if self.VERIF_EPUB:
                        u.manage_info("---------------------------------------------------------", u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Préparation pour moodle : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Fichier : ", os.path.basename(in_file_name)]), u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        u.manage_info("en cours de vérification. Patientez SVP ...", u.DISPLAY_AND_LOG, u.COLOR_PURPLE)

                        ret_status, n_fatal, n_error,  n_warn = u.check_epub(out_path_file_name, file_output_result_path_name)
                        fatal_tot += n_fatal
                        error_tot += n_error
                        warn_tot += n_warn
                        recap_tot.append("".join([test_file, " : ",str(n_fatal), " fatals / ", str(n_error), " errors / ", str(n_warn), " warnings\n"]))

                        u.manage_info(ret_status, u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        msg = " "
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                        if self.asked_2_quit:
                            break
                        else:
                            time.sleep(u.pause_time)
                msg_err = "".join(["Check status total : ", str(fatal_tot), " fatal / ", str(error_tot), " error / ", str(warn_tot), " warn"])
                if not self.asked_2_quit:
                    elapsed_time = int(time.time() - dirjob_tstart)
                    elapsed_min = elapsed_time // 60
                    elapsed_sec = elapsed_time % 60
                    if elapsed_min > 0 :
                        msg = "".join(["Police job terminated with ok code in ", str(elapsed_min), " min ", str(elapsed_sec), " sec"])
                    else:
                        msg = "".join(["Police job terminated with ok code in ", str(elapsed_sec), " sec"])

                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                        u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                else:
                    msg = "".join(["Job terminated by user !"])
                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info("\n", u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info("\n", u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                # there is no .epub files
                tk.messagebox.showinfo("Répertoire d'entrée \n", "Il n'y a pas de fichiers .epub dans ce répertoire. \nRefaites votre choix", icon='info')

        # rétablir l'état normal des boutons'
        u.manage_buttons("btnDirJob", "out")

    def file_prepare_for_moodle(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez à préparer pour moodle",
                                                     initialdir=self.new_nav_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            in_file_name = os.path.basename(in_path_file_name)
            self.prepare_for_moodle(in_path_file_name)  # start the optimisation
        else:
            self.msg_list.insert(tk.END, "Select a epub to improve")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")


    def prepare_for_moodle(self, in_path_file_name):
        """
            This function add nav buttons in the selected Epub
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        if len(in_path_file_name) != 0:

            # create the out_file_name with the in_file_name
            if "_moo" not in in_path_file_name:
                out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_moo.epub")
            else:
                out_file_name = os.path.basename(in_path_file_name)

            # the out filename goes in the wnav directory
            out_path_file_name = "".join([self.new_moo_path, out_file_name])
            # prepare the text to display in and out files
            txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
            txt_out_file = "".join(["Dst file : ", out_path_file_name])

            # display the files status
            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["Prepare for moodle : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
            u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(in_path_file_name, "r") as z:
                z.extractall(temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, ops_dir = u.get_ops_dir(temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
            css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
            js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
            font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])

            f_ok = True
            t_start = time.time()  # store the start time
            u.manage_info("... changement de la police en cours ... patientez SVP ...", u.DISPLAY_AND_LOG)

            # intégrer les scripts dans les pages xhtml pour moodle
            # pour tous les fichiers xhtml
            for file in os.listdir(text_path_dir):
                u.manage_info(file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                working_file="".join([text_path_dir, file])
                with open(working_file, "r", encoding="utf-8") as xhtml_file:
                    xhtml_data = xhtml_file.readlines()
                with open(working_file, "w", encoding="utf-8") as new_xhtml_file:
                    in_body = False
                    script_found = False

                    for l in xhtml_data:
                        if "<body>" in l:
                            in_body = True
                        if "</script>" in l and in_body:
                            script_found = True
                            # new_xhtml_file.writelines("</script>\n\n")
                            # new_xhtml_file.writelines("<script>\n")
                            for js_in_file in os.listdir(js_path_dir):
                                js_Path_file_name ="".join([js_path_dir, js_in_file])
                                # if "alternateur" in js_in_file or "cercle" in js_in_file or "oscillo" in js_in_file or "validation" in js_in_file or "rendement" in js_in_file or "jquery" in js_in_file:
                                # read the script data
                                with open(js_Path_file_name, "r", encoding="utf-8") as js_file:
                                    js_data = js_file.readlines()
                                # write the script data in the xhtml file just before the </body> tag
                                new_xhtml_file.writelines("//<![CDATA[\n")
                                # new_xhtml_file.writelines("<script> //<![CDATA[")
                                for l_j in js_data:
                                    new_xhtml_file.writelines(l_j)
                                new_xhtml_file.writelines("//]]>\n")
                                # new_xhtml_file.writelines("//]]></script>")
                            new_xhtml_file.writelines(l)
                        else:
                            new_xhtml_file.writelines(l)
                        if "</body>" in l:

                            in_body = False

            # adapter tous les fichiers texte pour que les boutons reprennent la police choisie (par le exercises.css
            for file in os.listdir(text_path_dir):
                working_file="".join([text_path_dir, file])
                with open(working_file, "r", encoding="utf-8") as xhtml_file:
                    xhtml_data = xhtml_file.readlines()
                with open(working_file, "w", encoding="utf-8") as new_xhtml_file:
                    for l in xhtml_data:
                        new_xhtml_file.writelines(l.replace("<button style=\"margin-top:15px\"", "<button class=\"exercise_button\" style=\"margin-top:15px\""))


            # FINAL TASKS
            # ===================
            # creating the zipped epub file
            msg = "... creating the final zipped epub file"
            u.manage_info(msg, u.DISPLAY_AND_LOG)
            u.zip_epub(temp_path_dir, out_path_file_name)

            if u.WITH_ZIP:
                # create also the zip file
                u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))

            if u.WITH_DIR:
                # and also the directory with all the epub files
                out_dir_name = out_path_file_name.replace(".epub", "")

                # if exist delete the directory
                if os.path.exists(out_dir_name):
                    shutil.rmtree(out_dir_name, ignore_errors=True)
                # create the new dir
                shutil.copytree(temp_path_dir, out_dir_name)
                os.chdir(self.cwd)

            # info that all its finished and deleting temporary files and directories
            u.manage_info("... putzing", u.DISPLAY_AND_LOG)
            # remove temporary files and directories
            if os.path.exists(temp_path_dir):
                v_return = u.empty_dir(temp_path_dir)
                if v_return != "":
                    v_msg = "".join([self.log_path_file_name, v_return])
                    u.write_in_logfile(v_msg)
                f_msg = "function new_job, final tasks : remove temp dir"
                try:
                    os.rmdir(temp_path_dir)
                except:
                    try:
                        time.sleep(self.ERROR_WAIT_TIME)
                        self.second_try += 1
                        u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                        u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                        os.rmdir(temp_path_dir)
                    except:
                        u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

            elapsed_time = time.time() - t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Préparation pour moodle du fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(in_path_file_name)])
                u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !\n"])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                msg_info = "".join(
                    ["Traitements des erreurs"])
                u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            # no file selected so do nothing
            u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
            u.manage_info("Select a epub to verify", u.DISPLAY_ONLY, u.COLOR_BLUE)
        return out_path_file_name


    def dir_add_nav_btn(self):

        """
        Cette fonction permet de vérifier tous les epub's contenus dans un répertoire
        Elle parcoure le répertoire choisi, vérifie qu'il y ait bien des fichiers epub puis,
        pour chaque ficheir epub, elle appelle la fonction file_job pour exécuter l'amélioration de façon individelle
        """
        # variable qui permet de savoir si l'utilisateur a demandé à interrompre la procédure
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # disable all buttons that can not be used during this task
        u.manage_buttons("btnDirJob", "in")
        self.asked_2_quit = False

        dirjob_tstart = time.time()
        # variable pour que la fonction sache que l'appel vient d'ici et gère les messages en conséquence
        self.dir_job_status = True
        # demande le nom du répertoire à travailler
        file_options = {}
        file_options['initialdir'] = self.new_police_path #self.org_path
        file_options['title'] = 'Select a directory with epub files'
        dir_name = filedialog.askdirectory(**file_options)

        file_output_result_path_name = "".join([self.log_path, "epub_check_result.txt"])
        with open(file_output_result_path_name, "w", encoding="utf-8") as prob_file:
            prob_file.write(str(datetime.now()))

        # erreurs totales
        fatal_tot = 0
        error_tot = 0
        warn_tot = 0
        recap_tot = []

        # On controle que le répertoire n'est pas vide
        if dir_name != "":
            # only the .epub files
            only_epub_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                               and os.path.splitext(f)[1] == ".epub"]
            if len(only_epub_files) > 0:
                # there is .epub files
                for test_file in only_epub_files:
                    t_start = time.time()
                    in_path_file_name = "/".join([dir_name, test_file])
                    in_file_name = os.path.basename(in_path_file_name)
                    out_path_file_name = self.add_nav_btn(in_path_file_name)

                    if self.VERIF_EPUB:
                        u.manage_info("---------------------------------------------------------", u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["VERIFICATION EPUB : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.LOG_ONLY, u.COLOR_PURPLE)
                        u.manage_info("".join(["Fichier : ", os.path.basename(in_file_name)]), u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        u.manage_info("en cours de vérification. Patientez SVP ...", u.DISPLAY_AND_LOG, u.COLOR_PURPLE)

                        ret_status, n_fatal, n_error,  n_warn = u.check_epub(out_path_file_name, file_output_result_path_name)
                        fatal_tot += n_fatal
                        error_tot += n_error
                        warn_tot += n_warn
                        recap_tot.append("".join([test_file, " : ",str(n_fatal), " fatals / ", str(n_error), " errors / ", str(n_warn), " warnings\n"]))

                        u.manage_info(ret_status, u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                        msg = " "
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                        if self.asked_2_quit:
                            break
                        else:
                            time.sleep(u.pause_time)
                msg_err = "".join(["Check status total : ", str(fatal_tot), " fatal / ", str(error_tot), " error / ", str(warn_tot), " warn"])
                if not self.asked_2_quit:
                    elapsed_time = int(time.time() - dirjob_tstart)
                    elapsed_min = elapsed_time // 60
                    elapsed_sec = elapsed_time % 60
                    if elapsed_min > 0 :
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_min), " min ", str(elapsed_sec), " sec"])
                    else:
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_sec), " sec"])

                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                        u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                        u.manage_info(msg, u.DISPLAY_AND_LOG)
                else:
                    msg = "".join(["Job terminated by user !"])
                    if self.VERIF_EPUB:
                        for r in recap_tot:
                            u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                # there is no .epub files
                tk.messagebox.showinfo("Répertoire d'entrée \n", "Il n'y a pas de fichiers .epub dans ce répertoire. \nRefaites votre choix", icon='info')

        # rétablir l'état normal des boutons'
        u.manage_buttons("btnDirJob", "out")

    def file_add_nav_btn(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier auquel il faut ajouter la barre de navigation",
                                                     initialdir=self.new_police_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            in_file_name = os.path.basename(in_path_file_name)
            self.add_nav_btn(in_path_file_name)  # start the optimisation
        else:
            self.msg_list.insert(tk.END, "Sélectionnez le fichier auquel il faut ajouter la barre de navigation")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")


    def add_nav_btn(self, in_path_file_name):
        """
            This function add nav buttons in the selected Epub
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        if len(in_path_file_name) != 0:

            # create the out_file_name with the in_file_name
            if "_wnav" not in in_path_file_name:
                out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_wnav.epub")
            else:
                out_file_name = os.path.basename(in_path_file_name)

            # the out filename goes in the wnav directory
            out_path_file_name = "".join([self.new_nav_path, out_file_name])
            # prepare the text to display in and out files
            txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
            txt_out_file = "".join(["Dst file : ", out_path_file_name])

            # display the files status
            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["Add nav btn : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
            u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(in_path_file_name, "r") as z:
                z.extractall(temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, ops_dir = u.get_ops_dir(temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
            css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
            js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
            font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])

            f_ok = True
            t_start = time.time()  # store the start time
            u.manage_info("... ajout des boutons de navigation en cours . Patientez SVP ...", u.DISPLAY_AND_LOG)

            # open opf file and read <spine> elements
            v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
            if v_return != "":
                u.manage_info(v_return, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            else:
                # verif si nav.xhtml est dans la Spine si non l'ajouter
                nav_found = False
                for v_file in spine_list:
                    if v_file == "nav.xhtml":
                        nav_found = True
                        break
                if not nav_found:
                    with open(ops_path_filename, "r", encoding="utf-8") as opf_file:
                        opf_data = opf_file.readlines()
                        index = 0
                        break_ok = False
                    for line in opf_data:
                        if "</spine>" in line:
                            index_pos_for_nav = index
                        index += 1
                    opf_data.insert(index_pos_for_nav , "<itemref idref=\"nav.xhtml\"/>\n")

                    with open(ops_path_filename, "w", encoding="utf-8") as opf_file:
                        for line in opf_data:
                            opf_file.writelines(line)
                    v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)

                # remove files nav_bar(...).js and nav_bar(...).css if exists
                for r, d, f in os.walk(css_path_dir):
                    for css_file in f:
                        if "nav_bar" in css_file:
                            os.remove("".join([css_path_dir, css_file]))
                for r, d, f in os.walk(js_path_dir):
                    for js_file in f:
                        if "nav_bar" in js_file:
                            os.remove("".join([js_path_dir, js_file]))

                # import updated files nav_bar(...).js and nav_bar(...).css in the epub
                css_nav_bar_file_name = ""
                js_nav_bar_file_name = ""
                txt2add = ""

                for r, d, f in os.walk(self.js_css_path):
                    for jscss_file in f:
                        if  "nav_bar" in jscss_file:
                            sce = "".join([self.js_css_path, jscss_file])
                            if jscss_file.split(".")[1] == "js":
                                dst = "".join([js_path_dir, jscss_file])
                                js_nav_bar_file_name = jscss_file
                                txt2add = "<item id='" + jscss_file + "' href='Misc/" + jscss_file + "' media-type='text/javascript'/>\n"
                            elif jscss_file.split(".")[1] == "css":
                                dst = "".join([css_path_dir, jscss_file])
                                css_nav_bar_file_name = jscss_file
                                txt2add = "<item id='" + jscss_file + "' href='Styles/" + jscss_file + "' media-type='text/css'/>\n"
                            shutil.copy2(sce, dst)
                            # add ref in content.opf
                            with open(ops_path_filename, "r", encoding="utf-8") as rFile:
                                data = rFile.readlines()
                            i = 0
                            for l in data:
                                if "</manifest>" in l:
                                    index = i
                                i += 1
                            data.insert(index, txt2add)
                            with open(ops_path_filename, "w", encoding="utf-8") as wFile:
                                wFile.writelines(data)




                # pour tous les fichiers xhtml inclus dans la Spine_list
                for current_page_number in range(len(spine_list)):
                    u.manage_info(spine_list[current_page_number], u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                    working_file = "".join([text_path_dir, spine_list[current_page_number]])

                    # read the file
                    with open(working_file, "r", encoding="utf-8") as rFile:
                        data = rFile.readlines()

                    # add nav references for .js and .css in all xhtml files
                    i = 0
                    for l in data:
                        if "</head>" in l:
                            data.insert(i, self.get_nav_bar_js_string(js_nav_bar_file_name))
                            data.insert(i, self.get_nav_bar_css_string(css_nav_bar_file_name))
                            break
                        i += 1

                    # add property scripted
                    with open(ops_path_filename, "r", encoding="utf-8") as opfFile:
                        opf_data = opfFile.readlines()
                    new_data = []
                    for this_line in opf_data:
                        if "<item " in this_line and spine_list[current_page_number] in this_line:
                            txt_2_search = "properties=\""
                            pos_start_properties = this_line.find(txt_2_search)
                            if pos_start_properties != -1:
                                pos_start_properties += len(txt_2_search)
                                pos_end_properties = this_line.find("\"/>", pos_start_properties)
                                properties_val = this_line[pos_start_properties:pos_end_properties]
                                if "scripted" not in properties_val:
                                    this_line = this_line[:pos_start_properties] + "scripted " + this_line[pos_start_properties:]
                            else:
                                pos_start_properties = this_line.find("/>")
                                this_line = this_line[:pos_start_properties] + " properties=\"scripted\"" + this_line[pos_start_properties:]
                        new_data.append(this_line)
                    with open(ops_path_filename, "w", encoding="utf-8") as new_file:
                        new_file.writelines(new_data)

                    # if btn bars exist, remove it
                    top_moodle_nav_div_begin_found = False
                    top_moodle_nav_div_end_found = False
                    break_ok = False
                    index_start_string_nav_div = 0
                    index_end_string_nav_div = 0

                    for x in range(len(data)):
                        if top_moodle_nav_div_begin_found and self.get_div_end_string() in data[x]:
                            top_moodle_nav_div_end_found = True
                            index_end_string_nav_div = x + 1
                        if top_moodle_nav_div_begin_found and top_moodle_nav_div_end_found:
                            del data[index_start_string_nav_div:index_end_string_nav_div]
                            top_moodle_nav_div_begin_found = False
                            top_moodle_nav_div_end_found = False
                            break_ok = True
                        if break_ok:
                            break

                    st1 = self.get_top_div_begin_string()
                    st2 = ""
                    st3 = ""
                    st4 = ""
                    st5 = ""
                    st6 = self.get_br_string()
                    st7 = self.get_div_end_string()
                    st8 = "" # self.get_br_string()

                    if current_page_number != len(spine_list)-1 and current_page_number != 0:
                        st2 = self.get_moodle_home_page_string()
                        st3 = self.get_menu_btn_nav_string()
                        st4 = self.get_previous_btn_nav_string().replace("previous_page_name", spine_list[current_page_number-1])
                        st5 = self.get_next_btn_nav_string().replace("next_page_name", spine_list[current_page_number+1])

                    if current_page_number == len(spine_list)-1: # dernière page
                        st2 = self.get_moodle_home_page_string()
                        st3 = self.get_menu_btn_nav_string()
                        st4 = self.get_previous_btn_nav_string().replace("previous_page_name", spine_list[current_page_number-1])

                    if current_page_number == 0: # première page
                        st2 = self.get_moodle_home_page_string()
                        st3 = self.get_menu_btn_nav_string()
                        st5 = self.get_next_btn_nav_string().replace("next_page_name", spine_list[current_page_number+1])

                    top_str = "".join([st1, st2, st3, st4, st5, st6, st7, st8])

                    # insert top btn
                    for x in range(len(data)):
                        if "<body" in data[x]:
                            data.insert(x + 1, top_str)
                            break

                    with open(working_file, "w", encoding="utf-8") as wFile:
                        wFile.writelines(data)

                # FINAL TASKS
                # ===================

                # update all js and css ref
                self.update_js_and_css_heart(ops_path_filename, js_path_dir, css_path_dir, text_path_dir)

                # beautify the epub en attente car pas terminé manque la reprise correcte du code javascript
                u.manage_info("pretifying the xhtml", u.LOG_ONLY, u.COLOR_PURPLE)
                y.pretify_xhtml(text_path_dir)

                # add <br/> at the end of <body>
                u.manage_info("adding <br/> at the end of each body section", u.LOG_ONLY, u.COLOR_PURPLE)
                y.add_br(text_path_dir)

                # creating the zipped epub file
                msg = "... creating the final zipped epub file"
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                u.zip_epub(temp_path_dir, out_path_file_name)

                if u.WITH_ZIP:
                    # create also the zip file
                    u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))

                if u.WITH_DIR:
                    # and also the directory with all the epub files
                    out_dir_name = out_path_file_name.replace(".epub", "")

                    # if exist delete the directory
                    if os.path.exists(out_dir_name):
                        shutil.rmtree(out_dir_name, ignore_errors=True)
                    # create the new dir
                    shutil.copytree(temp_path_dir, out_dir_name)
                    os.chdir(self.cwd)

                # info that all its finished and deleting temporary files and directories
                u.manage_info("... putzing", u.DISPLAY_AND_LOG)
                # remove temporary files and directories
                if os.path.exists(temp_path_dir):
                    v_return = u.empty_dir(temp_path_dir)
                    if v_return != "":
                        v_msg = "".join([self.log_path_file_name, v_return])
                        u.write_in_logfile(v_msg)
                    f_msg = "function new_job, final tasks : remove temp dir"
                    try:
                        os.rmdir(temp_path_dir)
                    except:
                        try:
                            time.sleep(self.ERROR_WAIT_TIME)
                            self.second_try += 1
                            u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                            u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                            os.rmdir(temp_path_dir)
                        except:
                            u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

            elapsed_time = time.time() - t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Ajout des boutons de navigation dans le fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(in_path_file_name)])
                u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !\n"])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                msg_info = "".join(
                    ["Traitements des erreurs"])
                u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            # no file selected so do nothing
            u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
            u.manage_info("Opération abandonnée", u.DISPLAY_ONLY, u.COLOR_BLUE)

        return out_path_file_name

    def file_remove_nav_btn(self):
        # clear the listbox
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        in_path_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier auquel il faut retirer la barre de navigations",
                                                     initialdir=self.new_nav_path,
                                                     filetypes=[('epub files', '.epub'), ('all files', '.*')])

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnAddNav", "in")

        if len(str(in_path_file_name)) > 0:
            t_start = time.time()  # store the start time
            # self.in_file_name = os.path.basename(in_path_file_name)
            self.remove_nav_btn(in_path_file_name)  # start the optimisation
        else:
            self.msg_list.insert(tk.END, "Select a epub to improve")
            self.msg_display.update()
        u.manage_buttons("btnAddNav", "out")


    def remove_nav_btn(self, in_path_file_name):
        """
            This function add nav buttons in the selected Epub
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)

        if len(in_path_file_name) != 0:

            # create the out_file_name with the in_file_name
            if "_nonav" not in in_path_file_name:
                out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_nonav.epub")
            else:
                out_file_name = os.path.basename(in_path_file_name)

            # the out filename goes in the wnav directory
            out_path_file_name = "".join([self.new_nav_path, out_file_name])
            # prepare the text to display in and out files
            txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
            txt_out_file = "".join(["Dst file : ", out_path_file_name])

            # display the files status
            u.manage_info("", u.DISPLAY_AND_LOG)
            u.manage_info("".join(["Add nav btn : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
            u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(in_path_file_name, "r") as z:
                z.extractall(temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, ops_dir = u.get_ops_dir(temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
            css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
            js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
            font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])

            f_ok = True
            t_start = time.time()  # store the start time
            u.manage_info("... ajout des boutons de navigation en cours . Patientez SVP ...", u.DISPLAY_AND_LOG)

            # open opf file and read <spine> elements
            v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
            if v_return != "":
                u.manage_info(v_return, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
            else:

                # pour tous les fichiers inclus dans la Spine_list
                for current_page_number in range(len(spine_list)):

                    u.manage_info(spine_list[current_page_number], u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                    working_file = "".join([text_path_dir, spine_list[current_page_number]])
                    # remove all .js and .css references
                    # read the file
                    with open(working_file, "r", encoding="utf-8") as rFile:
                        data = rFile.readlines()

                    # if btn bars exist, remove it
                    top_moodle_nav_div_begin_found = False
                    top_moodle_nav_div_end_found = False
                    new_data = []

                    for l in data:
                        # print(l)
                        if self.get_top_div_begin_string() in l:
                            top_moodle_nav_div_begin_found = True

                        if not (top_moodle_nav_div_begin_found and not top_moodle_nav_div_end_found):
                            new_data.append(l)

                        if top_moodle_nav_div_begin_found and self.get_div_end_string() in l:
                            top_moodle_nav_div_end_found = True

                    with open(working_file, "w", encoding="utf-8") as wFile:
                        for l in new_data:
                            wFile.writelines(l)


                # FINAL TASKS
                # ===================
                # beautify the epub en attente car pas terminé manque la reprise correcte du code javascript
                u.manage_info("pretifying the xhtml", u.LOG_ONLY, u.COLOR_PURPLE)
                y.pretify_xhtml(text_path_dir)

                # add <br/> at the end of <body>
                u.manage_info("adding <br/> at the end of each body section", u.LOG_ONLY, u.COLOR_PURPLE)
                y.add_br(text_path_dir)

                # creating the zipped epub file
                msg = "... creating the final zipped epub file"
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                u.zip_epub(temp_path_dir, out_path_file_name)

                if u.WITH_ZIP:
                    # create also the zip file
                    u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))

                if u.WITH_DIR:
                    # and also the directory with all the epub files
                    out_dir_name = out_path_file_name.replace(".epub", "")

                    # if exist delete the directory
                    if os.path.exists(out_dir_name):
                        shutil.rmtree(out_dir_name, ignore_errors=True)
                    # create the new dir
                    shutil.copytree(temp_path_dir, out_dir_name)
                    os.chdir(self.cwd)

                # info that all its finished and deleting temporary files and directories
                u.manage_info("... putzing", u.DISPLAY_AND_LOG)
                # remove temporary files and directories
                if os.path.exists(temp_path_dir):
                    v_return = u.empty_dir(temp_path_dir)
                    if v_return != "":
                        v_msg = "".join([self.log_path_file_name, v_return])
                        u.write_in_logfile(v_msg)
                    f_msg = "function new_job, final tasks : remove temp dir"
                    try:
                        os.rmdir(temp_path_dir)
                    except:
                        try:
                            time.sleep(self.ERROR_WAIT_TIME)
                            self.second_try += 1
                            u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                            u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                            os.rmdir(temp_path_dir)
                        except:
                            u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

                ##-------------------------------------------------------------------------------------------------
                ## fin ajout des boutons dans les fichiers de la spine_list
                ##-------------------------------------------------------------------------------------------------

            elapsed_time = time.time() - t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Retrait des boutons de navigation dans le fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(os.path.basename(in_path_file_name))])
                u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
                msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !"])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                msg_info = "".join(
                    ["Traitements des erreurs"])
                u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
        else:
            # no file selected so do nothing
            u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
            u.manage_info("Select a epub", u.DISPLAY_ONLY, u.COLOR_BLUE)

    def dir_verify_epub(self):

        """
        Cette fonction permet de vérifier tous les epub's contenus dans un répertoire
        Elle parcoure le répertoire choisi, vérifie qu'il y ait bien des fichiers epub puis,
        pour chaque ficheir epub, elle appelle la fonction file_job pour exécuter l'amélioration de façon individelle
        """
        # variable qui permet de savoir si l'utilisateur a demandé à interrompre la procédure
        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()
        # disable all buttons that can not be used during this task
        u.manage_buttons("btnDirJob", "in")
        self.asked_2_quit = False

        dirjob_tstart = time.time()
        # variable pour que la fonction sache que l'appel vient d'ici et gère les messages en conséquence
        self.dir_job_status = True
        # demande le nom du répertoire à travailler
        file_options = {}
        file_options['initialdir'] = self.new_path #self.org_path
        file_options['title'] = 'Select a directory with epub files to verify'
        dir_name = filedialog.askdirectory(**file_options)

        file_output_result_path_name = "".join([self.log_path, "epub_check_result.txt"])
        with open(file_output_result_path_name, "w", encoding="utf-8") as prob_file:
            prob_file.write(str(datetime.now()))

        # erreurs totales
        fatal_tot = 0
        error_tot = 0
        warn_tot = 0
        recap_tot = []

        # On controle que le répertoire n'est pas vide
        if dir_name != "":
            # only the .epub files
            only_epub_files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))
                               and os.path.splitext(f)[1] == ".epub"]
            if len(only_epub_files) > 0:
                # there is .epub files
                for test_file in only_epub_files:
                    t_start = time.time()
                    in_path_file_name = "/".join([dir_name, test_file])
                    in_file_name = os.path.basename(in_path_file_name)

                    u.manage_info("---------------------------------------------------------", u.LOG_ONLY, u.COLOR_PURPLE)
                    u.manage_info("".join(["VERIFICATION EPUB : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.LOG_ONLY, u.COLOR_PURPLE)
                    u.manage_info("".join(["Fichier : ", os.path.basename(in_file_name)]), u.DISPLAY_AND_LOG, u.COLOR_BLACK)
                    u.manage_info("en cours de vérification. Patientez SVP ...", u.DISPLAY_AND_LOG, u.COLOR_PURPLE)

                    ret_status, n_fatal, n_error,  n_warn = u.check_epub(in_path_file_name, file_output_result_path_name)
                    fatal_tot += n_fatal
                    error_tot += n_error
                    warn_tot += n_warn
                    recap_tot.append("".join([test_file, " : ",str(n_fatal), " fatals / ", str(n_error), " errors / ", str(n_warn), " warnings\n"]))

                    u.manage_info(ret_status, u.DISPLAY_AND_LOG, u.COLOR_PURPLE)
                    msg = " "
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
                    if self.asked_2_quit:
                        break
                    else:
                        time.sleep(u.pause_time)
                msg_err = "".join(["Check status total : ", str(fatal_tot), " fatal / ", str(error_tot), " error / ", str(warn_tot), " warn"])
                if not self.asked_2_quit:
                    elapsed_time = int(time.time() - dirjob_tstart)
                    elapsed_min = elapsed_time // 60
                    elapsed_sec = elapsed_time % 60
                    if elapsed_min > 0 :
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_min), " min ", str(elapsed_sec), " sec"])
                    else:
                        msg = "".join(["DIR job terminated with ok code in ", str(elapsed_sec), " sec"])

                    for r in recap_tot:
                        u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
                else:
                    msg = "".join(["Job terminated by user !"])
                    for r in recap_tot:
                        u.manage_info(r, u.DISPLAY_AND_LOG)
                    u.manage_info(msg_err, u.DISPLAY_AND_LOG)
                    u.manage_info(msg, u.DISPLAY_AND_LOG)
            else:
                # there is no .epub files
                tk.messagebox.showinfo("Répertoire d'entrée \n", "Il n'y a pas de fichiers .epub dans ce répertoire. \nRefaites votre choix", icon='info')

        # rétablir l'état normal des boutons'
        u.manage_buttons("btnDirJob", "out")


    #===============================================================================================================
    # btn nav strings
    #===============================================================================================================

    def get_top_div_begin_string(self):
        if self.pos_nav_bar == "TOP":
            return "<div class=\"navbar-ul-top w3-bar w3-dark-gray\" id=\"topMoodleNavBarId\">\n"
        elif self.pos_nav_bar == "BOTTOM":
            return "<div class=\"navbar-ul-bottom w3-bar w3-dark-gray\" id=\"topMoodleNavBarId\">\n"
        else:
            return "<div class=\"navbar-ul w3-bar w3-dark-gray\" id=\"moodleNavBarId\">\n"

    def get_bottom_div_begin_string(self):
        return "<div class=\"w3-bar w3-dark-gray\" id=\"bottomMoodleNavBarId\">\n"

    def get_div_end_string(self):
        return "</div>\n"

    def get_br_string(self):
        return "<br/>\n"

    def get_previous_btn_nav_string(self):
        previous_btn_str = "".join([\
            "<a href=\"previous_page_name\" class=\"w3-bar-item w3-button w3-padding-small\" style=\"font-size:", \
            self.menu_bar_font_size, \
            "\"> Précédente </a>\n"])
        return previous_btn_str

    def get_next_btn_nav_string(self):
        next_btn_str = "".join([\
            "<a href=\"next_page_name\" class=\"w3-bar-item w3-button w3-padding-small\" style=\"font-size:", \
            self.menu_bar_font_size, \
            "\"> Suivante </a>\n"])
        return next_btn_str

    def get_menu_btn_nav_string(self):
        menu_btn_str = "".join([\
            "<a href=\"nav.xhtml\" class=\"w3-bar-item w3-button w3-padding-small\" style=\"font-size:",\
            self.menu_bar_font_size,\
            "\"> Menu </a>\n"])
        return menu_btn_str
        # return "<a href=\"nav.xhtml\" class=\"w3-bar-item w3-button w3-padding-small\" style=\"font-size:8px\"> Menu </a>\n"

    def get_moodle_home_page_string(self):
        moodle_btn_str = "".join([\
            "<a onclick=\"GoToMoodleHomePage()\" href=\"javascript:void(0)\"  class=\"w3-bar-item w3-button w3-padding-small\" style=\"font-size:",\
            self.menu_bar_font_size,\
            "\"> Moodle </a>\n"])
        return moodle_btn_str

    def get_link_css_string(self, css_file_path_name):
        return "".join(["<link href=\"../", css_file_path_name, "\" rel=\"stylesheet\" type=\"text/css\"/>"])

    def get_link_js_string(self, js_file_path_name):
        return "".join(["<script src=\"../", js_file_path_name, "\" type=\"text/javascript\"></script>"])

    def get_nav_bar_css_string(self, nav_bar_css_file_name):
        nav_bar_css_string = "".join(["<link href=\"../Styles/", nav_bar_css_file_name, "\" rel=\"stylesheet\" type=\"text/css\"/>"])
        return nav_bar_css_string

    def get_nav_bar_js_string(self, nav_bar_js_file_name):
        nav_bar_js_string = "".join(["<script src=\"../Misc/", nav_bar_js_file_name, "\" type=\"text/javascript\"></script>"])
        return nav_bar_js_string


    def read_spine_in_content_opf(self, v_path_file_name):
        """
            this function delete a line in a epub html file
            input :
                v_path_file_name : path and name of the file to modify
                v_tag : tag where the new line must be inserted
                new_txt : text to be inserted
        return : if ok : return an empty string
               : else : return a message
        """
        spine_list = []
        id_found = False
        spine_begin_found = False
        spine_end_found = False
        with open(v_path_file_name, "r", encoding="utf-8") as opfFile:
            data = opfFile.readlines()
            for l in data:
                if "</spine" in l:
                    spine_end_found = True
                if spine_begin_found and not spine_end_found:
                    beg_file_name = l.find("idref=\"")
                    end_file_name = l.find("\"", beg_file_name + 7)
                    file_id = l[beg_file_name + 7:end_file_name]
                    # print("".join(["FILE_ID : ", file_id]))
                    v_return, file_name = self.get_file_name_from_id(file_id, data)
                    # print(file_name)
                    spine_list.append(file_name)
                    id_found = True
                if "<spine" in l:
                    spine_begin_found = True
        if id_found:
            v_return = ""
        else:
            v_return = "".join(["WARNING : spine not found in ", v_path_file_name])
        return v_return, spine_list

    def get_file_name_from_id(self, file_id, opf_data):

        manifest_end_found = False
        manifest_begin_found = False
        file_name_found = False
        file_name = ""

        for l in opf_data:
            if "</manifest>" in l:
                manifest_end_found = True
            if manifest_begin_found and not manifest_end_found:
                if "." in file_id :
                    if l.find(file_id) != -1:
                        file_name_begin_pos = l.find("href=") + 11
                        file_name_end_pos = l.find("\"", file_name_begin_pos)
                        file_name = l[file_name_begin_pos: file_name_end_pos]
                        file_name_found = True
                else:
                    if l.find("".join([file_id, "."])) != -1:
                        file_name_begin_pos = l.find("href=") + 11
                        file_name_end_pos = l.find("\"", file_name_begin_pos)
                        file_name = l[file_name_begin_pos: file_name_end_pos]
                        file_name_found = True
            if "<manifest>" in l:
                manifest_begin_found = True

        if not file_name_found:
            return "".join(["WARNING : file name of  ", file_id, " not found"]), file_name
        else:
            return "", file_name

    def update_manifest_line(self, opf_file, file_type, epub_dir, dict_str, dict_file):

        with open(opf_file, "r", encoding="utf-8") as rFile:
            opf_data = rFile.readlines()
        new_opf_data = []

        # mise à jour opf pour les fichiers .js
        manifest_end_found = False
        manifest_begin_found = False
        for l in opf_data:
            if "</manifest>" in l:
                manifest_end_found = True
            if manifest_begin_found and not manifest_end_found:
                for jscss_string in dict_str:
                    if file_type in l and jscss_string in l and dict_str[jscss_string]:
                        i_beg_file_name = l.find(epub_dir) + len(epub_dir)
                        i_end_file_name = l.find(file_type, i_beg_file_name) + len(file_type)
                        old_file_name = l[i_beg_file_name:i_end_file_name]
                        l = l.replace(old_file_name,dict_file[jscss_string])
            if "<manifest>" in l:
                manifest_begin_found = True
            new_opf_data.append(l)

        with open(opf_file, "w", encoding="utf-8") as wFile:
            for l in new_opf_data:
                wFile.write(l)
        return ""

    #
    # def add_manifest_line(self, opf_file, line_to_add):
    #     with open(opf_file, "r", encoding="utf-8") as rFile:
    #         opf_data = rFile.readlines()
    #
    #     manifest_end_found = False
    #     manifest_begin_found = False
    #     index = 0;
    #     for l in opf_data:
    #         index += 1
    #         if "</manifest>" in l:
    #             manifest_end_found = True
    #         if manifest_begin_found and not manifest_end_found:
    #             line_to_add = "".join([line_to_add,"\n"])
    #             opf_data.insert(index, line_to_add)
    #             # for  ll in opf_data:print(ll)
    #             break
    #         if "<manifest>" in l:
    #             manifest_begin_found = True
    #
    #     with open(opf_file, "w", encoding="utf-8") as wFile:
    #         for l in opf_data:
    #             wFile.write(l)
    #     return ""
    #
    # def remove_manifest_line(self, opf_file, ext_to_remove):
    #
    #     with open(opf_file, "r", encoding="utf-8") as rFile:
    #         opf_data = rFile.readlines()
    #
    #     manifest_end_found = False
    #     manifest_begin_found = False
    #     index = 0;
    #     remove_list = []
    #     for l in opf_data:
    #         if "</manifest>" in l:
    #             manifest_end_found = True
    #         if manifest_begin_found and not manifest_end_found:
    #             if ext_to_remove in l:
    #                 remove_list.append(index)
    #         if "<manifest>" in l:
    #             manifest_begin_found = True
    #         index += 1
    #     # print(len(remove_list), " -- ", remove_list)
    #
    #     index = len(remove_list)
    #     while index > 0:
    #         i = 0
    #         for l in opf_data:
    #             if remove_list[index-1] == i:
    #                 # print(l)
    #                 opf_data.remove(l)
    #                 break
    #             i += 1
    #         index -= 1
    #     with open(opf_file, "w", encoding="utf-8") as wFile:
    #         for l in opf_data:
    #             wFile.write(l)
    #     return ""


    # def update_js_and_css_old(self, in_path_file_name):
    #     """
    #         This function add nav buttons in the selected Epub
    #         input : none
    #         return : none
    #     """
    #
    #     u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
    #
    #     if len(in_path_file_name) != 0:
    #
    #         # create the out_file_name with the in_file_name
    #         if "_js" not in in_path_file_name:
    #             out_file_name = os.path.basename(in_path_file_name).replace(".epub", "_js.epub")
    #         else:
    #             out_file_name = os.path.basename(in_path_file_name)
    #
    #         # the out filename goes in the wnav directory
    #         out_path_file_name = "".join([self.new_js_path, out_file_name])
    #         # prepare the text to display in and out files
    #         txt_in_file = "".join(["Sce file : ", os.path.basename(in_path_file_name)])
    #         txt_out_file = "".join(["Dst file : ", out_path_file_name])
    #
    #         # display the files status
    #         u.manage_info("", u.DISPLAY_AND_LOG)
    #         u.manage_info("".join(["Change .js and .css file with \"à jour\" files : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
    #         u.manage_info(txt_in_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
    #         u.manage_info(txt_out_file, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
    #         u.manage_info("", u.DISPLAY_AND_LOG)
    #
    #         # search for a "unique directory name" and create the temp directory
    #         temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
    #         os.mkdir(temp_path_dir)
    #
    #         # unzip all files from inFileName to the temp extractDir
    #         u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
    #         with zipfile.ZipFile(in_path_file_name, "r") as z:
    #             z.extractall(temp_path_dir)
    #
    #         # search for the name of the OPS directory (can be OEBPS or OPS)
    #         ok, ops_dir = u.get_ops_dir(temp_path_dir)
    #         if not ok:
    #             u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
    #         ops_path_filename = "".join([temp_path_dir, ops_dir, self.CONTENT_OPF_FILE_NAME])
    #
    #         # path of the text directory
    #         text_path_dir = "".join([temp_path_dir, ops_dir, "Text/"])
    #         css_path_dir = "".join([temp_path_dir, ops_dir, "Styles/"])
    #         js_path_dir = "".join([temp_path_dir, ops_dir, "Misc/"])
    #         font_path_dir = "".join([temp_path_dir, ops_dir, "Fonts/"])
    #
    #         f_ok = True
    #         t_start = time.time()  # store the start time
    #         u.manage_info("... remplacement des fichiers .js et .css en cours . Patientez SVP ...", u.DISPLAY_AND_LOG)
    #
    #     # rermplacer tous les fichiers .js et .css par la dernière version a jour
    #         #1 supprimer tous les fichiers .js et .css existants
    #         for r, d, f in os.walk(css_path_dir):
    #             for css_file in f:
    #                 os.remove("".join([css_path_dir, css_file]))
    #         for r, d, f in os.walk(js_path_dir):
    #             for js_file in f:
    #                 os.remove("".join([js_path_dir, js_file]))
    #
    #         #2 importer les versions à jour des .js et .css
    #         for r, d, f in os.walk(self.js_css_path):
    #             for jscss_file in f:
    #                 sce = "".join([self.js_css_path, jscss_file])
    #                 if jscss_file.split(".")[1] == "js":
    #                     dst = "".join([js_path_dir, jscss_file])
    #                 elif jscss_file.split(".")[1] == "css":
    #                     dst = "".join([css_path_dir, jscss_file])
    #                 shutil.copy2(sce, dst)
    #
    #         # open opf file and read <spine> elements
    #         v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
    #         if v_return != "":
    #             u.manage_info(v_return, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
    #         else:
    #             # verif si nav.xhtml est dans la Spine si non l'ajouter
    #             nav_found = False
    #             for v_file in spine_list:
    #                 if v_file == "nav.xhtml":
    #                     nav_found = True
    #                     break
    #             if not nav_found:
    #                 with open(ops_path_filename, "r", encoding="utf-8") as opf_file:
    #                     opf_data = opf_file.readlines()
    #                     index = 0
    #                     break_ok = False
    #                 for line in opf_data:
    #                     if "</spine>" in line:
    #                         index_pos_for_nav = index
    #                     index += 1
    #                 opf_data.insert(index_pos_for_nav , "<itemref idref=\"nav.xhtml\"/>\n")
    #
    #                 with open(ops_path_filename, "w", encoding="utf-8") as opf_file:
    #                     for line in opf_data:
    #                         opf_file.writelines(line)
    #                 v_return, spine_list = self.read_spine_in_content_opf(ops_path_filename)
    #
    #             # pour tous les fichiers inclus dans la Spine_list
    #             for current_page_number in range(len(spine_list)):
    #                 u.manage_info(spine_list[current_page_number], u.DISPLAY_AND_LOG, u.COLOR_BLUE)
    #                 working_file = "".join([text_path_dir, spine_list[current_page_number]])
    #                 data = []
    #                 data_new = []
    #                 # remove all .js ans .css references
    #                 # read the xhtml file
    #                 with open(working_file, "r", encoding="utf-8") as rFile:
    #                     data = rFile.readlines()
    #                 end_head_found = False
    #                 begin_tag_found = False
    #                 begin_head_found = False
    #
    #                 for l in data:
    #                     # if ("<script" in l or "<link" in l) :
    #                     #     script_or_link_in_l = True
    #                     # else:
    #                     #     script_or_link_in_l = False
    #                     # print("script_or_link_in_l ",script_or_link_in_l)
    #                     #
    #                     # if ("/>" in l or "</script>" in l) :
    #                     #     end_script = True
    #                     # else:
    #                     #     end_script = False
    #                     # print("end_script ",end_script)
    #                     #
    #                     # if ("/MathJax.js" in l) :
    #                     #     mathjax_in_l = True
    #                     # else:
    #                     #     mathjax_in_l = False
    #                     # print("mathjax_in_l ",mathjax_in_l)
    #                     # print ("ttestcond ", script_or_link_in_l and end_script and not mathjax_in_l)
    #                     to_remove = False
    #                     if "<head>" in l :
    #                         begin_head_found = True
    #                     if begin_head_found and not end_head_found:
    #                         if ("<script" in l or "<link" in l) and ("/>" in l or "</script>" in l) and not ("/MathJax.js" in l):
    #                             to_remove = True
    #                         if ("<script" in l or "<link" in l) and not ("/>" in l or "</script>" in l) and not ("/MathJax.js" in l):
    #                         # if ("<script" in l or "<link" in l) and "/>" not in l:
    #                             begin_tag_found = True
    #                             to_remove = True
    #                         if begin_tag_found and "</" in l:
    #                             begin_tag_found = False
    #                             to_remove = True
    #                         if begin_tag_found :
    #                             to_remove = True
    #                     if not to_remove:
    #                         data_new.append(l)
    #                     if "</head>" in l :
    #                         end_head_found = True
    #                 with open(working_file, "w", encoding="utf-8") as txt_file:
    #                     for l in data_new:
    #                         txt_file.writelines(l)
    #                 # add ref for all js and css files
    #                 txt_to_insert = ""
    #                 for r, d, f in os.walk(self.js_css_path):
    #                     for jscss_file in f:
    #                         if jscss_file.split(".")[1] == "js":
    #                             txt_to_insert = self.get_link_js_string("".join(["Misc/",jscss_file]))
    #                         elif jscss_file.split(".")[1] == "css":
    #                             txt_to_insert = self.get_link_css_string("".join(["Styles/",jscss_file]))
    #                         with open(working_file, "r", encoding="utf-8") as txt_file:
    #                             data = txt_file.readlines()
    #                         for x in range(len(data)):
    #                             if "</head>" in data[x]:
    #                                 data.insert(x, "".join([txt_to_insert, "\n"]))
    #                                 break
    #                         with open(working_file, "w", encoding="utf-8") as txt_file:
    #                             for l in data:
    #                                 txt_file.writelines(l)
    #                 # add property scripted
    #                 with open(ops_path_filename, "r", encoding="utf-8") as opfFile:
    #                     opf_data = opfFile.readlines()
    #                 new_data = []
    #                 for this_line in opf_data:
    #                     if "<item " in this_line and spine_list[current_page_number] in this_line:
    #                         txt_2_search = "properties=\""
    #                         pos_start_properties = this_line.find(txt_2_search)
    #                         if pos_start_properties != -1:
    #                             pos_start_properties += len(txt_2_search)
    #                             pos_end_properties = this_line.find("\"/>", pos_start_properties)
    #                             properties_val = this_line[pos_start_properties:pos_end_properties]
    #                             if "scripted" not in properties_val:
    #                                 this_line = this_line[:pos_start_properties] + "scripted " + this_line[pos_start_properties:]
    #                         else:
    #                             pos_start_properties = this_line.find("/>")
    #                             this_line = this_line[:pos_start_properties] + " properties=\"scripted\"" + this_line[pos_start_properties:]
    #                     new_data.append(this_line)
    #                 with open(ops_path_filename, "w", encoding="utf-8") as new_file:
    #                     new_file.writelines(new_data)
    #
    #                 # if btn bars exist, remove it
    #                 top_moodle_nav_div_begin_found = False
    #                 top_moodle_nav_div_end_found = False
    #                 break_ok = False
    #                 index_start_string_nav_div = 0
    #                 index_end_string_nav_div = 0
    #
    #                 for x in range(len(data)):
    #                     if top_moodle_nav_div_begin_found and self.get_div_end_string() in data[x]:
    #                         top_moodle_nav_div_end_found = True
    #                         index_end_string_nav_div = x + 1
    #                     if top_moodle_nav_div_begin_found and top_moodle_nav_div_end_found:
    #                         del data[index_start_string_nav_div:index_end_string_nav_div]
    #                         top_moodle_nav_div_begin_found = False
    #                         top_moodle_nav_div_end_found = False
    #                         break_ok = True
    #                     if break_ok:
    #                         break
    #
    #             # traitement du manifest de content.opf
    #             opf_file = ops_path_filename
    #             self.remove_manifest_line(opf_file, ".js")
    #             self.remove_manifest_line(opf_file, ".css")
    #
    #             jscss_txt = ""
    #             for r, d, f in os.walk(self.js_css_path):
    #                 for jscss_file in f:
    #                     if jscss_file.split(".")[1] == "js":
    #                         jscss_file_path_name = "/".join(["Misc", jscss_file])
    #                         jscss_txt = "".join(["<item", " href=\"", jscss_file_path_name, "\" id=\"", jscss_file.split(".")[0], "\" media-type=\"text/javascript\"/>"])
    #                     elif jscss_file.split(".")[1] == "css":
    #                         jscss_file_path_name = "/".join(["Styles", jscss_file])
    #                         jscss_txt = "".join(["<item", " href=\"", jscss_file_path_name, "\" id=\"", jscss_file.split(".")[0], "\" media-type=\"text/css\"/>"])
    #                     else:
    #                         jscss_file_path_name = ""
    #                     self.add_manifest_line(opf_file, jscss_txt)
    #
    #             # FINAL TASKS
    #             # ===================
    #             # beautify all xhtml files
    #             u.manage_info("pretifying the xhtml", u.LOG_ONLY, u.COLOR_PURPLE)
    #             y.pretify_xhtml(text_path_dir)
    #
    #             # add <br/> at the end of <body>
    #             u.manage_info("adding <br/> at the end of each body section", u.LOG_ONLY, u.COLOR_PURPLE)
    #             y.add_br(text_path_dir)
    #
    #             # creating the zipped epub file
    #             msg = "... creating the final zipped epub file"
    #             u.manage_info(msg, u.DISPLAY_AND_LOG)
    #             u.zip_epub(temp_path_dir, out_path_file_name)
    #
    #             if u.WITH_ZIP:
    #                 # create also the zip file
    #                 u.zip_epub(temp_path_dir, out_path_file_name.replace(".epub", ".zip"))
    #
    #             if u.WITH_DIR:
    #                 # and also the directory with all the epub files
    #                 out_dir_name = out_path_file_name.replace(".epub", "")
    #
    #                 # if exist delete the directory
    #                 if os.path.exists(out_dir_name):
    #                     shutil.rmtree(out_dir_name, ignore_errors=True)
    #                 # create the new dir
    #                 shutil.copytree(temp_path_dir, out_dir_name)
    #                 os.chdir(self.cwd)
    #
    #             # info that all its finished and deleting temporary files and directories
    #             u.manage_info("... putzing", u.DISPLAY_AND_LOG)
    #             # remove temporary files and directories
    #             if os.path.exists(temp_path_dir):
    #                 v_return = u.empty_dir(temp_path_dir)
    #                 if v_return != "":
    #                     v_msg = "".join([self.log_path_file_name, v_return])
    #                     u.write_in_logfile(v_msg)
    #                 f_msg = "function new_job, final tasks : remove temp dir"
    #                 try:
    #                     os.rmdir(temp_path_dir)
    #                 except:
    #                     try:
    #                         time.sleep(self.ERROR_WAIT_TIME)
    #                         self.second_try += 1
    #                         u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
    #                         u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
    #                         os.rmdir(temp_path_dir)
    #                     except:
    #                         u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)
    #
    #         elapsed_time = time.time() - t_start
    #         # self.msg_list.delete(0, END)
    #         self.msg_display.update()
    #
    #         # the result of the analyse to the user
    #         if f_ok:
    #             # all is ok
    #             t_stop = time.time()
    #             msg = ""
    #             u.manage_info(msg, u.DISPLAY_AND_LOG)
    #             msg = "".join(["Mise à jour .js et .css dans le fichier : "])
    #             u.manage_info(msg, u.DISPLAY_AND_LOG)
    #             msg = "".join([os.path.basename(in_path_file_name)])
    #             u.manage_info(msg, u.DISPLAY_AND_LOG, u.COLOR_BLUE)
    #             msg = "".join(["terminée avec succès en ", str(round(elapsed_time, 3)), " s !"])
    #             u.manage_info(msg, u.DISPLAY_AND_LOG)
    #         else:
    #             msg_info = "".join(
    #                 ["Traitements des erreurs"])
    #             u.manage_info(msg_info, u.DISPLAY_AND_LOG, u.COLOR_RED_ON_YELLOW)
    #     else:
    #         # no file selected so do nothing
    #         u.manage_info("Cancel pressed", u.DISPLAY_ONLY, u.COLOR_BLUE)
    #         u.manage_info("Select a epub", u.DISPLAY_ONLY, u.COLOR_BLUE)
    #     return out_path_file_name

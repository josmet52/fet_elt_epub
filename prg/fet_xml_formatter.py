#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fet_xhtml_formatter.py
===========

En entrée :

En sortie :

auteur : josmet
date : 10.04.2019

version 0.1 : auf eine grune weise
"""
import os
import time
import uuid
import zipfile

from datetime import datetime
from tkinter import *
from tkinter import filedialog

from fet_class import ClasseFet
from fet_lib import ClasseFetLib


class ClasseFetXmlFormatter:

    def __init__(self, var_msg, msg_list, msg_display, btn_frame, option_nav_btn_position):

        self.version_file = "fet_xml_formatter.py"
        self.version_no = "0.1"
        self.version_date = "10.04.2019"
        self.version_auteur = "Joseph Métrailler"
        self.version_description = "Version POO"
        self.version_status = "pre-alpha"

        self.nbre_passes = 0
        self.nbre_erreurs = 0

        self.IDENTATION_SPACES = 4
        self.ERROR_WAIT_TIME = 0.5
        self.second_try = 0

        # initialisation variables
        self.var_msg = var_msg
        self.msg_list = msg_list
        self.msg_display = msg_display
        self.btn_frame = btn_frame
        self.option_nav_btn_position = option_nav_btn_position

        self.pos_nav_bar = "TOP"

        self.CONTENT_OPF_FILE_NAME = "content.opf"
        self.INI_FILE_NAME = "fet_epub.ini"
        self.LOG_FILE_NAME = "fet_log.txt"

        # Current working directory
        self.cwd = "".join([str(os.getcwd()).replace("\\", "/").replace("\n", ""), "/"])
        self.new_path = ""
        self.tmp_path = ""
        self.nav_path = ""
        self.tiptop_path = ""
        self.ini_path_file_name = "".join([self.cwd, self.INI_FILE_NAME])
        self.log_path = "".join([self.cwd, "log/"])
        self.log_path_file_name = "".join([self.log_path, self.LOG_FILE_NAME])

        # lecture des répertoires dans le fichier .ini
        if os.path.isfile(self.ini_path_file_name):

            with open(self.ini_path_file_name, "r", encoding="utf-8") as f_path:
                r = f_path.readlines()
                for p in r:
                    x = p.split("=")

                    if x[0] == "org_dir":
                        self.org_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ", "").replace("//", "/")
                    elif x[0] == "new_dir":
                        self.new_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ", "").replace("//", "/")
                    elif x[0] == "tmp_dir":
                        self.new_tmp_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ", "").replace("//", "/")
                    elif x[0] == "new_nav_dir":
                        self.new_nav_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
                                            "").replace("//", "/")
                    elif x[0] == "new_tiptop_dir":
                        self.tiptop_path = "".join([x[1].replace("\"", ""), "/"]).replace("\n", "").replace(" ",
                                            "").replace("//", "/")

    def beautify_xml(self):
        """
            This function beautify the xml
            input : none
            return : none
        """

        u = ClasseFet(self.var_msg, self.msg_list, self.msg_display, self.btn_frame)
        f = ClasseFetLib()

        # disable all buttons that can not be used during this task
        u.manage_buttons("btnXmlFormat", "in")
        # clear the listbox
        u.msg_list.delete(0, END)
        u.msg_display.update()

        # go to the start dir
        os.chdir(self.cwd)

        # ask for the filename to work with
        self.in_file_name = filedialog.askopenfilename(title="Sélectionnez le fichier qu il faut rendre lisible",
                                                        initialdir=self.new_nav_path,
                                                        filetypes=[('epub files', '.epub'), ('all files', '.*')])
        if len(self.in_file_name) != 0:

            # self.out_path_file_name = self.in_file_name

            # create the out_file_name with the in_file_name
            if "_beauty" not in self.in_file_name:
                self.out_file_name = os.path.basename(self.in_file_name).replace(".epub", "_beauty.epub")
            else:
                self.out_file_name = os.path.basename(self.in_file_name)

            # the out filename goes in the new directory
            self.out_path_file_name = "".join([self.tiptop_path, self.out_file_name])
            # prepare the text to display in and out files
            self.txt_in_file = "".join(["Sce file : ", os.path.basename(self.in_file_name)])
            self.txt_out_file = "".join(["Dst file : ", self.out_file_name])

            # display the files status
            u.manage_info("".join(["Beautify XML : ", datetime.now().strftime("%Y%m%d-%H%M%S")]), u.DISPLAY_AND_LOG)
            u.manage_info("", u.DISPLAY_AND_LOG)

            # search for a "unique directory name" and create the temp directory
            self.temp_path_dir = "".join([self.tmp_path, str(uuid.uuid4()), "/"])
            os.mkdir(self.temp_path_dir)

            # unzip all files from inFileName to the temp extractDir
            u.manage_info("... unzip epub", u.DISPLAY_AND_LOG)
            with zipfile.ZipFile(self.in_file_name, "r") as z:
                z.extractall(self.temp_path_dir)

            # search for the name of the OPS directory (can be OEBPS or OPS)
            ok, self.ops_dir = u.get_ops_dir(self.temp_path_dir)
            if not ok:
                u.manage_info("get_ops_dir ERROR ... the programm give up", u.DISPLAY_AND_LOG)
            self.ops_path_filename = "".join([self.temp_path_dir, self.ops_dir, self.CONTENT_OPF_FILE_NAME])

            # path of the text directory
            self.text_path_dir = "".join([self.temp_path_dir, self.ops_dir, "Text/"])

            f_ok = True
            self.t_start = time.time()  # store the start time
            u.manage_info("... Beautify XML en cours . Patientez SVP ...", u.DISPLAY_AND_LOG)

            #================================================================
            # do the job
            #================================================================

            list_files = os.listdir(self.text_path_dir)
            for file in list_files:
                # if "anim" in file:
                #     a = 0
                working_file = "".join([self.text_path_dir, file])
                if (os.path.splitext(working_file)[1]).lower() == ".xhtml":
                    with open(working_file, "r", encoding="utf-8") as xml_file:
                        org_xml = xml_file.readlines()

                    new_xml = f.xml_formatter(org_xml)

                    with open(working_file, "w", encoding="utf-8") as xml_file:
                        xml_file.writelines(new_xml)

            # FINAL TASKS
            # ===================
            # creating the zipped epub file
            msg = "... creating the final zipped epub file"
            u.manage_info(msg, u.DISPLAY_AND_LOG)
            u.zip_epub(self.temp_path_dir, self.out_path_file_name)

            # info that all its finished and deleting temporary files and directories
            u.manage_info("... putzing", u.DISPLAY_AND_LOG)
            # remove temporary files and directories
            if os.path.exists(self.temp_path_dir):
                v_return = u.empty_dir(self.temp_path_dir)
                if v_return != "":
                    v_msg = "".join([self.log_path_file_name, v_return])
                    u.write_in_logfile(v_msg)
                f_msg = "function new_job, final tasks : remove temp dir"
                try:
                    os.rmdir(self.temp_path_dir)
                except:
                    try:
                        time.sleep(self.ERROR_WAIT_TIME)
                        self.second_try += 1
                        u.manage_info(" ".join(["2nd try in", f_msg]), u.DISPLAY_AND_LOG)
                        u.manage_error(" ".join(["2nd try in", f_msg]), "", 1)
                        os.rmdir(self.temp_path_dir)
                    except:
                        u.manage_error(" ".join(["Error in:", f_msg]), u.error_msg(sys.exc_info()), 3)

            elapsed_time = time.time() - self.t_start
            # self.msg_list.delete(0, END)
            self.msg_display.update()

            # the result of the analyse to the user
            if f_ok:
                # all is ok
                self.t_stop = time.time()
                msg = ""
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join(["Beautify du fichier : "])
                u.manage_info(msg, u.DISPLAY_AND_LOG)
                msg = "".join([os.path.basename(self.in_file_name)])
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
            u.manage_buttons("btnXmlFormat", "out")
        u.manage_buttons("btnXmlFormat", "out")

    # pour lancer la procedure d'exportation export_exo_to_moodle_xml() depuis ce fichier mais pas si la classe est incluse
    if __name__ == '__main__':

        from fet_xml_formatter import ClasseFetXmlFormatter
        F = ClasseFetXmlFormatter(None, None, None, None, None, )

        tag_txt_in = ""
        tag_txt_out = ""
        current_index = 0
        indentation_level = 0
        current_str_pos = 0

        with open("example.xhtml", "r", encoding="utf-8") as xml_file:
            org_xml = xml_file.readlines()

        # new_xml = F.xml_formatter(org_xml)
        new_xml = F.xml_formatter(org_xml)

        with open("example_new.xhtml", "w", encoding="utf-8") as xml_file:
            xml_file.writelines(new_xml)

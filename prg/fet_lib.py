#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fet_lib.py
============
Cette classe contient des fonctions utiles à la gestion des documents epub

fichier : fet_lib.py
utilisé par : fet_main.py et fet_class.py
procédure de lancement : aucune
auteur : josmet
date : 21.06.2018
"""

import re
import os
import tkinter as tk
import ctypes

class ClasseFetLib():

    def __init__(self):
        self.IDENTATION_SPACES = 4
        self.TITLE_TAG_BEG = ("<h1", "<h2", "<math")
        self.TITLE_TAG_END = ("</h1", "</h2", "</math")

    def message_box(self, title, text, style):
        ## Styles:
        #  0 : OK
        #  1 : OK | Cancel
        #  2 : Abort | Retry | Ignore
        #  3 : Yes | No | Cancel
        #  4 : Yes | No
        #  5 : Retry | No
        #  6 : Cancel | Try Again | Continue

        ## To also change icon, add these values to previous number
        # 16 Stop-sign icon
        # 32 Question-mark icon
        # 48 Exclamation-point icon
        # 64 Information-sign icon consisting of an 'i' in a circle

        ## return values
        # OK = 0
        # CANCEL = 2
        # ABORT = 3
        # YES = 6
        # NO = 7
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def find_all_substr(self, a_str, substr):
        start = 0
        while True:
            start = a_str.find(substr, start)
            if start == -1: return
            yield start
            start += len(substr)

    def get_tag_list(self, xml_txt, tag_in):

        tag_in_list = []
        tag_list_out = []

        l_tag_in = tag_in.split("+")

        for t in l_tag_in:
            tag_b_e = ["".join(["<", t]), "".join(["</", t, ">"])]
            tag_in_list.append(tag_b_e)

        no_line = 0
        for line in xml_txt:
            no_line += 1

            for tx in tag_in_list :
                if tx[0] in line:
                    a = self.find_all_substr(line, tx[0])
                    for i in a:
                        i_end = line.find(tx[1],i)
                        str_title = line[i : i_end + len(str(tx[1]))]
                        tag_list_out.append(str_title)
                        # print (str_title, no_line)

        return tag_list_out, no_line

    def get_file_list_from_spine(self, xml_txt, tag):

        tag_found = False
        file_list = []

        tag_beg = "".join(["<", tag])
        tag_end = "".join(["</", tag, ">"])

        for line in xml_txt:
            if tag_end in line :
                tag_found = False

            if tag_found:
                fragm = line.split(" ")
                for elem in fragm :
                    if "idref" in elem :
                        attrib=elem.split("=")
                        if "/" in elem:
                            v_path = attrib[1].split("/")
                            v_file_name = v_path[0][1:len(v_path[0])-1]
                            v_ext = v_file_name.split(".")[1].replace("\"", "")
                        else:
                            v_file_name = attrib[1][1:len(attrib[1])-1].replace("\"", "")
                            v_ext = v_file_name.split(".")[1].replace("\"", "")
                        if v_ext == "xhtml":
                            if v_file_name != "cover.xhtml" \
                                    and v_file_name != "nav.xhtml" \
                                    and v_file_name != "page_copyright.xhtml" \
                                    and v_file_name != "page_reference.xhtml" \
                                    and v_file_name != "toc.xhtml":
                               file_list.append(v_file_name)
                        break
            if tag_beg in line:
                tag_found = True
        return file_list

    def get_file_manifest_contenr(self, xml_txt, tag):

        tag_found = False
        tag_content = []

        tag_begin_line = "".join(["<", tag])
        tag_end_line = "/>"
        tag_begin_bloc = "".join(["<", tag])
        tag_end_bloc = "".join(["</", tag, ">"])

        for line in xml_txt:
            if not tag_found and (tag_begin_line in line and tag_end_line in line):
                tag_content.append(str(line).strip())
            else:
                if tag_found and tag_end_bloc in line :
                    tag_found = False
                if tag_found  :
                    # tag_content.append(str(line).strip())  #.replace('\u200b' or '\n' or ' ', '')
                    tag_content.append(str(line).replace('\u200b' or '\n' or ' ', ''))
                if not tag_found and tag_begin_bloc in line:
                    tag_found = True
        return tag_content

    def get_attribute(self, xml_txt, attrib):
        pos_attrib = xml_txt.find(attrib)
        pos_start = xml_txt.find("\"", pos_attrib)+1
        pos_end = xml_txt.find("\"", pos_start+1)
        return xml_txt[pos_start:pos_end]

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def get_ebook_chapters_list (self, text_path, oebps_path, chapters_style_h):

        content_path_file_name = "".join([oebps_path, "content.opf"])

        with open(content_path_file_name, "r", encoding="utf-8") as opf_file:
            # opf_lines = [x.strip() for x in opf_file.readlines()]
            opf_lines = opf_file.readlines()
            opf_file.close()

        # with open(content_path_file_name, "r", encoding="utf-8") as f:
        #     data_content = f.readlines()
        # file_list = self.get_file_list_from_spine(opf_lines, "manifest")
        file_list = self.get_file_list_from_spine(opf_lines, "spine")
        # (file_list)

        title_account = []
        i=1
        for file_name in file_list :
            file_path_name = "".join([text_path, file_name])
            if os.path.exists(file_path_name):
                with open(file_path_name, "r", encoding="utf-8") as opened_file:
                    xml_txt_data = opened_file.readlines()
                    opened_file.close()

                title_list, line_no = self.get_tag_list(xml_txt_data, chapters_style_h)

                for this_line in title_list:
                    this_file = file_name
                    this_title = self.remove_html_tags(this_line).replace('\u200b' or '\n' or ' ', '')
                    this_index = "{:03d}".format(i)
                    this_level = this_line[0:3]
                    title_account.append([this_file, this_line, this_title, this_index, this_level])
                    i += 1
        return title_account

    def update_manifest_properties(self, opf_file_path_name):
        """
        :param opf_file_path_name:
        :return: list_of_corrections[] (empty if no problem)

        """
        opf_file_path_name = "C:/Users/jmetr/Desktop/ET ch 3/OEBPS/content.opf"

        list_corrections = []
        # initialisation dictionnaire  media-type
        dic_media_type = {}
        dic_media_type[".xhtml"] = "application/xhtml+xml"
        dic_media_type[".css"] = "text/css"
        dic_media_type[".ttf"] = "application/x-font-truetype"
        dic_media_type[".png"] = "image/png"
        dic_media_type[".jpg"] = "image/jpeg"
        dic_media_type[".js"] = "application/javascript"

        #initialise le dictionnaire properties
        dic_property = {}
        dic_property["<math"] = "mathml"
        dic_property["<script"] = "scripted"
        dic_property["<svg"] = "svg"
        # dic_property["<cover"] = "cover-image"
        # dic_property["<nav"] = "nav"
        # dic_property["<switch"] = "switch"

        # initialise la liste des properties
        list_property = []
        list_property.append("<math")
        list_property.append("<scripted")
        list_property.append("<svg")

        opf_path, opf_filename = os.path.split(opf_file_path_name)
        opf_path = "".join([opf_path, "/"])

        # read the content of .opf file in xml_opf_lines[]
        with open(opf_file_path_name, "r", encoding="utf-8") as opf_file:
            xml_opf_lines = [x.strip() for x in opf_file.readlines()]
            opf_file.close()

        # from xml_opf_line get the manifest content
        manifest_found = False
        new_xml_opf_lines = []
        # pour chaque ligne du fichier content.opf
        for opf_line in xml_opf_lines:

            # si </manifest> dans la ligne : la fin du <manifest> est atteinte
            if "</manifest>" in opf_line :
                manifest_found = False

            # on est dans la section du <manifest
            if manifest_found and "<item " in opf_line:
                attrib_list = []
                # recherche tous les signes = dans la ligne
                for egal_pos in self.find_all_substr(opf_line, "="):
                    # recherche l'espace précédent
                    space_found = False
                    first_space_before_egal = egal_pos
                    while not space_found:
                        if opf_line[first_space_before_egal] == " ":
                            space_found = True
                            first_space_before_egal += 1
                        else:
                            first_space_before_egal -= 1
                    # extrait le nom de l'attribut
                    attrib_name = opf_line[first_space_before_egal : egal_pos]
                    #recherche les signes " qui encadrent la valeur et extrait la valeur
                    val_beg = opf_line.find("\"", egal_pos )
                    val_end = opf_line.find("\"", val_beg + 1)
                    attrib_val = opf_line[val_beg : val_end].strip("\"").strip()
                    # ajoute l'attribut à la liste des attributs'
                    attrib_list.append([attrib_name, attrib_val])

                # lire les valeurs des attributs en fonction de leur usage
                for attrib in attrib_list:
                    if attrib[0] == "href":
                        a_file_name = attrib[1]
                        a_file_ext = os.path.splitext(a_file_name)[1]
                    if attrib[0] == "properties":
                        a_property = attrib[1]
                    if attrib[0] == "id":
                        a_id = attrib[1]
                    if attrib[0] == "media-type":
                        a_media_type = attrib[1]

                # if a_file_ext == ".xhtml":
                #     if self.DEBUG: print (a_file_name)
                #     if self.DEBUG: print(opf_line.replace("\n", "").strip())
                    # for attr in attrib_list:
                    #     print(attr)
                    # print()


            # si <manifest dans la ligne : la début du <manifest> est atteint
            if "<manifest" in opf_line :
                manifest_found = True

        return list_corrections

    def make_one_string(self, xml_str_in):
        """
        make one continus string with xml
        and remove somme characters
        """
        xml_str_out = ""
        for l in xml_str_in:
            xml_str_out += l \
                .replace("\n", "") \
                .replace("\t", "") \
                .replace("\u200b", "")
        return xml_str_out

    def remove_comment(self, xml_str_in):
        """
        Remove all comment from string
        Comments are generally old xlm strings not more necessary
        """

        if "<!--" in xml_str_in:

            current_pos = 0  # index of working area in string
            comment_occurence = []  # list to store all comments coordiates
            comment_found = True  # to control the loop
            xml_str_out = ""
            # loop
            while comment_found:
                beg_comment = xml_str_in.find("<!--", current_pos)
                if beg_comment != -1:
                    end_comment = xml_str_in.find("-->", beg_comment) + len("-->")
                    current_pos = end_comment
                    # the is comment so add the coordinates to the list
                    comment_occurence.append((beg_comment, end_comment))
                else:
                    # no more comment so quit the loop
                    comment_found = False

            # remove all comments from the xml string
            # if there is comment
            if len(comment_occurence) > 0:
                # add the xml part before the first comment in the out str
                xml_str_out = xml_str_in[0:comment_occurence[0][0]]

            # for each next comment
            i = 0
            for i, occurence in enumerate(comment_occurence):
                if i != 0:
                    xml_str_out += xml_str_in[comment_occurence[i-1][1]:comment_occurence[i][0]]

            # add the part after the last comment
            if len(comment_occurence) > 0:
                xml_str_out += xml_str_in[comment_occurence[i][1]:]
        else:
            xml_str_out = xml_str_in

        return xml_str_out

    def xml_formatter(self, org_xml):

        # make one string
        str_xml1 = self.make_one_string(org_xml)
        # remove all comment
        str_xml = self.remove_comment(str_xml1)

        current_index = 0
        tag_found = True
        indentation_level = -1
        new_xml = ""

        while tag_found:

            beg_tag = str_xml.find("<", current_index)

            current_text = str_xml[current_index:beg_tag].strip()

            len_text = len(current_text)
            if len_text > 0:
                new_xml += "\n" + ' ' * (indentation_level+1) * self.IDENTATION_SPACES + current_text

            if beg_tag == -1:
                tag_found = False
            else:
                end_tag = str_xml.find(">", beg_tag) + 1
                current_index = end_tag

                tmp_tag = str_xml[beg_tag:end_tag].strip().replace(" ", "")
                current_tag = str_xml[beg_tag:end_tag]

                # print(current_tag)

                if not ("<?xml" in current_tag or "<!DOCTYPE" in current_tag or "<html" in current_tag):

                    if tmp_tag.find("/>") != -1 or tmp_tag.find("]>") != -1:
                        the_case = 3  # tag ouvert-fermé
                    elif tmp_tag.find("</") != -1:
                        the_case = 2  # fermeture de tag
                    elif beg_tag != -1 and end_tag != -1:
                        the_case = 1  # ouverture de tag
                    else:
                        the_case = 0

                    if the_case == 0:
                        tk.MessageBox(0, "OUUUUPS ERROR TAG : " + current_tag, 'Erreur')
                        print("OUUUUPS ERROR TAG : ", current_tag)
                    elif the_case == 1:
                        indentation_level += 1
                        new_xml += "\n" + ' ' * indentation_level * self.IDENTATION_SPACES + current_tag
                    elif the_case == 2:
                        # if len_text < 70 and "script" in current_tag :
                        #     new_xml += current_tag
                        # else:
                        #     new_xml += "\n" + ' ' * indentation_level * self.IDENTATION_SPACES + current_tag
                        new_xml += "\n" + ' ' * indentation_level * self.IDENTATION_SPACES + current_tag
                        indentation_level -= 1
                    elif the_case == 3:
                        new_xml += "\n" + ' ' * (indentation_level+1) * self.IDENTATION_SPACES + current_tag

                    # new_xml += "\n" + ' '  * indentation_level * self.IDENTATION_SPACES + current_tag
                else:
                    new_xml += current_tag + "\n"

        new_new_xml = ""
        new_h_str = ""
        beg_h_found = False
        end_h_found = False
        first_pass = True


        tmp_xml = new_xml.split("\n")
        # for l in tmp_xml: print(l)

        for line in tmp_xml:

            for tag_beg in self.TITLE_TAG_BEG:
                if tag_beg in line :
                    beg_h_found = True
                    break

            if not beg_h_found :
                new_new_xml += line + "\n"
            else:
                if first_pass :
                    new_h_str += line
                    first_pass = False
                else:
                    new_h_str += line.strip()

            for tag_end in self.TITLE_TAG_END:
                if tag_end in line :
                    end_h_found = True
                    break

            if end_h_found:
                new_new_xml += new_h_str.replace("\n", "") + "\n"
                new_h_str = ""
                beg_h_found = False
                end_h_found = False
                first_pass = True

        # new_new_xml += "\n"

        # essai pour le script dans le body get script code
        script_data = self.get_script_code(org_xml)
        # for l in script_data: print(l)

        working_data = new_new_xml.split("\n")
        # for l in working_data: print(l)

        #insert the script just before </body>
        in_body = False
        in_script = False
        s_new_xml = []
        for l in working_data:

            if "<body>" in l:
                in_body = True
            elif "</body>" in l:
                in_body = False
                for s_l in script_data:
                    s_new_xml.append(s_l)
            elif "<script>" in l:
                in_script = True

            if (not in_body) or (in_body and not in_script):
                s_new_xml.append(l + "\n")

            if "</script>" in l:
                in_script = False
        # for l in s_new_xml: print(l)

        return s_new_xml
        # return new_new_xml


    def pretify_xhtml(self, file_path_name):

        list_files = os.listdir(file_path_name)
        for file in list_files:
            working_file = "".join([file_path_name, file])
            if (os.path.splitext(working_file)[1]).lower() == ".xhtml":
                with open(working_file, "r", encoding="utf-8") as xml_file:
                    org_xml = xml_file.readlines()
                if "tri_anim_alternateur_triphase_v1d" in working_file:
                    a = 0
                new_xml = self.xml_formatter(org_xml)
                with open(working_file, "w", encoding="utf-8") as xml_file:
                    xml_file.writelines(new_xml)

    def add_br(self, file_path_name):

        list_files = os.listdir(file_path_name)
        for file in list_files:
            working_file = "".join([file_path_name, file])
            if (os.path.splitext(working_file)[1]).lower() == ".xhtml":
                with open(working_file, "r", encoding="utf-8") as xml_file:
                    org_xml = xml_file.readlines()
                line_m1 = ""
                new_xml = []
                for line_m0 in org_xml:
                    if "</body>"in line_m0:
                        if line_m1 != "<br/>":
                            # new_xml.append("    <br/>\n")
                            line_m0 = line_m0.replace("</body>", "<br/></body>")
                    new_xml.append(line_m0)
                    line_m1 = line_m0
                with open(working_file, "w", encoding="utf-8") as xml_file:
                    xml_file.writelines(new_xml)

    def get_script_code (self, in_data):

        body_found = False
        script_found = False
        script_data = []

        for l in in_data:
            # print(l)
            if "<body>" in l:
                body_found = True
            if "<script>" in l:
                script_found = True
            if body_found and script_found:
## ZONE A PROBLEME DEBUT ====================================================================================
## le problèem est que s'il y a deux tags sur une ligne, les deux sont inscrits dans la ligne en cours
                if not l is None :
                    # nbre_tags = l.count("<")
                    # if nbre_tags > 1 :
                    #     print(l)
                    script_data.append(l.replace("</form>", ""))
## ZONE A PROBLEME FIN ====================================================================================
            if "</body>" in l:
                body_found = False
            if "</script>" in l:
                script_found = False
        script_data.append("\n")
        # for l in script_data: print(l)
        return script_data


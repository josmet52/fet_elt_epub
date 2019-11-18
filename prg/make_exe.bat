pyinstaller --noconfirm --noconsole --icon=logo_fet.ico fet_main.py
pause
copy C:\Users\jmetr\_data\mandats\FET_new\fet_elt_epub\prg\fet_epub.ini C:\Users\jmetr\_data\mandats\FET_new\fet_elt_epub\prg\dist\fet_main\fet_epub.ini
xcopy /e C:\Users\jmetr\_data\mandats\FET_new\fet_elt_epub\prg\epubcheck C:\Users\jmetr\_data\mandats\FET_new\fet_elt_epub\prg\dist\fet_main\epubcheck\
pause "appuyez sur une touche pour terminer"

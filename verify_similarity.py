#coding: utf-8

from os import listdir
from os.path import isfile, join


def is_in(dir, file, cat):
    dir_cat = dir + cat + "/"
    for f in listdir(dir_cat):
        if isfile(join(dir_cat, f)):
            if(f == file):
                return True
    return False


def verify_is(dir, cat, dir2):
    dir_cat = dir + cat + "/"
    for f in listdir(dir_cat):
        if isfile(join(dir_cat, f)):
            if(is_in(dir2, f, cat) != True):
                categories = ["positivo", "negativo", "neutro"]
                categories.remove(cat)
                for categ in categories:
                    if (is_in(dir2, f, categ) == True):
                        print("%s deveria ser \"%s\", mas está em \"%s\"" % (f, categ, cat))



dir_ver1 = 'contents/NB/release_1.1.0_nltk/'
dir_ver2 = 'contents/release_1.1.0 - classif/'

verify_is(dir_ver1, "positivo", dir_ver2) # Verificar os positivos
verify_is(dir_ver1, "negativo", dir_ver2) # Verificar os positivos
verify_is(dir_ver1, "neutro", dir_ver2) # Verificar os positivos
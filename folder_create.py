import os

def create_folder(folder_name, valami):
    try:
        os.mkdir('C:/test/' + folder_name)
        for mappa_i in range(len(valami)):
            os.chdir('C:/test/' + folder_name)
            os.mkdir('C:/test/' + folder_name + '/' + str(mappa_i))
        os.chdir('C:/test/' + folder_name)
        print("Directory made and changed.")
    except FileExistsError:
        print("This directory", folder_name, "already exist")
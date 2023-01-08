from functions import *

file_name, file_extension = GET_FILE_PATH('paths.txt', 'XY_FORMAT_FOR_IUA_PLUS_FILENAME')
# example: file_name = "YYY-XXXXXX_XY input format for IUA_plus_Rev00" and file_extension = "xlsx"

template_location = GET_FOLDER_PATH('paths.txt', 'folder_template_path')

revision_string_format = GET_REVISION_STRING('paths.txt', "REVISION_FORMAT")

revision_pos_in_file_name = file_name.index(revision_string_format)
revision_string = file_name[revision_pos_in_file_name:]

temp = revision_string[len(revision_string_format):]
print('revision_string_in file name: ', temp)
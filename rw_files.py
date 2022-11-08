import csv
import docx2txt


def read_txt(input_file_path: str):
    with open(input_file_path) as f:
        lines = f.read()
        return lines


def read_docx(input_file_path: str):
    return docx2txt.process(input_file_path)


def read_csv(input_file_path: str):
    # open file in read mode
    with open(input_file_path, 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = csv.DictReader(read_obj)
        """gets a list of dictionaries from dict_reader"""
        list_of_dict = list(dict_reader)
        # print list of dict i.e. rows
        # print(list_of_dict[0])
        # print("\n")
        return list_of_dict


def write_csv(output_file_path: str, list_of_dict: list[dict]):
    with open(output_file_path, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=list_of_dict[0].keys(),
                                     lineterminator='\n', dialect=csv.excel)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)













# coding: utf-8

import codecs
import subprocess

def run_commnad(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    # print "waiting for the command to finish"
    stdout_data, stderr_data = p.communicate()
    return stdout_data, stderr_data

def parse_segmentation(string, test_file_out):
    segmentation_results = string.split("EOS\n")
    for segmentation_result in segmentation_results:
        tokens = []
        for token_info in segmentation_result.split("\n")[:-1]:
            columns = token_info.split()
            tokens.append(columns[0])
        test_file_out.write(" ".join(tokens) + "\n")
    return tokens


def preprocess_file(in_file_location):
    temp_file = codecs.open(in_file_location + "_space_deleted.txt", "w", "utf-8")
    test_file = codecs.open(in_file_location, "r", "utf-8")
    for line in test_file:
        line = line.replace(u"／", "")  # For Twitter data
        temp_file.write(line.replace(" ", ""))
    temp_file.close()
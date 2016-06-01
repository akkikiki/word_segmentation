import codecs
import subprocess

def preprocess_file(in_file):
    f = codecs.open(in_file, "r", "utf-8")
    preprocessed_file_location = in_file + "_space_deleted.txt"
    f_preprocessed = codecs.open(preprocessed_file_location, "w", "utf-8")

    for line in f:
        f_preprocessed.write(line.replace(" ", ""))

def parse_segmentation(stdout_data, test_file_out):
    # f_test_file_out = codecs.open(test_file_out, "w", "utf-8")
    segmented_string = []
    for line in stdout_data.split("\n"):
        if line == "EOS":
            print " ".join(segmented_string)
            test_file_out.write(" ".join(segmented_string) + "\n")
            segmented_string = []
            continue

        if line.split():
            segmented_string.append(line.split("\t")[0])

def run_commnad(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    # print stdout_data
    return stdout_data, stderr_data

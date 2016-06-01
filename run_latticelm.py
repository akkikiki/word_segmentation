# coding: utf-8
# TODO:To be implemented.

# insert a space into every characters
import codecs
import run_command

in_file  = "data/test_data/uniq_katakanas.txt"
out_file = codecs.open(in_file + "_char_segmented", "w", "utf-8")

for line in codecs.open(in_file, "r", "utf-8"):
    print line[:-1]
    a = list(line[:-1])
    out_file.write(" ".join(a) + "\n")

run_latticelm = "/Users/Fujinuma/Software/latticelm_github/latticelm/latticelm -prefix out/ %s" % (in_file + "_char_segmented")
stdout_data, _ = run_command.run_commnad(run_latticelm)
print stdout_data
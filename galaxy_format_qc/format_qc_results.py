import sys
import re


"""
Sub program 
"""
def format_bracken_report(bf):
    bf_array = bf.readlines()
    temp = bf_array[1].split()
    species_name = temp[0] + "-" + temp[1]
    species_coverage = temp[7]

    return species_name, species_coverage

def format_fastqc_summary(fastqc_summary):
    fastqc_array = fastqc_summary.readlines()
    temp = fastqc_array[1].split("\t")
    read_length = temp[5]
    total_number_of_bases = temp[4]
    coverage = temp[8]
    percentage_duplication = abs((float(temp[10]) + float(temp[11]))/2) 

    return read_length,coverage

def format_fastqc_report(fqc_report):
    start_phred_cal = 0 
    phred_score = 0
    n_phred_score = 0
    for i in fqc_report:
        # total number of reads
        if re.search("^Total Sequences",i):
            tot_seq = i.split()[2]

        # Read length
        if re.search("^Sequence length",i):
            read_length = i.split()[2]

        if re.search("^%GC",i):
            GC_per = i.split()[1]

        # Phred score calculation
        if start_phred_cal == 1:
            if not re.search(">>END_MODULE",i):
                phred_score += float(i.split()[1]) 
                n_phred_score += 1
        
        if re.search("^#Base",i):
            start_phred_cal += 1

        if re.search(">>END_MODULE",i) and (start_phred_cal == 1):
            start_phred_cal = 0
            mean_phred_score = phred_score/n_phred_score
            break
        
    return GC_per, mean_phred_score, int(tot_seq),int(read_length)

# Main 

# Input 1: bracken file 
bf = open(sys.argv[1],"r")

# Input 2:Fastqc Summary output Phred Score summary 
#fastqc_summary = open(sys.argv[2],"r")

# Input 4 and 5: Phred Score summary 
fqc_forward = open(sys.argv[2],"r")
fqc_reverse = open(sys.argv[3],"r")

# Input 5
genome_size = int(sys.argv[4])

# Output File
OF = open("formatted_read_qc_output.txt","w")
header = "SpeciesName\tProportionOfMappedReads\tReadLength\tCoverage\tGC-Content\tMean-PhredScore\n"
OF.write(header)

# Part 1: Format Bracken Output
(species_name,species_coverage) = format_bracken_report(bf)

# Part 2 Format FastQC Summary
#(read_length, coverage) = format_fastqc_summary(fastqc_summary)

# Part 3 Format FastQC reports
GC_per_forward,mean_phred_score_forward,tot_seq_forward,read_length_forward = format_fastqc_report(fqc_forward)
GC_per_reverse,mean_phred_score_reverse,tot_seq_reverse,read_length_reverse = format_fastqc_report(fqc_reverse)
GC_per = (float(GC_per_forward) + float(GC_per_reverse))/2
mean_phred_score = (mean_phred_score_forward + mean_phred_score_reverse)/2
coverage = int(((tot_seq_forward * read_length_forward) * 2)/genome_size)

# Write the results into the file
txt = species_name + "\t" + str(species_coverage) + "\t" + str(read_length_forward) + "\t" + str(coverage) + "x" + "\t" + str(GC_per) + "%" + "\t" + str(mean_phred_score) + "\n" 

OF.write(txt)

OF.close()


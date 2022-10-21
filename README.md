## QC Pipeline - FastQ_Reads

### Tools list
|No.| Steps | Tool name|
|---|--- |--- |
|1.| Length of reads|FastQC |
|2.| Coverage | Use FastQC stat and genome size |
|3.| Species confirmation and contamination (interspecies) |Kraken2-Bracken|
|2.| Format_QC_Results | Formats Bracken and fasqc results. Takes genome size as input and calculates coverage |


Format_QC_Results - Locally developed. So, it has to be added to galaxy manually as of Oct 2022. Soon, it will be added to galaxy toolshed


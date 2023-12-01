import os
import argparse
import pandas as pd
import subprocess

USER = os.environ.get('USER')

def process_pcap(directory_dohlyzer, pcap_folder, output, cleaning):
    csv_files = []
    for file in os.listdir(pcap_folder):
        if file.endswith(".pcap"):
            pcap_file = os.path.join(pcap_folder, file)
            csv_file = os.path.splitext(pcap_file)[0] + ".csv"
            command = '/home/{user}/anaconda3/condabin/conda run -n DoHLyzer python3 {dohlyzer}DoHLyzer/meter/dohlyzer.py -f {pcap} -c {csv}'.format(
                user = USER,
                dohlyzer = directory_dohlyzer, 
                pcap = pcap_file, 
                csv = csv_file)
            
            try:
                subprocess.check_call(command, shell=True)
                csv_files.append(csv_file)
            except subprocess.CalledProcessError as e:
                print("Error executing command:", e)
                break
    
    if csv_files:
        merge_csv_files(csv_files, pcap_folder, output, cleaning)

def merge_csv_files(csv_files, pcap_folder, output, cleaning):
    combined_data = pd.DataFrame()
    
    for file in csv_files:
        data = pd.read_csv(file)
        combined_data = combined_data.append(data, ignore_index=True)
    
    print('output:' + str(output))
    if pcap_folder != output:
        merged_csv_file = output
    else:
        merged_csv_file = os.path.join(pcap_folder, "merged.csv")

    print(merged_csv_file)
    combined_data.to_csv(merged_csv_file, index=False)
    print("Merged CSV file created:", merged_csv_file)

    if cleaning:
        for file in csv_files:
            try:
                os.remove(file)
            except OSError as error:
                print(error)
                print("File path can not be removed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process pcap files with DoHLyzer and merge CSV files")
    parser.add_argument("-d", "--directory_dohlyzer", help="Path to the DoHLyzer directory", required=True)
    parser.add_argument("-p", "--pcap_folder", help="Path to the folder containing pcap files", required=True)
    parser.add_argument("-o", "--csv_output", help="Path to the resulting merged CSV file")
    parser.add_argument("-c", "--clear", help="Clear the intermediate CSV files created", action="store_true")
    args = parser.parse_args()

    directory_dohlyzer = args.directory_dohlyzer
    pcap_folder = args.pcap_folder

    if args.csv_output:
        output = args.csv_output
    else:
        output = pcap_folder
    
    cleaning = args.clear

    process_pcap(directory_dohlyzer, pcap_folder, output, cleaning)

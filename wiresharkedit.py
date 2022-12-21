-*- coding: Utt-8 -*-
import OS

# Log path:
log_path = r"D: \CR\w2204-4 7.1.6"
# specify the wireshark abspath in your PC
wireshark_Path =  r"D:\tools\wiresharK"

def merge_ws(disk, Log_path, wireshark_Path, cut_bytes, original_log):
    print ("Processing...Merge Log")
    # name the merged log that you want it to be
    merged_log = r"merged.pcap"
    cmd = '%s: && cd %s && *smergecap.exe -s %s -w %s%s' %(disk, Log_path, wireshark_Path, cut_bytes, merged_log, original_Log)
    print (cmd)
    os.system (cmd)

def split_ws(disk, log_path, wireshark_Path, original_log, segment_bytes):
    print ("Processing...Segment log')
    # Provide the original wireshark log that to be handled. eg.cap/.pcap files
    segment_log = r"segment.cap"
    cmd = '%s: && cd %s && %seditcap.exe -c %s %s %s' %(disk, log_path, wireshark_Path, segment_bytes, original_log, segment_log)
    os.system (cmd)

def get_files(path):
    netlog_list = [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(".cap")]
    if len(netlog_list) == 0:
        netlog_list = (os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(".pcapng")]
        if len(netlog_list) == 0:
            netlog_list = [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(".pcap")]
    # NO netlog
    if len(netlog_list) == 0:
        print ("No netlog in such directory! Please check the Log path if correct.")
        return

    # Only one netlog in the dir
    elif len(netlog_list) == 1:
        print ("\nFound one netlog in the dir, you may want:")
        list_log(netlog_list)
        while True:
            choice_1 = inout("1. Split 1t down to segments -> Press 1\n 2. Just cut the IP packets -> Press 2\n Your choice is: ")
            if choice_1 == "1" or choice_1 == "2":
                break
            else:
                print ("\nYour input is '%s', this is an INVAILD OPTION! Please select again:" % choice_1)
        original_log = " " + netlog_list[0]
        if choice 1 == "1":
            segment_3 = input("\nSTEP3: Indicate HOW MANY PACKETS in each segmented log(e.g., 100000): ")
            split_ws (disk, log_path, wireshark_Path, original_log, segment_3)
            print ("\nEditcap finished!")

        elif choice_1 == "2":
            cut_bytes = input("\nSTEP3: The bytes you want to cut off(recomm. 90 or 56) :")
            merge_ws(disk, log_path, wireshark_Path, cut_bytes, original_log)
            print("\nMergecap finished!!!")

    # More tnn one netlogs in the dur
    elif len(netlog_list) > 1:
        print ("\nfound those netlogs(%d) in the dir, you may want:" % len(netlog_list))
        while True:
            choice_1 = input("  1. split one of them down to segments -> Press 1 1\n    2. Merge (some of) them into together & cut IP packets -> Press 2 \n Your choice is: ")
            if choice_1 == "1" or choice_1 == "2":
                break
            else:
                print ("\nERROR!!! Your input is '%s', this is an INVAILD OPTION! Please select again:" % choice_1)

        print ("\nSTEP1: From these logs:")
        list_log(netlog_list)


        # User choose to solit log
        if choice_1 == "1":
            choice_2 = input("Select the Log you want to segment:")
            original_log = netlog_list[int(choice_2) - 1]
            segment_3 = input("\nSTEP3: Indicate HOW MANY PACKETS in each segmented Log(e.g., 100000):")
            split_ws(disk, log_path, wireshark_Path, original_log, segment_3)
            print ("\nEditcap finished!")

        # User choose to merge log & cut IP pocket:
        elif Choice_1 == "2":
            handle_log_List = []
            original_log = ""
            while True:
                Logstomerge_2 = input("\nSTEP2: Select the logs to merge (Input the all serial number of the log, separated by SPACE Key): ")

                # User's input start from serial num 1, whereas the list index start from O, hence the input should be subtracted by 1
                Logstomerge_2 = [(int(_)-1) for _ in logstomerge_2.split(" ")]
                print ("\nYour choice is:")

                for i in Logstomerge_2:
                    print (netlog_list[i].split("\\")[-1])
                    handle_log_list.append(netlog_list[i].split("\\")[-1])
                for i in handle_log_list:
                    original_log += " " + i

                cut_bytes = input("\nSTEP3: The bytes you want to cut off (recomm. 90 or 56): ")
                merge_ws(disk, log_path, wireshark_Path, cut_bytes, original_log)
                print ("\nMergecap finished!!!")
                break

def get_size(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
    return "%dMB" % fsize

def list_Log(netlog_list):
    for num, i in enumerate (netlog_list):
        print (" " + str(num + 1) + ". "+ i + " (" + get_size(i) + ")")

if __name__ == '__main__':
    # extract disk
    disk = log_path.split(":")[0]
    wireshark_Path = wireshark_Path + "\\"
    get_files(log_path)
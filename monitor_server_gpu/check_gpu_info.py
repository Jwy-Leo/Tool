import os
import cv2
import argparse
import subprocess
import numpy as np
#sense_usuage=500 # MB
#update_intervel=5#300 #300 # 5 min
def Arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--sense_capability_usage", type=int, default=500, help="set a bounding of gpu active such as lower than 500MB is active")
    parser.add_argument("-S", "--update_second", type=int, default=300, help="set update gpu status frequency (second)")
    parser.add_argument("-F", "--server_file_path", type=str, default="config/observe_server_list.cfg", help="Read server list from file")
    args = parser.parse_args()
    print(args)
    return args

def main(args):
    readtext = open_server_list(args.server_file_path)
    while True:
        gpu_info_list = server_status_check(readtext, args.sense_capability_usage)
        if not draw_gpu_info(gpu_info_list, args.update_second): break
        print("updating")

def open_server_list(FilePath):

    if not os.path.exists(FilePath):
        raise IOError("{} path doesn't exists".format(FilePath))
    
    with open(FilePath, 'r') as F:
        readtext = F.readlines()

    return readtext

def server_status_check(readtext, sense_capability_MB):

    gpu_info_tuple_list = []

    for _readtext in readtext:
        text_blob = [text for text in _readtext.rstrip().split(" ") if text!=""]
        if text_blob[0] == "#": continue

        server_name, username, IP, port, passward = text_blob
        command_blob = ['sshpass', "-p", passward, "ssh", "{}@{}".format(username, IP), "-p", port, 'nvidia-smi', '--query-gpu=timestamp,memory.used', '--format=csv']
        # print(" ".join(command_blob))
        ssh = subprocess.Popen(
            command_blob, \
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        back = ssh.stdout.readlines()
        gpu_status = []
        if len(back)>1:
           back = back[1:]
           count = 0
           for gpu_info in back:
               MB_size = int(str(gpu_info.rstrip()).split(",")[1].split(' ')[1])
               if MB_size <= sense_capability_MB:
                   count += 1
                   gpu_status.append(True)
               else:
                   gpu_status.append(False)
           # print("{}, can used/Total gpu, {}/{}".format(server_name, count, len(back)))
        else:
           # print("{}'s gpu doesn't work".format(server_name))
           pass
        gpu_info_tuple_list.append((server_name, gpu_status))

    return gpu_info_tuple_list
def draw_gpu_info(infos, update_second):
    length = len(infos)
    lp_w_loc = [10, 210, 260, 310, 360]
    lp_h_loc = [50 + 50*i for i in range(length)]#[10, 60, 110, 160, 210]
    drawer = np.zeros((50 + length*50, 500, 3), np.uint8)
    for index_h, _info in enumerate(infos):
        server_name, SV_status = _info
        h_loc = lp_h_loc[index_h]
        cv2.putText(drawer, server_name, (lp_w_loc[0], h_loc), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 255), 3, cv2.LINE_AA)
        for index, status in enumerate(SV_status):
            loc = (lp_w_loc[index+1], h_loc)
            color = (0,255,0) if status==True else (0,0,255)
            cv2.circle(drawer, loc, 25, color, -1)
    cv2.imshow("gpu_info", drawer)
    #window_close = cv2.getWindowProperty('gpu_info', 0)
    key = cv2.waitKey(update_second*1000)
    if key ==ord('q') or cv2.getWindowProperty('gpu_info', cv2.WND_PROP_AUTOSIZE)<0:
        #cv2.destroyAllWindows()
        return False
        #exit(0)
    #cv2.destroyAllWindows()
    return True 

if __name__ == "__main__":
    args = Arguments()
    main(args)

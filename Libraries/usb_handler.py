import subprocess
import os
import send

def detect_keydrive():
        if os.name == 'nt':
            try:
                subprocess.check_output("wmic logicaldisk list brief | findstr KEYDRIVE", shell=True)
            except subprocess.CalledProcessError:
                return False
            return True
        elif os.name == 'posix':
            try:
                subprocess.check_output("lsblk -o MOUNTPOINT | grep KEYDRIVE", shell=True)
            except subprocess.CalledProcessError:
                return False
            return True


def usb_read_write_chunk(chunk):
    if chunk is "read":
        keydrive_chunk = open('<path_to_Dist_Login>/Files/usb_chunk.txt').read()
        return keydrive_chunk
    else:
        keydrive_file = open('<path_to_Dist_Login>/Files/usb_chunk.txt', "w")
        keydrive_file.write(chunk)
        keydrive_file.close()
        send.transmit()
        return 0

def init_usb_chunk(chunk):
    f = open('<path_to_mounted_KEYDRIVE>/chunk.txt', 'w+')
    print("chunks[0]: " + chunk)
    f.write(chunk)
    f.close()
    print("close file")

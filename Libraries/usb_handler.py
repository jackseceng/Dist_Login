import subprocess
import os


def detect_keydrive():
        if os.name == 'nt':
            try:
                subprocess.check_output("wmic logicaldisk list brief | findstr KEYDRIVE", shell=True)
            except subprocess.CalledProcessError:
                return False
            return True
        elif os.name == 'posix':
            output = str(subprocess.check_output("lsblk -o MOUNTPOINT | grep KEYDRIVE", shell=True))
            if not output.find("KEYDRIVE"):
                return False
            else:
                return True


def usb_read_write_chunk(chunk):
    drive_path = ""
    output = ""
    if os.name == 'nt':
        try:
            output = str(subprocess.check_output("wmic logicaldisk list brief | findstr KEYDRIVE", shell=True))
        except subprocess.CalledProcessError:
            print("KEYDRIVE not found")
            exit()
        drive_path = (output[2:3] + ':\chunk.txt')
    elif os.name == 'posix':
        output = str(subprocess.check_output("lsblk -o MOUNTPOINT | grep KEYDRIVE", shell=True))
        if not output.find("KEYDRIVE"):
            print("KEYDRIVE not found")
            exit()
        else:
            output = (output[2:])
            output = (output[:-3])
            drive_path = (output + '/chunk.txt')
    if chunk is "read":
        keydrive_chunk = open(drive_path).read()
        return keydrive_chunk
    else:
        keydrive_file = open(drive_path, "w")
        keydrive_file.write(chunk)
        keydrive_file.close()
        return 0

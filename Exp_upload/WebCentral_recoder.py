class WebCentral_recoder():
    def __init__(self,
                 RecodeName,
                 Location,
                 ExpNote="",
                 GSpreadSheet=''# your google sheet name):
        GDriveJSON = '' # your Access key
        GSpreadSheet = GSpreadSheet
        import time
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials as SAC
        username, ip = self.get_ip_address('eth0')
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            excel_client = gspread.authorize(key)
            worksheet = excel_client.open(GSpreadSheet).sheet1
            data = worksheet.get_all_records()
            Time = time.strftime('%Y/%m/%d\t:\t%H:%M:%S', time.localtime())
            if len(data) == 0:
                worksheet.append_row((1, RecodeName, Time, username + ":" + ip, Location, ExpNote))
            else:
                worksheet.append_row(
                    (int(data[len(data) - 1]['Number']) + 1, RecodeName, Time, username + ":" + ip, Location, ExpNote))
        except Exception as ex:
            print(ex)
    def get_ip_address(self,ifname):
        import socket
        import fcntl
        import struct
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.gethostname(), socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                                                  0x8915,  # SIOCGIFADDR
                                                                  struct.pack('256s', ifname[:15]))[20:24]),
if __name__=="__main__":
    WebCentral_recoder("HAHA",Location=__file__)

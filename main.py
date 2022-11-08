import wha_gui as whagui
import email_smtp as msmtp
import rw_files as rwf
import exceptions
import configparser as cp
import time
import datetime as dt


start_time = time.time()
# Press the green button in the gutter to run the script
if __name__ == '__main__':

    def format_time(ip_time: dt.datetime):
        # print(ip_time.year, ip_time.month, ip_time.day, ip_time.hour, ip_time.minute, ip_time.second)
        time_str = ip_time.day.__str__() + "/" + ip_time.month.__str__() + "/" + ip_time.year.__str__()
        return time_str

    """
    def format_msg(msg: str) 
    ... processes the body of the msg argument so to  
        substitute the placeholders contained in the    
        msg with candidate info such as name, degree, etc. 
    """

    csv_file_path = 'files/contacts.csv'
    wha_msg_m_path = 'files/msg/wha_msg_m.docx'
    wha_msg_f_path = 'files/msg/wha_msg_f.docx'
    email_msg_m_path = 'files/msg/email_msg_m.docx'
    email_msg_f_path = 'files/msg/email_msg_f.docx'

    # list of dictionaries of strings (key:string -> value:string)
    csv_rows: list[dict] = rwf.read_csv(csv_file_path)

    config = cp.ConfigParser()
    config.read('files/config.ini')
    email_adr_sender = config['EMAIL']['email_adr_sender']
    pswd = config['EMAIL']['pswd']
    subject = config['EMAIL']['subject']
    coord_x = int(config['GUI']['coord_x'])
    coord_y = int(config['GUI']['coord_y'])
    wait_time = int(config['GUI']['wait_time'])
    close_time = int(config['GUI']['close_time'])
    """
    idea for upgrade:
    email and wha_msg strings can be extended with 
    placeholders to be replaced with candidate info by 
    calling the format_msg(msg: str) method defined above
    """
    email_msg_m = rwf.read_docx(email_msg_m_path)
    email_msg_f = rwf.read_docx(email_msg_f_path)
    wha_msg_m = rwf.read_docx(wha_msg_m_path)
    wha_msg_f = rwf.read_docx(wha_msg_f_path)

    """
    idea for upgrade: 
    msgs = check_received_wha_msgs() 
    for m in msgs for row in csv_rows 
        if m["Name"] = row["Name"] && row["wha"] is True
            row["WHA_risp"] = True 
            row["WHA_risp_tstamp"] = dt.now()
    """

    for row in csv_rows:

        if row["email_flag"].lower() == 'y' and row['email'].lower() == 'n':
            email_adr_receiver = row["email_address"].lower()
            if row["gender"].lower()[0] == 'm':
                msmtp.send_mail(email_adr_sender, pswd, subject, email_msg_m, email_adr_receiver)
            elif row["gender"].lower()[0] == 'f':
                msmtp.send_mail(email_adr_sender, pswd, subject, email_msg_f, email_adr_receiver)
            else:
                raise exceptions.UnspecifiedGender(
                    "You must specify a valid gender for "+row["name"]+" "+row["surname"] +
                    " in order to contact him/her!"
                )
            row['email_flag'] = 'n'
            row['email'] = 'y'
            row['email_date'] = format_time(dt.datetime.now())
            rwf.write_csv(csv_file_path, csv_rows)

        phone_num = row["phone_number"].replace(" ", "")
        if '+39' not in row["phone_number"]:   # italian prefix
            phone_num = '+39'+row["phone_number"]

        if row['wha_flag'].lower() == 'y' and row['wha'].lower() == 'n':
            if row["gender"].lower()[0] == 'm':
                # u.instant_send_wha_msg(phone_num, wha_msg_m, coord_x, coord_y)
                whagui.instant_send_wha_msg(phone_num, wha_msg_m, coord_x, coord_y, wait_time, True, close_time)
                # sleep for 2 secs between one call to send_wha_msg_instantly() and the other
                print("WHA Sent Successfully!")
            elif row["gender"].lower()[0] == 'f':
                whagui.instant_send_wha_msg(phone_num, wha_msg_f, coord_x, coord_y, wait_time, True, close_time)
                # sleep for 2 secs between one call to send_wha_msg_instantly() and the other
                print("WHA Sent Successfully!")
            else:
                raise exceptions.UnspecifiedGender(
                    "You must specify a valid gender for "+row["NAME"]+" "+row["SURNAME"] +
                    " in order to contact him/her!"
                )
            row['wha_flag'] = 'n'
            row['wha'] = 'y'
            row['wha_date'] = format_time(dt.datetime.now())
            rwf.write_csv(csv_file_path, csv_rows)
            time.sleep(2)
    # print(csv_rows[0])


print("--- Run time: %s seconds ---" % (time.time() - start_time))



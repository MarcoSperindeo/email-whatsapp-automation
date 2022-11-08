import time
import datetime as dt
from platform import system
from urllib.parse import quote
import webbrowser as web
import pyautogui as pg
import exceptions
import logs


WIDTH, HEIGHT = pg.size()


def check_number(number: str) -> bool:
    """Checks the Number to see if contains the Country Code"""

    return "+" in number or "_" in number


def close_tab(wait_time: int = 2) -> None:
    """Closes the Currently Opened Browser Tab"""

    time.sleep(wait_time)
    if system().lower() in ("windows", "linux"):
        pg.hotkey("ctrl", "w")
    elif system().lower() == "darwin":
        pg.hotkey("command", "w")
    else:
        raise Warning(f"{system().lower()} not supported!")
    pg.press("enter")


def _web(receiver: str, message: str) -> None:
    """Opens WhatsApp Web based on the Receiver"""
    if check_number(number=receiver):
        web.open(
            "https://web.whatsapp.com/send?phone="
            + receiver
            + "&text="
            + quote(message)
        )
    else:
        web.open("https://web.whatsapp.com/accept?code=" + receiver)


"""
def get_wha_msgs_info() -> list[tuple]:
   ... gui controller  iterates over received msgs and  
        retrieves info such as body, sender and tstamp. 
"""


def send_message(message: str, receiver: str, coord_x: int, coord_y: int, wait_time: int) -> None:
    """Parses and Sends the Message"""

    _web(receiver=receiver, message=message)
    time.sleep(7)
    # click(WIDTH / 2, HEIGHT / 2)
    pg.click(WIDTH - coord_x, HEIGHT - coord_y)
    time.sleep(wait_time - 7)
    if not check_number(number=receiver):
        for char in message:
            if char == "\n":
                pg.hotkey("shift", "enter")
            else:
                pg.typewrite(char)
    pg.press("enter")


def instant_send_wha_msg(
    phone_no: str,
    message: str,
    coord_x: int,
    coord_y: int,
    wait_time: int = 10,
    tab_close: bool = True,
    close_time: int = 1,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}", 0)
    time.sleep(wait_time)
    # pg.click(WIDTH / 2, HEIGHT / 2)
    pg.click(WIDTH - coord_x, HEIGHT - coord_y)
    time.sleep(1)
    pg.press("enter")
    # time.sleep(5)
    logs.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        close_tab(wait_time=close_time)


def send_wha_msg(
    phone_no: str,
    message: str,
    time_hour: int,
    time_min: int,
    coord_x: int,
    coord_y: int,
    wait_time: int = 15,
    tab_close: bool = True,
    close_time: int = 3,
) -> None:
    """Send a WhatsApp Message at a Certain Time"""

    if not check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = dt.datetime.strptime(
        f"{time_hour}:{time_min}:00", "%H:%M:%S"
    ) - dt.datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    time.sleep(sleep_time)
    send_message(message=message, receiver=phone_no, coord_x=coord_x, coord_y=coord_y,  wait_time=wait_time)
    logs.log_message(_time=current_time, receiver=phone_no, message=message)
    if tab_close:
        close_tab(wait_time=close_time)

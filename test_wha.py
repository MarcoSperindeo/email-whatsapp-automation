import wha_gui as whagui
import time

# testing how much time it takes to send 1 wha msg via wha web on avg
# (time to open browser + wait time + time to close browser)
start_time = time.time()

msg = "Lorem ipsum dolor sit amet, \n consectetur adipiscing elit, \n" \
      "sed do eiusmod tempor incident ut labore et dolore magna aliqua. " \
      "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi " \
      "ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit " \
      "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
      "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " \
      "deserunt mollit anim id est laborum."
phone_num = '+39 xxx-xxxxxxx'

for i in range(2):
    whagui.instant_send_wha_msg(phone_num, msg, 150, 120, 12, True, 3)


print("--- Run time: %s seconds ---" % (time.time() - start_time))

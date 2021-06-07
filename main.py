from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re





def start_whatsapp():
    # driver.maximize_window()
    driver.get('https://web.whatsapp.com/')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]'))
    )

def format_chat(name):
    try:
        chat_text = driver.execute_script("return document.getElementsByClassName('_3XpKm _20zqk')")
    except:
        return
    formatted_chat = []
    for chat_ele in chat_text:
        main_text = chat_ele.text.split('\n')[:-1]
        if len(main_text):
            try:
                chat_target = driver.execute_script("return arguments[0].getElementsByTagName('span')[0].getAttribute('aria-label');", chat_ele)
            except:
                pass
            if chat_target != None:
                data = f'{chat_target} {main_text[-1]}'
            else:
                chat_target = main_text[0]
                if chat_target == 'You' or chat_target == name:
                    data = f'{chat_target} {main_text[-1]}'
                else:
                    try:
                        chat_target = driver.execute_script("return arguments[0].getElementsByClassName('copyable-text')[0].getAttribute('data-pre-plain-text');", chat_ele)
                        chat_target = chat_target.split(']')[1]
                    except:
                        chat_target = ''
                    data = f'{chat_target} {main_text[-1]}'
            formatted_chat.append(data)
    return formatted_chat


def get_chat_data(name):
    prevHeight = 0
    count = 0
    while True:
        driver.execute_script("document.getElementsByClassName('_1gL0z')[0].scrollTop -= 3000;")
        scrollHeight = driver.execute_script("return document.getElementsByClassName('_1gL0z')[0].scrollHeight")
        scrolling_stopped = driver.execute_script("return document.getElementsByClassName('_2tZna')")
        if scrolling_stopped:
            return format_chat(name)
        if prevHeight == scrollHeight:
            count += 1
        else:
            prevHeight = scrollHeight
            count = 0
        if count > 5:
            return format_chat(name)
        time.sleep(1)


def get_number_of_contact():
    driver.execute_script("document.getElementsByClassName('_2uaUb')[0].click()")
    chat_info = driver.execute_script("return document.getElementsByClassName('_2oUye')[0]").text
    if chat_info == 'Group info':
        return False

    time.sleep(1)
    phone_container = driver.execute_script("return document.getElementsByClassName('_2kOFZ')")
    if re.search('[a-zA-Z]', phone_container[4].text) == None:
        return phone_container[4].text
    return phone_container[5].text

def is_a_phone_number(text):
    if re.search('[a-zA-Z]', text):
        return False
    return True

def select_chat():
    data = []
    count = 0
    f = open("demofile2.txt", "w")
    while True:
        try:
            chats = driver.execute_script("return document.getElementsByClassName('_2aBzC')")
            for chat in chats:
                name = chat.text.split('\n')[0]
                key = "".join(chat.text.split('\n'))
                if key not in data:
                    actions = ActionChains(driver)
                    actions.move_to_element(chat).click().perform()
                    data.append(key)
                    count = 0
                    time.sleep(1)
                    phone = name
                    if not is_a_phone_number(name):
                        phone = get_number_of_contact()
                        driver.execute_script("document.getElementsByClassName('_27F2N')[0].click()")
                    if phone:
                        all_chats = get_chat_data(name)
                        print(phone, name)
                        f.write(f'{name} {phone}'+'\n')
                        for chat in all_chats:
                            f.write(chat + '\n')
                    time.sleep(1)
                else:
                    count += 1
            if count > 10 and count < 15:
                driver.execute_script("document.getElementById('pane-side').scrollBy(0, 200)")
            if count > 15:
                driver.quit()
                f.close()
                break
        except:
            pass


driver = webdriver.Chrome()
start_whatsapp()
select_chat()
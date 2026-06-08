import numpy as np
import keyboard
import easyocr
import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
import concurrent.futures
from PIL import ImageGrab

reader = easyocr.Reader(['en'])
g = [755,770,2450,880]

def popup(a,t):
    window = tk.Tk()
    window.geometry("1400x100+100+50")
    window.attributes("-topmost", True)
    tk.Label(window, text=a,font=("Arial", 15, "bold")).pack(pady=20)
    window.after(t*1000, window.destroy)
    window.mainloop()

def popup_out(pack):
    if not state:
        popup("closed",1)

    elif not pack:
        popup("No items found", 3)
        return
    
    _, letters, numbers = zip(*pack)

    window = tk.Tk()
    window.geometry("1400x100+100+50")
    window.attributes("-topmost", True)
    for i in range(len(letters)):
        window.grid_columnconfigure(i, weight=1)

    # First row
    for i, letter in enumerate(letters):
        tk.Label(window, text=letter, font=("Arial", 15, "bold")).grid(
            row=0, column=i, sticky="nsew"
        )

    # Second row
    for i, number in enumerate(numbers):
        tk.Label(window, text=number, font=("Arial", 15)).grid(
            row=1, column=i, sticky="nsew"
        )
    window.after(10000, window.destroy)
    window.mainloop()

def fetch_url(lx_cord,url):
# Using a with-statement ensures the connection is closed after each request
    price = 0
    with requests.get(url, timeout=5) as response:
        if response.status_code == 404:
            print("no price")
            price = "na"
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            for meta in soup.find_all("meta"):
                content = meta.get("content")
                if content and "Price:" in content:
                    match = re.search(r"Price:\s*(\d+)", content)
                    if match:
                        price = int(match.group(1))
                        
        return lx_cord,url,price
    
running = True
def stop():
    global running
    running = False
    popup("press p again to close",1)

keyboard.add_hotkey('q', stop)

while running:
    try:
        items = []
        popup("ready",5)
        keyboard.wait('p')
        screenshot = ImageGrab.grab(bbox = g)
        #screenshot = sct.grab(monitor)

        frame = np.array(screenshot)
        #cv2.imwrite("s.png",frame)
        results1 = reader.readtext(frame)

        for item in results1:
            box, text, conf = item
            avg_x = (box[0][0] + box[1][0])/2
            state = True
            for i in range(len(items)):
                if abs(items[i][0] - avg_x) <= 15:
                    items[i][1] = items[i][1]+" "+text
                    state = False

            if state:
                items.append([avg_x,text])
                
        #items.remove([0,0])

    ################
        p_s = []
        urls = []
        for i in range(len(items)):
            group = items[i]#get [avg_x,text]
            x_cord = group[0]
            word = group[1].replace(" ", "_")
            if not any(kw in text.lower() for kw in ("prime", "forma")):
                continue

            word = word.lower()
            url = "https://warframe.market/items/" + word +"?type=sell"
            urls.append((x_cord,url))

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(fetch_url, (x for x, _ in urls),(u for _, u in urls))

            for x_c,l_url,p in results:
                l_url = l_url.replace("https://warframe.market/items/","")
                l_url = l_url.replace("?type=sell","")
                p_s.append([x_c,l_url,p])

        finals = sorted(p_s, key=lambda x: x[0])
        popup_out(finals)

    except:
        break
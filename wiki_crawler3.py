import requests
from queue import Queue
import requests.compat
import numpy as np
import pickle

BASE_URL_href = "http://localhost:8080/vikidia_en_all_maxi_2023-09/A/"
BASE_URL_img = "http://localhost:8080/vikidia_en_all_maxi_2023-09/I/"

def from_to(text, str_start, str_end, start_search=0):
    start = text.find(str_start, start_search)
    end = text.find(str_end, start + len(str_start) + 1)
    if start != -1 and end != -1:
        return text[start:end+len(str_end)], end + len(str_end) + 1
    return None, 0

def get_language(HTML_text):
    HTML_tag = from_to(HTML_text, "<html", ">")[0]
    if HTML_tag is None:
        return None
    lang = from_to(HTML_tag, " lang=", "\"")[0][7:9]
    return lang

def is_image(link):
    for ext in (".webp", "png",".jpg",".jpeg", ".svg"):
        if link.endswith(ext): return True
    return False

def get_links(text):
    links = []
    hrefs = []
    link = None
    i = 0
    while i < len(text):
        link, i = from_to(text, "<a", ">", i)
        if link is not None:
            links.append(link)
            id = from_to(link, "id=\"", "\"")[0]
            if id is None or id.find("kiwix") == -1: # ignorira linkove koje je dodao Kiwix
                href = from_to(link, " href=", "\"")[0]
                # fragment_start = href.find("#")
                if href is not None:
                    href = href[7:-1]
                    if not href.startswith("http"): # izbjegava eksterne linkove, prati samo localhost
                        try:
                            fragment_start = href.find("#")
                            if fragment_start != -1:
                                href = href[:fragment_start] # uklanja fragment url-a
                            hrefs.append(requests.compat.urljoin(BASE_URL_href, href))
                        except Exception as e:
                            print(f"failed to resolve {href}: {e}")        
        else:
            break
    return hrefs

def get_images(text, page):
    hrefs = []
    link = None
    i = 0
    while i < len(text):
        link, i = from_to(text, "<img", ">", i)
        if link is not None:
            if True:
                href = from_to(link, " src=", "\"")[0]
                if href is not None:
                    href = href[7:-1]
                    if not href.startswith("http"): # izbjegava eksterne linkove, prati samo localhost
                        try:
                            hrefs.append(requests.compat.urljoin(page, href).replace("/A/I/", "/I/").replace("http://localhost:8080/I/", BASE_URL_img))
                        except Exception as e:
                            print(f"failed to resolve {href}: {e}")        
        else:
            break
    return hrefs

words_f = open("words.txt", "r")
words = {}
for line in words_f:
    words[line[:-1]] = [] # popis stranica koje imaju tu rijec
progress = 0
all_links = {}
open_queue = Queue(-1)
open_queue.put (BASE_URL_href + "Main_Page")
idx = 0
closed = {}
failed_to_get = set()
while not open_queue.empty():
    link = open_queue.get()
    if link in closed.keys() or link in failed_to_get:
        continue
    try:
        progress += 1
        if progress%50 == 0: print(progress)
        resp = requests.get(link)
        if resp.status_code not in (200, 304):
            resp = requests.get(link.replace("http://localhost:8080/A/", BASE_URL_href))
        if resp.status_code in (200, 304):
            closed[link] = idx
            idx += 1
            all_links[link] = []
            if is_image(link):
                continue # u slikama ne treba traziti linkove ni kljucne rijeci
            # print(f"crawling {link}")
            # trazi rijeci
            for word in resp.text.split():
                if word in words.keys():
                    words[word].append(link)
            # trazi linkove
            link_list = get_links(resp.text) + get_images(resp.text, link)
            for l in link_list:
                all_links[link].append(l)
                if l not in closed.keys() and l not in failed_to_get:
                    open_queue.put(l)
        else: 
            print(f"unexpected status code: {resp.status_code} for page {link}")
            failed_to_get.add(link)
    except:
        failed_to_get.add(link)
        print(f"failded to get {link}")

skoro_H = sorted([[len(v), k, v] for k, v in all_links.items()], reverse=True)
n = len(skoro_H)
for i in range(n):
    lista = skoro_H[i][2]
    lista2 = []
    for l in lista:
        if l in all_links.keys():
            lista2.append(l)
        else:
            skoro_H[i][0] -= 1
    skoro_H[i][2] = lista2
skoro_H.sort(reverse=True)

numeracija = {}
for i in range(n):
    numeracija[skoro_H[i][1]] = i
H = np.zeros(shape=(n, n))
k = n
for n_veza, parent, children in skoro_H:
    if n_veza == 0:
        k = numeracija[parent]
        print(k)
        break
    i = numeracija[parent]
    for ch in children:
        j = numeracija.get(ch)
        if j is not None:
            H[i][j] += 1
H1 = H[:k, :] / H[:k, :].sum(axis=1)[:,None]
H = np.vstack((H1, np.zeros((n-k, n))))
np.save(arr=H, file="H_matrix_vikidia2")
num_file = open("numeration2.txt", "wb")
pickle.dump(numeracija, num_file)
num_file.close()

for k in words:
    nums = [numeracija[ime] for ime in words[k]]
    words[k] = nums
search_file = open("search.txt", "wb")
pickle.dump(words, search_file)
search_file.close()

print(H.shape)
print(H)


# for i in skoro_H: print(i)
print(len(skoro_H))
print(len(closed))
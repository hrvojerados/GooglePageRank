import requests

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

def get_links(text):
    links = []
    hrefs = []
    link = None
    i = 0
    while i < len(text):
        link, i = from_to(text, "<a", ">", i)
        if link is not None:
            links.append(link)
            href = from_to(link, " href=", "\"")[0]
            if href is not None:
                href = href[7:-1]
                if href.startswith("//"):
                    href = "https:" + href
                elif href.startswith("/wiki"):
                    href = "https://en.vikidia.org" + href
                elif href.startswith("wiki"):
                    href = "https://en.vikidia.org/" + href
                if href.startswith("https://en.vikidia.org") or href.startswith("https://www.vikidia.org"):
                    hrefs.append(href)
        else:
            break
    return hrefs

links = set(["https://en.vikidia.org"])
headers = { "referer":"https://www.google.com/",
# "dnt":"1",
# "if-modified-since":"Thu, 12 Jun 2025 04:34:02 GMT",
# "priority":"u=0, i",
"sec-ch-ua":'"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
# "sec-ch-ua-mobile":"?0",
"sec-ch-ua-platform":"Windows",
# "sec-fetch-dest":"document",
# "sec-fetch-mode":"navigate",
# "sec-fetch-site":"none",
# "sec-fetch-user":"?1",
# "upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

for i in range(4):
    links2 = set()
    for link in links:
        print(f"crawling {link}")
        resp = requests.get(link, headers = headers)
        print(resp.status_code, resp.text)
        if resp.status_code in (200, 304) and get_language(resp.text) == "en":
            links2.update(get_links(resp.text))
        print(len(links2))
    links = links2
    print(len(links))
print(len(links))
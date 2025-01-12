from datetime import datetime
from bs4 import BeautifulSoup
from subprocess import run, CalledProcessError
from requests import get


BASE_URL = f"http://paper.people.com.cn/rmrb/pc/layout/"
IDM_PATH = "C://Program Files (x86)//Internet Download Manager//IDMan.exe"


def main():
    html_node = get_html_node(BASE_URL + get_date() + "node_01.html")
    file_url = get_file_url(BASE_URL + get_date() + html_node)
    download_with_idm(file_url)


def get_date(mode: int = 0) -> str:
    date = datetime.now()
    month = str(date.month) if date.month >= 10 else f"0{date.month}"
    day = str(date.day) if date.day >= 10 else f"0{date.day}"
    if mode == 1:
        return f"{date.year}-{month}-{day}"
    return f"{date.year}{month}/{day}/"


def get_html_node(url: str) -> str:
    response = get(url)
    if response.status_code != 200:
        raise ValueError(f"Can't get {url}")
    soup = BeautifulSoup(response.text, "lxml")
    html_node = str(soup.find_all('div', class_='swiper-slide')[-1])[36:48]
    return html_node


def get_file_url(url: str) -> str:
    response = get(url)
    if response.status_code != 200:
        raise ValueError(f"Can't get {url}")
    soup = BeautifulSoup(response.text, "lxml")
    file_url = str(soup.find_all('p', class_='right btn')[0])[70:132]
    return "http://paper.people.com.cn/rmrb/pc/" + file_url


def download_with_idm(url):
    # # Use IDM to download
    # command = [IDM_PATH, '/d', url]
    # try:
    #     run(command, check=True)
    # except CalledProcessError as error:
    #     print(f"Download Error: {error}")
    open(f"./{get_date(mode=1)}.pdf", "wb").write(get(url).content)


if __name__ == "__main__" :
    main()

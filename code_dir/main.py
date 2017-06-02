import code_dir.file_utils as file_utils
import os

PHANTOMJS_PATH = os.path.expandvars('${PHANTOMJS_DIR}/bin/phantomjs')
PHANTOMJS_LOGFILE = '/tmp/ghostdriver.log'

from selenium import webdriver
from bs4 import BeautifulSoup


def _download(url, out_file):
    try:
        driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,
                                     service_log_path=PHANTOMJS_LOGFILE)
        driver.set_window_size(1600, 900)
        driver.get(url)
        file_utils.write_file(out_file, driver.page_source.encode('utf8'))
        driver.quit()
    finally:
        os.remove(PHANTOMJS_LOGFILE)


def _get_links(soup, base_url):
    assert base_url.endswith('/')
    result = set([])
    for link in soup.find_all('a'):
        link_text = link.get('href')
        if not link_text:
            continue
        if link_text.startswith('javascript:'):
            continue
        if link_text.startswith('/'):
            link_text = base_url + link_text[1:]
        if link_text.startswith('#'):
            link_text = base_url + link_text
        if link_text.startswith('http'):
            result.add(link_text)
    return sorted(list(result))


def _save_content(soup, original_url, base_url, out_file):
    result = u'<html><head><meta charset="utf-8">'
    result += u'<title>Snapshot</title>'
    result += u'<style type="text/css">p.news '
    result += u'{color:#0000DD;font-size:200%;}</style>'
    result += u'</head><body style="background-color:#D0FFD0">'
    result += '<hr/>'
    if soup.title is None:
        return ''
    result += u'<h2>{}</h2>'.format(soup.title.string)
    for header_item in soup('h1'):
        result += u'<h1>{}</h1>'.format(
            header_item.get_text())
    for span_item in soup('span'):
        span_class = span_item.attrs.get('class', '')
        if 'publish_date' in span_class:
            result += u'<h2>{}</h2>'.format(span_item.get_text())
    result += '<h2><a href="{}" target="_blank">link</a></h2>'.format(
        original_url)
    for div_item in soup('div'):
        div_class = div_item.attrs.get('class', '')
        if 'articleBody' in div_class:
            result += u'<p class="news">{}</p>'.format(div_item.get_text())
    images = []
    for image_item in soup('img'):
        image_src = image_item.attrs.get('src', None)
        if image_src is None:
            continue
        if image_src.startswith('//'):
            image_src = 'http:' + image_src
        elif image_src.startswith('/'):
            image_src = base_url + image_src
        if not image_src.endswith('.png') and not image_src.endswith('.jpg'):
            continue
        if image_src in images:
            continue
        print(image_src)
        images.append(image_src)
    for image_src in images:
        result += '<p><img src="{}" width="60%"/></p>'.format(image_src)
    result = result.replace('Advertisement: Replay AdAds by ZINC', '')
    result += '</body></html>'
    file_utils.write_file(out_file, result.encode('utf8'))


def _download_links():
    out_file = os.path.expandvars('${CACHE_DIR}/temp.txt')
    base_url = 'http://www.anandabazar.com/'
    url = 'http://www.anandabazar.com/khela/'
    # _download(url, out_file)
    html_text = file_utils.read_file(out_file).decode('utf8')
    soup = BeautifulSoup(html_text, 'html.parser')
    print '\n'.join(_get_links(soup, base_url))


def _download_text():
    out_file = os.path.expandvars('${CACHE_DIR}/temp2.txt')
    out_html_file = os.path.expandvars('${CACHE_DIR}/temp3.html')
    base_url = 'http://www.anandabazar.com/'
    url = ('http://www.anandabazar.com/sport/gav'
           'askar-joins-the-coach-controversy-1.621592')
    url = ('http://www.anandabazar.com/supplementary/anandaplus'
           '/exclusive-interview-of-arpita-chatterjee-1.620330')
    # _download(url, out_file)
    html_text = file_utils.read_file(out_file).decode('utf8')
    soup = BeautifulSoup(html_text, 'html.parser')
    _save_content(soup, url, base_url, out_html_file)



def do_main():
    # _download_links()
    _download_text()

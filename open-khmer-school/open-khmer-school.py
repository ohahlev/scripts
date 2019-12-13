import os
import requests
import time
import zipfile
from fontTools.ttLib import TTFont
from pathlib import Path
from shutil import move


# repo
OPEN_KHMER_SCHOOL_ZIP = "https://github.com/OpenInstituteCambodia/open-khmer-school/archive/master.zip"

def download_file(url):
    local_filename = '/tmp/%s' % url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename
    
def unzip_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('/tmp/')

def install_fonts(font_dir):
    home = str(Path.home())
    user_font_dir = '%s/.fonts' % (home)
    if not os.path.isdir(user_font_dir):
        os.mkdir(user_font_dir)
    font_list = os.listdir(font_dir)
    for font in font_list:
        print('installing %s into %s' % (font, user_font_dir))
        ttfFont = TTFont('%s/%s' % (font_dir, font))
        ttfFont.save('%s/%s' % (user_font_dir, font))
        time.sleep(1)

def copy_font_config():
    font_conf_dir = '/etc/fonts/conf.d'
    khmer_font_conf = '65-khmer.conf'
    khmer_font_conf_path = '%s/%s' % (font_conf_dir, khmer_font_conf)
    bak_conf_path = '%s/%s_bak' % (font_conf_dir, khmer_font_conf)
    if os.path.isfile(khmer_font_conf_path):
        os.system('sudo mv %s %s' % (khmer_font_conf_path, bak_conf_path))
    os.system('sudo cp %s %s' % (khmer_font_conf, font_conf_dir))

def clean_up():
    tmp_master_zip = '/tmp/master.zip'
    tmp_extracted_master_zip = '/tmp/open-khmer-school-master'
    if os.path.isfile(tmp_master_zip):
        os.system('sudo rm -rf %s' % tmp_master_zip)
    if os.path.isdir(tmp_extracted_master_zip):
        os.system('sudo rm -rf %s' % tmp_extracted_master_zip)

zip_file = download_file(OPEN_KHMER_SCHOOL_ZIP)
unzip_file(zip_file)
install_fonts('/tmp/open-khmer-school-master/fonts/Normal')
copy_font_config()
clean_up()

import speedtest
import time

import requests
from bs4 import BeautifulSoup

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# --------------------- Getting Speed Data ---------------------

def get_servers():
    """
    Finds all relevant servers (in this case, from Tel Aviv)
    Requires requests and BeautifulSoup.
    Future: move cc/name as args and other criteria as optional args
    
    """
    
    r = requests.get('http://c.speedtest.net/speedtest-servers-static.php')
    soup = BeautifulSoup(r.text, "lxml")
    
    servers = []
    
    for i in soup.find_all(attrs={'cc':'GB', 'name':"London"}):
        servers.append(int(i.get('id')))
        
    return servers
    

def run_test(servers):
    """
    Based on docs: https://github.com/sivel/speedtest-cli/wiki
    """
    
    try:
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()
        s.results.share()

        results_dict = s.results.dict()
        results_dict['test_status'] = 1  # 1  == OK

        return results_dict
    
    except Exception as e:
        return {'download':0, 'timestamp':0, 'ping':0, 'upload':0, 'server':{'id':0, 'sponsor':0}, 'test_status': e}
    
    
    
def parse_results(results_dict):
    """
    Speed test returns a dict. Writing to google sheets with gspread requires a list.
    This function takes the result_dict from run_test() and returns a list.
    """
    
    return [results_dict['timestamp'], results_dict['ping'], results_dict['download'], results_dict['upload'], results_dict['server']['id'], results_dict['test_status']]



# --------------------- Writing to Google Sheet ---------------------


def get_creds(json_loc):
    """
    Gets authentication credentials.
    
    json_loc: path+filename of the credentials json.
    """
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_loc, scope)
    
    return credentials



def gsheet_connect(credentials):
    """
    Connects to google.
    """
    
    # reading material on scope: https://stackoverflow.com/a/10588651/5056689
    
    global gc
    gc = gspread.authorize(credentials)

    
    
def gsheet_open(sprdname='gsheet_test', shtname='SpeedLog'):
    """
    'Opens' a specific sheet in a workbook for editing.
    
    sprdname: spreadsheet name, str
    shtname: sheet name in that spreadsheet, str
    """
    
    global wks
    
    sht = gc.open(sprdname)
    wks = sht.worksheet(shtname)

    
    
def append_row(row):
    """
    row: list of values
    """
    wks.append_row(row)

    


# --------------------- Putting It All Together ---------------------


def main(json_loc, n_samples, sleeptime):
    """
    
    n_samples: number of times to sample the network, int
    sleeptime: number of seconds to wait between speed tests, int
    """
    
    servers = get_servers()    
    
    
    credentials = get_creds(json_loc)
    
    gsheet_connect(credentials)
    
    gsheet_open(sprdname='gsheet_test', shtname='SpeedLog')
    
    
       
    for i in range(n_samples):
    	print '\r Running test %d of %d' %(i+1, n_samples),

        results_dict = run_test(servers)
        append_row(parse_results(results_dict))
        


json_loc = 'assets/speedtracker.json'
main(json_loc, 20, 120)


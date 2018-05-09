import speedtest
import time

import requests
from bs4 import BeautifulSoup

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# --------------------- Getting Speed Data ---------------------

def get_servers(attrs_dict):
    """
    Finds server ids for all relevant servers.
    Requires requests and BeautifulSoup.
    
    attrs_dict: dictionary with attributes (keys) and their values to 
    filter the list of servers by. Available attributes include: 
    name - city name, country - country name, cc - two letter country code, sponsor, id et al.
    """
    
    r = requests.get('http://c.speedtest.net/speedtest-servers-static.php')
    soup = BeautifulSoup(r.text, "lxml")
    
    servers = []
    
    for i in soup.find_all(attrs=attrs_dict):
        servers.append(int(i.get('id')))
        
    return servers
    

def run_test(servers):
    """
    Runs the speed test and returns a dictionary of results.
    test_status (key): indicates whether speed test was run successfully (value = 1) or not (value = 0).
    Based on docs: https://github.com/sivel/speedtest-cli/wiki

    servers: list of server ids, the output of get_servers().
    """
    
    # TO DO: check that servers is a list, check all values are ints


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

    
    
def gsheet_open(sprdname, shtname):
    """
    'Opens' a specific sheet in a workbook for editing.
    
    sprdname: spreadsheet name, str
    shtname: sheet name in that spreadsheet, str
    """
    
    # TO DO: handle non existing spreadsheets / sheetnames

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
    
    servers = get_servers({'cc':'GB', 'name':"London"})    
    
    
    credentials = get_creds(json_loc)
    
    gsheet_connect(credentials)
    
    gsheet_open(sprdname='gsheet_test', shtname='SpeedLog')
    
    
       
    for i in range(n_samples):
    	print '\r Running test %d of %d' %(i+1, n_samples),

        results_dict = run_test(servers)
        append_row(parse_results(results_dict))
        


json_loc = 'your_json_file.json'
main(json_loc, 2, 120)


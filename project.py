from bs4 import BeautifulSoup
import requests
import csv

start = 'https://www.floridagators.com/sports/'
page = requests.get(start)
soup = BeautifulSoup(page.text, 'html.parser')

sportnames = ['football', 'baseball', 'womens-basketball', 'mens-basketball', 'mens-golf', 'womens-golf', 'womens-gymnastics', 'womens-lacrosse', 'womens-soccer', 'softball', 'mens-swimming-and-diving', 'womens-swimming-and-diving', 'mens-tennis', 'womens-tennis', 'track-and-field', 'volleyball']
team_url = 'https://www.floridagators.com/sports/football/roster'
def scrape_one_team (team_url):
    page = requests.get(team_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    names = soup.find_all('td', class_='sidearm-table-player-name')
    try:
        places = soup.find_all('td', class_='hometownhighschool')
    except:
        pass
    if(soup.find('td', class_='hometownprevious')):
        track_places = soup.find_all('td', class_ = 'hometownprevious')
        for track in track_places:
            places.append(track)

    count = 0
    master_list = []
    for name in names:
        players_details = []
        players_details.append(name.text)
        hometown = places[count].text.split(' / ')
        players_details.append(hometown[0])
        count += 1
        master_list.append(players_details)
    return master_list

def write_csv(sportnames):
    csvfile = open('hometowns.csv', 'w', newline='', encoding='utf-8')
    c = csv.writer(csvfile)
    c.writerow( ['name','hometown', 'sport'] )
    for sportname in sportnames:
        url = 'https://floridagators.com/sports/' + str(sportname) + '/roster'
        fill = scrape_one_team(url)
        for i in range (len(fill)):
            fill[i].append(sportname)
            c.writerow(fill[i])
    csvfile.close()
write_csv(sportnames)

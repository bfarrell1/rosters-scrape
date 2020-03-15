# Scraping UF Athletics Rosters
## Objective
The goal of this scraping project was to successfully scrape every varsity team roster at the University of Florida to find every athletes' name and hometown. This way, this information can easily be used to do something like map where UF recruits its athletes from overall and by sport.
## Steps
After importing everything, I found all of the partial URLs for all of the teams. It's pretty simple because they are pretty much just "(sport)/roster". This can be done by hand and in just a few minutes.
Next, I built my scraper. I used the football roster as an example to make sure everything worked.
```
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
```
This is the first half of my scraper. The list `sportnames` includes all of the partial URLs that I am using to scrape. I used the football roster as a test. The function `scrape_one_team` is what scrapes the roster. `names` finds all of the names held in the table on the page (note: this is using the HTML for when the roster page is set to the grid view), while `places` finds all of the hometowns.
The code is complicated by the fact that the track and field rosters for both teams are on the same page and use a different class for the hometown called `hometownprevious`. The try/except and if statements allow the scraper to still scrape the track page despite the change in the class name.
```
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
```
This is the second half of the scraper. From here, the scraper finds the names through `name.text` and appends it to the empty list `players_details`. The hometowns are a little more difficult because the high schools are in the same cell. Using `split(' / ')`, the text is split at the slash that separates the hometown from the high school on the page. `hometown[0]` collects only the hometown and not the high school.
The rest of the code results in getting three things per player inside `players_details`: player name, hometown and sport. It returns that to `master_list`, another empty list, in the form of `[name, hometown, sport]`. It does that for every player on a team.  
```
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
```
From here, all that's left to do is to write this information to a .csv file, so I created the function `write_csv(sportnames)`. This function creates a new .csv file and then writes a row per player. Then, the for-loop loops every sport through the scraper. Because the scraper produces a list where every row is an item in the list, `for i in range(len(fill))` writes a row for every player on every team. After that, I closed the .csv file and called the function.
## Issues
I had a lot of difficulty with this. I didn't expect the track and field teams to have a different td class on their hometowns, so I had to use try and except to fix that. I also didn't foresee the volleyball roster URL defaulting to this spring's roster instead of last season's, so I ended up using the one for next season. It was also difficult to get the name, hometown and sport into one list to write into the csv file, but using two lists in the scraper solved that. 

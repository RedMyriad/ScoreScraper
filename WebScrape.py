# Francisco Lopez
# 12/28/2017
# Purpose: Scrape NFL site for scores

from bs4 import BeautifulSoup as soup
from urllib import request as req
import datetime as date


def open_client(year, week):

    cur_year = date.date.today().year

    # check for year and week being under limit
    if year >= 2001 and week >= 1:
        # check for year being over limit
        if year <= cur_year and week <= 16:

            year = str(year)
            week = str(week)
            url = 'http://www.nfl.com/scores/'
            page_url = url + year + '/' + 'REG' + week

            # request html page
            client = req.Request(page_url)
            nfl_req = req.urlopen(client)
            nfl_page = nfl_req.read()

            # close connection
            nfl_req.close()
            return nfl_page
        else:
            return 'Year/Week out of Bounds'
    else:
        return 'Year/Week out of Bounds'


def get_data(page, csv_save, printable):

    file = open(csv_save, 'w')
    headers = 'date, network, teams, scores\n'
    file.write(headers)

    page_soup = soup(page, 'html.parser')

    # tag - <div class="scorebox-wrapper'>
    scores = page_soup.find_all('div', {'class': 'scorebox-wrapper'})

    for score_data in scores:

        # tag - <span class="date"....>
        date = score_data.find('span', {'class': 'date'}).text

        # tag - <span class="network"....>
        network = score_data.find('span', {'class': 'network'}).text

        # tag - <p class="team-name">
        team1 = score_data.find_all('p', {'class': 'team-name'})[0].text
        team2 = score_data.find_all('p', {'class': 'team-name'})[1].text
        teams = team1 + ' vs. ' + team2

        score1 = score_data.find_all('p', {'class', 'total-score'})[0].text
        score2 = score_data.find_all('p', {'class', 'total-score'})[1].text
        scores = score1 + ' to ' + score2

        if printable == 'y':
            print('Date: ' + date + '\n' +
                  'Network: ' + network + '\n' +
                  'Teams: ' + teams + '\n' +
                  'Score: ' + scores + '\n')
        else:
            file.write(date.replace(',', '  /') + ',' + network + ',' + teams + ',' + scores + ' \n')

    file.close()


if __name__ == '__main__':

    # scores will be save in this file if they chose to not see the scores
    csv_file = 'Nfl_scores.csv'

    # get user input / format input
    input_year = input("What year would you like to see? ")
    input_year = int(input_year)
    input_week = input("What week in " + str(input_year) + "'s season would you like to see? ")
    input_week = int(input_week)

    to_print = input("Would you like to see the scores printed out on the screen?(y/n) ")
    to_print = to_print.lower()

    # validate user input
    if to_print == 'y':
        print("Okay, your scores shall be printed momentarily. \n \n")
        print('SEASON: ' + str(input_year) + '\tWEEK: ' + str(input_week) + '\n')
    elif to_print == 'n':
        print("Okay the scores shall be printed onto a csv file.")
    else:
        print("Your input was invalid so the scores will be sent to a csv file.")

    # get nfl scores html page
    page = open_client(input_year, input_week)
    # scrape relevant info from page and make presentable
    get_data(page, csv_file, to_print)

    # give user confirmation
    if to_print != 'y':
        print('The scores have been sent to a csv file named ' + csv_file)

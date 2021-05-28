from flask import render_template, redirect, current_app as app, jsonify, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from .models import Player
from bs4 import BeautifulSoup
from math import floor

@app.route('/', methods=['GET'])
def index():
    def get_player_data(player_name):
        print('Beginning web scraping...')
        
        driver = webdriver.Chrome('./chromedriver')
        driver.get('https://nbastuffer.com')

        sleep(3)

        link_to_click = driver.find_elements_by_class_name('x-recent-post6')[3]
        link_to_click.click()

        sleep(5)

        search_field = driver.find_element_by_tag_name('input')
        search_term = player_name
        search_field.send_keys(search_term)

        # BeautifulSoup functionality begins
        page = requests.get(driver.current_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tbody = soup.find('tbody', class_='row-hover')

        player_list = [tr for idx, tr in enumerate(list(tbody.children)) if idx%2!=0]
        for idx, p in enumerate(player_list):
            stats_list = list(p.children)[1:-2]
            player_name = stats_list[1].text
            if player_name == search_term:
                # player_data = p
                break
        s = stats_list
        p = Player(
            name=s[1].text,
            team=s[2].text,
            position=s[3].text,
            age=floor(float(s[4].text)),
            games_played=int(s[5].text),
            minutes_per_game=float(s[6].text),
            ft_attempts=int(s[10].text),
            ft_percentage=float(s[11].text),
            tp_attempts=int(s[12].text),
            tp_percentage=float(s[13].text),
            th_attempts=int(s[14].text),
            th_percentage=float(s[15].text),
            points_per_game=float(s[18].text),
            rebounds_per_game=float(s[19].text),
            assists_per_game=float(s[21].text),
            steals_per_game=float(s[23].text),
            blocks_per_game=float(s[24].text),
            turnovers_per_game=float(s[25].text)
        )
        driver.close()
        p.save()
        print('Web scraping complete...')
    get_player_data('LeBron James')
    sleep(30)
    return redirect(url_for('index'))
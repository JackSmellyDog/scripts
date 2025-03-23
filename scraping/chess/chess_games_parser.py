import time
import json
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.chromium.webdriver import RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraping.core.scraping_core import execute_webdriver_task

BASE_URL = 'https://www.chess.com'
LOGIN_URL = BASE_URL + '/login'

LOGIN = 'YOUR_LOGIN'
PASSWORD = 'YOUR_PASS'
NICKNAME = 'YOUR_NICKNAME'.lower()
GAME_OWNER = 'my_game'

LOGIN_INPUT_XPATH = "//input[@id='username']"
LOGIN_BUTTON_XPATH = "//button[@id='login']"
PASS_INPUT_XPATH = "//input[@id='password']"

GAME_ROW_XPATH = "//table[contains(@class, 'archive-games-table')]//tbody//tr"

GAME_TIME_CONTROL_XPATH = ".//*[contains(@class, 'archive-games-game-time')]"
GAME_LINK_XPATH = ".//a[contains(@href, 'chess.com/game/live')]"
GAME_RESULT_XPATH = ".//*[contains(@class, 'archive-games-result-icon')]"

OPPONENT_XPATH = f".//a[contains(@href, 'chess.com/member/') and not (contains(@href, '{NICKNAME}'))]"
OPPONENT_RATING_XPATH = OPPONENT_XPATH + "//following-sibling::span[contains(@class, 'user-tagline-rating')]"
OPPONENT_COUNTRY_XPATH = OPPONENT_XPATH + "//following-sibling::*[contains(@class, 'country-flags')]"


@dataclass(frozen=True)
class Opponent:
    nick: str
    rating: str
    country: str


@dataclass(frozen=True)
class ChessGame:
    id: str
    time_control: str
    result: str
    date: str
    opponent: Opponent

    def __eq__(self, other):
        if isinstance(other, ChessGame):
            return self.id == other.id
        return False


@dataclass(frozen=True)
class ParseError:
    page: int


@dataclass(frozen=True)
class Credentials:
    login: str
    password: str


def main():
    credentials = Credentials(login=LOGIN, password=PASSWORD)
    all_games = set()
    start_page = 1

    while True:
        games, error = parse_games(start_page=start_page, credentials=credentials)
        all_games.update(games)

        if error is None:
            break
        else:
            start_page = error.page

    print(all_games)
    final_json = '[' + ','.join([chess_game_to_json(game) for game in all_games]) + ']'

    with open('chess-games.json', 'w') as f:
        f.write(final_json)


def chess_game_to_json(game: ChessGame) -> str:
    return json.dumps(game.__dict__, default=lambda o: o.__dict__)


@execute_webdriver_task
def parse_games(wd: RemoteWebDriver, start_page, credentials) -> tuple[set, ParseError]:
    login(wd, credentials)
    wait = WebDriverWait(wd, 10)

    games = set()
    page: int = start_page
    error: ParseError | None = None

    try:
        while True:
            time.sleep(1)
            wd.get(build_archive_url(page))
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, GAME_ROW_XPATH)))

            number_of_games_before = len(games)

            for element in elements:
                game_link = element.find_element(By.XPATH, GAME_LINK_XPATH).get_attribute('href')
                game_id = game_link.split('/')[-1]

                time_control = element.find_element(By.XPATH, GAME_TIME_CONTROL_XPATH).text
                result = element.find_element(By.XPATH, GAME_RESULT_XPATH).get_attribute('v-tooltip')
                date = element.text.split('\n')[-1]

                opponent_link = element.find_element(By.XPATH, OPPONENT_XPATH).get_attribute('href')
                nick = opponent_link.split('/')[-1]

                opponent_rating = element.find_element(By.XPATH, OPPONENT_RATING_XPATH).text.replace('(', '').replace(')', '')
                opponent_country = element.find_element(By.XPATH, OPPONENT_COUNTRY_XPATH).get_attribute('v-tooltip')

                opponent = Opponent(nick=nick, rating=opponent_rating, country=opponent_country)
                game = ChessGame(id=game_id, time_control=time_control, result=result, date=date, opponent=opponent)

                games.add(game)

            if number_of_games_before == len(games):
                print("No new games found! Stopping.")
                break

            print(f"Page: {page} is complete")

            page = page + 1
    except Exception as e:
        print(e)
        error = ParseError(page)

    return games, error


def build_archive_url(page: int, base_url=BASE_URL, game_owner=GAME_OWNER):
    return f'{base_url}/games/archive?gameOwner={game_owner}&page={page}'


def login(wd: RemoteWebDriver,
          credentials: Credentials,
          login_url=LOGIN_URL,
          login_xpath=LOGIN_INPUT_XPATH,
          login_button_xpath=LOGIN_BUTTON_XPATH,
          pass_xpath=PASS_INPUT_XPATH):
    wait = WebDriverWait(wd, 10)
    wd.get(login_url)

    wait.until(EC.presence_of_element_located((By.XPATH, login_xpath))).send_keys(credentials.login)
    wait.until(EC.presence_of_element_located((By.XPATH, pass_xpath))).send_keys(credentials.password)
    wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()

    time.sleep(3)


if __name__ == '__main__':
    main()


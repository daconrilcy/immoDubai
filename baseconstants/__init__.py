# Liste des constantes utilisées dans le programme

DEFAULT_FOLDER = "recherche appart dubai"
DEFAULT_PATH = "C:\\Users\\Cyril CONDAMINE\\Desktop\\" + DEFAULT_FOLDER + "\\"
PHOTOS_FOLDER = "Photos"
PATH_REP_PHOTOS = DEFAULT_PATH + PHOTOS_FOLDER + "\\"
BASE_HYPERLINK = '=LIEN_HYPERTEXTE("'
FOLDER_DB = 'db_base'
PATH_FOLDER_DB = DEFAULT_PATH + "\\" + FOLDER_DB + "\\"

# DB
DB_GPS_FILE = "gps.csv"
DB_CITIES_FILE = "cities.csv"

# Constantes BlueGround
BLUEGROUND_FOLDER = "blueground"
PATH_FOLDER_BG = DEFAULT_PATH + BLUEGROUND_FOLDER + "\\"
PATH_PHOTOS_FOLDER_BG = PATH_FOLDER_BG + PHOTOS_FOLDER + "\\"
BASE_URL_BLUEGROUND = "https://www.theblueground.com/api/furnished-apartments-dubai-uae?currency=AED&language=en" \
                      "&offset=1"

# Constantes Currencies
AED_IN_EURO = 0.27
USD_IN_EURO = 1.01
PATH_REP_HISTORY_FILE = 'currency/history_files/'
URL_CONVERSION_BOURSORAMA = "https://www.boursorama.com/bourse/devises/convertisseur-devises/convertir?"

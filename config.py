HOST='irc.twitch.tv'
PORT=6667
NICK="spot1ight"
PASS="oauth:52w2ijbv87pme55reorvp5y55cvwoi"
CHAN="snakecase" # "upalanapol"

DB_HOST="localhost"
DB_USER="root"
DB_PASS="qwerty123456"
DB_SCHEME="mydb"

viewers = {}
START_POINTS = 100

# attention, if you change it, change enum in BD
type_viewer = ['moderators', 'staff', 'admins', 'global_mods', 'viewers']

# livewbot
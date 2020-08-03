PDP_API_ENDPOINT_URI = "http://localhost:3000/api"
DATABASE_URI = "postgres+psycopg2://irtk:irtk@localhost:5432/irtk"

# The transaction rate threshold for a blockchain to satisfy the Filter.FAST criterion. Only
# blockchains with a transaction rate euqal or higher than this threshold are considered fast.
MIN_TX_RATE = 4

# The transaction cost threshold for a blockchain to satisfy the Filter.CHEAP criterion. Only
# blockchains with a transaction cost equal or lower than this threshold are considered cheap.
MAX_TX_COST = 1

# The popularity threshold for a blockchain to satisfy the Filter.POPULAR criterion. Only
# blockchains with a popularity equal or higher than this threshold are considered popular.
MIN_POPULARITY = 0.5

# The stability threshold for a blockchain to satsify the Filter.STABLE creterion. Only blockchains
# with a popularity equal or higher than this threshold are considered stable.
MIN_STABILITY = 0.5

# The timeframe values can be configured. The expected format is "HH:MM", where HH specifies the
# hours and MM and specifies the minutes, respectively. The "day" timeframe lasts from DAY_START to
# NIGHT_START, the "night" timeframe lasts from NIGHT_START to DAY_START, the "morning" timeframe
# lasts from DAY_START to AFTERNOON_START, and the "afternoon" timeframe lasts from AFTERNOON_START
# to NIGHT_START, respectively.
TIME_DAY_START = "06:00"
TIME_AFTERNOON_START = "12:00"
TIME_NIGHT_START = "18:00"

import logging as log

BLACKJACK = 21
DEALER_THRESHOLD = 17
CUT = 60
INTEGER_INF = 9999999999999999999999999999999999
DEBUG = True

log.getLogger().setLevel(log.INFO if not DEBUG else log.DEBUG)

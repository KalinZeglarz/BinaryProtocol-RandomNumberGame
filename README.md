# BinaryProtocol-RandomNumberGame

## How to run
Note: Application default needs Python2.7 to work properly as it was testet at this version

To run as server: `python main.py -a server_ip -S` <br>
To run as client: `python main.py -a server_ip -S`

If address and mode are not supplied, the default values are `127.0.0.1`(localhost) and application ask about working mode.

## help
<pre>
usage: main.py [-h] [-a ADDR] [-S] [-C]
optional arguments:
  -h, --help            show this help message and exit
  -a ADDR, --addr ADDR  valid ip address for working
  -S, --server          working as server
  -C, --client          working as client
</pre>

## TCP Segment description

<pre>
OPERATION TYPE  |   ANSWER  |   ID token   |  Complement bits
00000               0000        000           0000
5 bits              4 bits      3 bits        4 bits

:16 bits per segment
</pre>

OPERATION TYPES (OPERTION FLAG - BINARY NUMBER AS DECIMAL - DESCRIPTION):
<ul>
    <li>GET_ID - 1 - Flag used to get ID token from server,</li>
    <li>SEND_ID - 2 - Flag used by server to send ID token to client,</li>
    <li>TRIES - 4 - Number of tries left to the end of game,</li>
    <li>GUESS - 8 - Guessing try (used when client try to guess secret number),</li>
    <li>RESULT - 16 - Used to inform client about winning the game,</li>
    <li>GET_ID_TRIES - 5 - Flag combo used by client to get form server ID token and tries in one single query,</li>
    <li>SEND_ID_TRIES - 6 - Flag combo used by server to inform client about tries left and to send ID token.</li>
<li>

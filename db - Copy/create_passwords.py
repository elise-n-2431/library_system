import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  
a=generate_password_hash('4')
print(a)

s=check_password_hash('pbkdf2:sha256:150000$uVZgLF7o$d8dda4d8548dc27efc84b285146a714fdeb1f121257702e434de6c01f2d784dc','4')
print(s)
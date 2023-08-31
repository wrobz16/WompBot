import os

import os

def load_token():
    with open("token.txt", "r") as file:
        return file.readline().strip()

def load_prefix():
    with open("prefix.txt", "r") as file:
        return file.readline().strip() + " "

TOKEN = load_token()
PREFIX = load_prefix()

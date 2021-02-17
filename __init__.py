from flask import *
from requests import get, post
from bs4 import BeautifulSoup as bs
import os, math, json, random, re, base64, time, smtplib
import pymysql.cursors

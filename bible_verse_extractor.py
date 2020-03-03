#! /usr/bin/env python3

import requests
import bs4 as bs
import re
import csv

codePattern = re.compile('(?<=\().{3}(?:_.{2,3})?(?=\))')
translationPattern = re.compile(r'(?<=versions/)(\d+?)\b')

bibleBooks = {'genesis': 'GEN', 'exodus': 'EXO', 'leviticus': 'LEV', 'numbers': 'NUM', 'deuteronomy': 'DEU', 'joshua': 'JOS', 'judges': 'JDG', 'ruth': 'RUT',
              '1 samuel': '1SA', '2 samuel': '2SA', '1 kings': '1KI', '2 kings': '2KI', '1 chronicles': '1CH', '2 chronicles': '2CH', 'ezra': 'EZR',
              'nehemiah': 'NEH', 'esther': 'EST', 'job': 'JOB', 'psalms': 'PSA', 'proverbs': 'PRO', 'ecclesiastes': 'ECC', 'song of solomon': 'SNG',
              'isaiah': 'ISA', 'jeremiah': 'JER', 'lamentations': 'LAM', 'ezekiel': 'EZK', 'daniel': 'DAN', 'hosea': 'HOS', 'joel': 'JOL', 'amos': 'AMO',
              'obadiah': 'OBA', 'jonah': 'JON', 'micah': 'MIC', 'nahum': 'NAM', 'habakkuk': 'HAB', 'zephaniah': 'ZEP', 'haggai': 'HAG', 'zechariah': 'ZEC',
              'malachi': 'MAL', 'matthew': 'MAT', 'mark': 'MRK', 'luke': 'LUK', 'john': 'JHN', 'acts': 'ACT', 'romans': 'ROM', '1 chorinthians': '1CO',
              '2 chorinthians': '2CO', 'galatians': 'GAL', 'ephesians': 'EPH', 'philippians': 'PHP', 'collosians': 'COL', '1 thessalonians': '1TH',
              '2 thessalonians': '2TH', '1 timothy': '1TI', '2 timothy': '2TI', 'titus': 'TIT', 'philemon': 'PHM', 'hebrews': 'HEB', 'james': 'JAS',
              '1 peter': '1PE', '2 peter': '2PE', '1 john': '1JN', '2 john': '2JN', '3 john': '3JN', 'jude': 'JUD', 'revelation': 'REV', 'tobit': 'TOB',
              'judith': 'JDT', 'wisdom of solomon': 'WIS', 'sirach': 'SIR', 'baruch': 'BAR', 'letter of jeremiah': 'LJE',
              'prayer of azariah (and hymn of the three young men)': 'S3Y', 'susanna': 'SUS', 'bel and the snake': 'BEL', '1 maccabees': '1MA',
              '2 maccabees': '2MA', '1 esdras': '1ES', 'prayer of manasseh': 'MAN', 'psalm 151': 'PS2', '3 maccabees': '3MA', '2 esdras': '2ES', '4 maccabees': '4MA'}
#Book of Esther (Greek) has odd chapter numbering in several (many?) translations
#esther = ['Chapter 200: Mordecai’s dream', 'Chapter 1: Queen Vashti', 'Chapter 2: Finding a new queen', 'Chapter 3: Haman plans to destroy Mordecai', 'Chapter 201: Artaxerxes’ decree', 'Chapter 3 part 2', 'Chapter 4: A crisis for the Jews', 'Chapter 202: Mordecai and Esther pray for deliverance', 'Chapter 203: Esther appears before the king', 'Chapter 5: Esther acts', 'Chapter 6: Honor for Mordecai', 'Chapter 7', 'Chapter 8: Esther acts again', 'Chapter 204: Artaxerxes’ second decree', 'Chapter 8 part 2', 'Chapter 9: The fateful day', 'Chapter 10: The fame of Artaxerxes and Mordecai', 'Chapter 205: Mordecai interprets his dream'}
bibleStats = {'GEN': {1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32, 11: 32, 12: 20, 13: 18, 14: 24, 15: 21, 16: 16, 17: 27, 18: 33, 19: 38, 20: 18, 21: 34, 22: 24, 23: 20, 24: 67, 25: 34, 26: 35, 27: 46, 28: 22, 29: 35, 30: 43, 31: 55, 32: 32, 33: 20, 34: 31, 35: 29, 36: 43, 37: 36, 38: 30, 39: 23, 40: 23, 41: 57, 42: 38, 43: 34, 44: 34, 45: 28, 46: 34, 47: 31, 48: 22, 49: 33, 50: 26}, 'EXO': {1: 22, 2: 25, 3: 22, 4: 31, 5: 23, 6: 30, 7: 25, 8: 32, 9: 35, 10: 29, 11: 10, 12: 51, 13: 22, 14: 31, 15: 27, 16: 36, 17: 16, 18: 27, 19: 25, 20: 26, 21: 36, 22: 31, 23: 33, 24: 18, 25: 40, 26: 37, 27: 21, 28: 43, 29: 46, 30: 38, 31: 18, 32: 35, 33: 23, 34: 35, 35: 35, 36: 38, 37: 29, 38: 31, 39: 43, 40: 38}, 'LEV': {1: 17, 2: 16, 3: 17, 4: 35, 5: 19, 6: 30, 7: 38, 8: 36, 9: 24, 10: 20, 11: 47, 12: 8, 13: 59, 14: 57, 15: 33, 16: 34, 17: 16, 18: 30, 19: 37, 20: 27, 21: 24, 22: 33, 23: 44, 24: 23, 25: 55, 26: 46, 27: 34}, 'NUM': {1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36, 11: 35, 12: 16, 13: 33, 14: 45, 15: 41, 16: 50, 17: 13, 18: 32, 19: 22, 20: 29, 21: 35, 22: 41, 23: 30, 24: 25, 25: 18, 26: 65, 27: 23, 28: 31, 29: 40, 30: 16, 31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13}, 'DEU': {1: 46, 2: 37, 3: 29, 4: 49, 5: 33, 6: 25, 7: 26, 8: 20, 9: 29, 10: 22, 11: 32, 12: 32, 13: 18, 14: 29, 15: 23, 16: 22, 17: 20, 18: 22, 19: 21, 20: 20, 21: 23, 22: 30, 23: 25, 24: 22, 25: 19, 26: 19, 27: 26, 28: 68, 29: 29, 30: 20, 31: 30, 32: 52, 33: 29, 34: 12}, 'JOS': {1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35, 9: 27, 10: 43, 11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10, 17: 18, 18: 28, 19: 51, 20: 9, 21: 45, 22: 34, 23: 16, 24: 33}, 'JDG': {1: 36, 2: 23, 3: 31, 4: 24, 5: 31, 6: 40, 7: 25, 8: 35, 9: 57, 10: 18, 11: 40, 12: 15, 13: 25, 14: 20, 15: 20, 16: 31, 17: 13, 18: 31, 19: 30, 20: 48, 21: 25}, 'RUT': {1: 22, 2: 23, 3: 18, 4: 22}, '1SA': {1: 28, 2: 36, 3: 21, 4: 22, 5: 12, 6: 21, 7: 17, 8: 22, 9: 27, 10: 27, 11: 15, 12: 25, 13: 23, 14: 52, 15: 35, 16: 23, 17: 58, 18: 30, 19: 24, 20: 42, 21: 15, 22: 23, 23: 29, 24: 22, 25: 44, 26: 25, 27: 12, 28: 25, 29: 11, 30: 31, 31: 13}, '2SA': {1: 27, 2: 32, 3: 39, 4: 12, 5: 25, 6: 23, 7: 29, 8: 18, 9: 13, 10: 19, 11: 27, 12: 31, 13: 39, 14: 33, 15: 37, 16: 23, 17: 29, 18: 33, 19: 43, 20: 26, 21: 22, 22: 51, 23: 39, 24: 25}, '1KI': {1: 53, 2: 46, 3: 28, 4: 34, 5: 18, 6: 38, 7: 51, 8: 66, 9: 28, 10: 29, 11: 43, 12: 33, 13: 34, 14: 31, 15: 34, 16: 34, 17: 24, 18: 46, 19: 21, 20: 43, 21: 29, 22: 53}, '2KI': {1: 18, 2: 25, 3: 27, 4: 44, 5: 27, 6: 33, 7: 20, 8: 29, 9: 37, 10: 36, 11: 21, 12: 21, 13: 25, 14: 29, 15: 38, 16: 20, 17: 41, 18: 37, 19: 37, 20: 21, 21: 26, 22: 20, 23: 37, 24: 20, 25: 30}, '1CH': {1: 54, 2: 55, 3: 24, 4: 43, 5: 26, 6: 81, 7: 40, 8: 40, 9: 44, 10: 14, 11: 47, 12: 40, 13: 14, 14: 17, 15: 29, 16: 43, 17: 27, 18: 17, 19: 19, 20: 8, 21: 30, 22: 19, 23: 32, 24: 31, 25: 31, 26: 32, 27: 34, 28: 21, 29: 30}, '2CH': {1: 17, 2: 18, 3: 17, 4: 22, 5: 14, 6: 42, 7: 22, 8: 18, 9: 31, 10: 19, 11: 23, 12: 16, 13: 22, 14: 15, 15: 19, 16: 14, 17: 19, 18: 34, 19: 11, 20: 37, 21: 20, 22: 12, 23: 21, 24: 27, 25: 28, 26: 23, 27: 9, 28: 27, 29: 36, 30: 27, 31: 21, 32: 33, 33: 25, 34: 33, 35: 27, 36: 23}, 'EZR': {1: 11, 2: 70, 3: 13, 4: 24, 5: 17, 6: 22, 7: 28, 8: 36, 9: 15, 10: 44}, 'NEH': {1: 11, 2: 20, 3: 32, 4: 23, 5: 19, 6: 19, 7: 73, 8: 18, 9: 38, 10: 39, 11: 36, 12: 47, 13: 31}, 'EST': {1: 22, 2: 23, 3: 15, 4: 17, 5: 14, 6: 14, 7: 10, 8: 17, 9: 32, 10: 3}, 'JOB': {1: 22, 2: 13, 3: 26, 4: 21, 5: 27, 6: 30, 7: 21, 8: 22, 9: 35, 10: 22, 11: 20, 12: 25, 13: 28, 14: 22, 15: 35, 16: 22, 17: 16, 18: 21, 19: 29, 20: 29, 21: 34, 22: 30, 23: 17, 24: 25, 25: 6, 26: 14, 27: 23, 28: 28, 29: 25, 30: 31, 31: 40, 32: 22, 33: 33, 34: 37, 35: 16, 36: 33, 37: 24, 38: 41, 39: 30, 40: 24, 41: 34, 42: 17}, 'PSA': {1: 6, 2: 12, 3: 8, 4: 8, 5: 12, 6: 10, 7: 17, 8: 9, 9: 20, 10: 18, 11: 7, 12: 8, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9, 21: 13, 22: 31, 23: 6, 24: 10, 25: 22, 26: 12, 27: 14, 28: 9, 29: 11, 30: 12, 31: 24, 32: 11, 33: 22, 34: 22, 35: 28, 36: 12, 37: 40, 38: 22, 39: 13, 40: 17, 41: 13, 42: 11, 43: 5, 44: 26, 45: 17, 46: 11, 47: 9, 48: 14, 49: 20, 50: 23, 51: 19, 52: 9, 53: 6, 54: 7, 55: 23, 56: 13, 57: 11, 58: 11, 59: 17, 60: 12, 61: 8, 62: 12, 63: 11, 64: 10, 65: 13, 66: 20, 67: 7, 68: 35, 69: 36, 70: 5, 71: 24, 72: 20, 73: 28, 74: 23, 75: 10, 76: 12, 77: 20, 78: 72, 79: 13, 80: 19, 81: 16, 82: 8, 83: 18, 84: 12, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17, 91: 16, 92: 15, 93: 5, 94: 23, 95: 11, 96: 13, 97: 12, 98: 9, 99: 9, 100: 5, 101: 8, 102: 28, 103: 22, 104: 35, 105: 45, 106: 48, 107: 43, 108: 13, 109: 31, 110: 7, 111: 10, 112: 10, 113: 9, 114: 8, 115: 18, 116: 19, 117: 2, 118: 29, 119: 176, 120: 7, 121: 8, 122: 9, 123: 4, 124: 8, 125: 5, 126: 6, 127: 5, 128: 6, 129: 8, 130: 8, 131: 3, 132: 18, 133: 3, 134: 3, 135: 21, 136: 26, 137: 9, 138: 8, 139: 24, 140: 13, 141: 10, 142: 7, 143: 12, 144: 15, 145: 21, 146: 10, 147: 20, 148: 14, 149: 9, 150: 6}, 'PRO': {1: 33, 2: 22, 3: 35, 4: 27, 5: 23, 6: 35, 7: 27, 8: 36, 9: 18, 10: 32, 11: 31, 12: 28, 13: 25, 14: 35, 15: 33, 16: 33, 17: 28, 18: 24, 19: 29, 20: 30, 21: 31, 22: 29, 23: 35, 24: 34, 25: 28, 26: 28, 27: 27, 28: 28, 29: 27, 30: 33, 31: 31}, 'ECC': {1: 18, 2: 26, 3: 22, 4: 16, 5: 20, 6: 12, 7: 29, 8: 17, 9: 18, 10: 20, 11: 10, 12: 14}, 'SNG': {1: 17, 2: 17, 3: 11, 4: 16, 5: 16, 6: 13, 7: 13, 8: 14}, 'ISA': {1: 31, 2: 22, 3: 26, 4: 6, 5: 30, 6: 13, 7: 25, 8: 22, 9: 21, 10: 34, 11: 16, 12: 6, 13: 22, 14: 32, 15: 9, 16: 14, 17: 14, 18: 7, 19: 25, 20: 6, 21: 17, 22: 25, 23: 18, 24: 23, 25: 12, 26: 21, 27: 13, 28: 29, 29: 24, 30: 33, 31: 9, 32: 20, 33: 24, 34: 17, 35: 10, 36: 22, 37: 38, 38: 22, 39: 8, 40: 31, 41: 29, 42: 25, 43: 28, 44: 28, 45: 25, 46: 13, 47: 15, 48: 22, 49: 26, 50: 11, 51: 23, 52: 15, 53: 12, 54: 17, 55: 13, 56: 12, 57: 21, 58: 14, 59: 21, 60: 22, 61: 11, 62: 12, 63: 19, 64: 12, 65: 25, 66: 24}, 'JER': {1: 19, 2: 37, 3: 25, 4: 31, 5: 31, 6: 30, 7: 34, 8: 22, 9: 26, 10: 25, 11: 23, 12: 17, 13: 27, 14: 22, 15: 21, 16: 21, 17: 27, 18: 23, 19: 15, 20: 18, 21: 14, 22: 30, 23: 40, 24: 10, 25: 38, 26: 24, 27: 22, 28: 17, 29: 32, 30: 24, 31: 40, 32: 44, 33: 26, 34: 22, 35: 19, 36: 32, 37: 21, 38: 28, 39: 18, 40: 16, 41: 18, 42: 22, 43: 13, 44: 30, 45: 5, 46: 28, 47: 7, 48: 47, 49: 39, 50: 46, 51: 64, 52: 34}, 'LAM': {1: 22, 2: 22, 3: 66, 4: 22, 5: 22}, 'EZK': {1: 28, 2: 10, 3: 27, 4: 17, 5: 17, 6: 14, 7: 27, 8: 18, 9: 11, 10: 22, 11: 25, 12: 28, 13: 23, 14: 23, 15: 8, 16: 63, 17: 24, 18: 32, 19: 14, 20: 49, 21: 32, 22: 31, 23: 49, 24: 27, 25: 17, 26: 21, 27: 36, 28: 26, 29: 21, 30: 26, 31: 18, 32: 32, 33: 33, 34: 31, 35: 15, 36: 38, 37: 28, 38: 23, 39: 29, 40: 49, 41: 26, 42: 20, 43: 27, 44: 31, 45: 25, 46: 24, 47: 23, 48: 35}, 'DAN': {1: 21, 2: 49, 3: 30, 4: 37, 5: 31, 6: 28, 7: 28, 8: 27, 9: 27, 10: 21, 11: 45, 12: 13}, 'HOS': {1: 11, 2: 23, 3: 5, 4: 19, 5: 15, 6: 11, 7: 16, 8: 14, 9: 17, 10: 15, 11: 12, 12: 14, 13: 16, 14: 9}, 'JOL': {1: 20, 2: 32, 3: 21}, 'AMO': {1: 15, 2: 16, 3: 15, 4: 13, 5: 27, 6: 14, 7: 17, 8: 14, 9: 15}, 'OBA': {1: 21}, 'JON': {1: 17, 2: 10, 3: 10, 4: 11}, 'MIC': {1: 16, 2: 13, 3: 12, 4: 13, 5: 15, 6: 16, 7: 20}, 'NAM': {1: 15, 2: 13, 3: 19}, 'HAB': {1: 17, 2: 20, 3: 19}, 'ZEP': {1: 18, 2: 15, 3: 20}, 'HAG': {1: 15, 2: 23}, 'ZEC': {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21}, 'MAL': {1: 14, 2: 17, 3: 18, 4: 6}, 'MAT': {1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29, 8: 34, 9: 38, 10: 42, 11: 30, 12: 50, 13: 58, 14: 36, 15: 39, 16: 28, 17: 27, 18: 35, 19: 30, 20: 34, 21: 46, 22: 46, 23: 39, 24: 51, 25: 46, 26: 75, 27: 66, 28: 20}, 'MRK': {1: 45, 2: 28, 3: 35, 4: 41, 5: 43, 6: 56, 7: 37, 8: 38, 9: 50, 10: 52, 11: 33, 12: 44, 13: 37, 14: 72, 15: 47, 16: 20}, 'LUK': {1: 80, 2: 52, 3: 38, 4: 44, 5: 39, 6: 49, 7: 50, 8: 56, 9: 62, 10: 42, 11: 54, 12: 59, 13: 35, 14: 35, 15: 32, 16: 31, 17: 37, 18: 43, 19: 48, 20: 47, 21: 38, 22: 71, 23: 56, 24: 53}, 'JHN': {1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59, 9: 41, 10: 42, 11: 57, 12: 50, 13: 38, 14: 31, 15: 27, 16: 33, 17: 26, 18: 40, 19: 42, 20: 31, 21: 25}, 'ACT': {1: 26, 2: 47, 3: 26, 4: 37, 5: 42, 6: 15, 7: 60, 8: 40, 9: 43, 10: 48, 11: 30, 12: 25, 13: 52, 14: 28, 15: 41, 16: 40, 17: 34, 18: 28, 19: 41, 20: 38, 21: 40, 22: 30, 23: 35, 24: 27, 25: 27, 26: 32, 27: 44, 28: 31}, 'ROM': {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39, 9: 33, 10: 21, 11: 36, 12: 21, 13: 14, 14: 23, 15: 33, 16: 27}, '1CO': {1: 31, 2: 16, 3: 23, 4: 21, 5: 13, 6: 20, 7: 40, 8: 13, 9: 27, 10: 33, 11: 34, 12: 31, 13: 13, 14: 40, 15: 58, 16: 24}, '2CO': {1: 24, 2: 17, 3: 18, 4: 18, 5: 21, 6: 18, 7: 16, 8: 24, 9: 15, 10: 18, 11: 33, 12: 21, 13: 14}, 'GAL': {1: 24, 2: 21, 3: 29, 4: 31, 5: 26, 6: 18}, 'EPH': {1: 23, 2: 22, 3: 21, 4: 32, 5: 33, 6: 24}, 'PHP': {1: 30, 2: 30, 3: 21, 4: 23}, 'COL': {1: 29, 2: 23, 3: 25, 4: 18}, '1TH': {1: 10, 2: 20, 3: 13, 4: 18, 5: 28}, '2TH': {1: 12, 2: 17, 3: 18}, '1TI': {1: 20, 2: 15, 3: 16, 4: 16, 5: 25, 6: 21}, '2TI': {1: 18, 2: 26, 3: 17, 4: 22}, 'TIT': {1: 16, 2: 15, 3: 15}, 'PHM': {1: 25}, 'HEB': {1: 14, 2: 18, 3: 19, 4: 16, 5: 14, 6: 20, 7: 28, 8: 13, 9: 28, 10: 39, 11: 40, 12: 29, 13: 25}, 'JAS': {1: 27, 2: 26, 3: 18, 4: 17, 5: 20}, '1PE': {1: 25, 2: 25, 3: 22, 4: 19, 5: 14}, '2PE': {1: 21, 2: 22, 3: 18}, '1JN': {1: 10, 2: 29, 3: 24, 4: 21, 5: 21}, '2JN': {1: 13}, '3JN': {1: 14}, 'JUD': {1: 25}, 'REV': {1: 20, 2: 29, 3: 22, 4: 11, 5: 14, 6: 17, 7: 17, 8: 13, 9: 21, 10: 11, 11: 19, 12: 17, 13: 18, 14: 20, 15: 8, 16: 21, 17: 18, 18: 24, 19: 21, 20: 15, 21: 27, 22: 21}, 'TOB': {1: 22, 2: 14, 3: 17, 4: 21, 5: 22, 6: 18, 7: 16, 8: 21, 9: 6, 10: 13, 11: 18, 12: 22, 13: 18, 14: 15}, 'JDT': {1: 16, 2: 28, 3: 10, 4: 15, 5: 24, 6: 21, 7: 32, 8: 36, 9: 14, 10: 23, 11: 23, 12: 20, 13: 20, 14: 19, 15: 14, 16: 25}, 'WIS': {1: 16, 2: 24, 3: 19, 4: 20, 5: 23, 6: 25, 7: 30, 8: 21, 9: 18, 10: 21, 11: 26, 12: 27, 13: 19, 14: 31, 15: 19, 16: 29, 17: 21, 18: 25, 19: 22}, 'SIR': {1: 30, 2: 18, 3: 31, 4: 31, 5: 15, 6: 37, 7: 36, 8: 19, 9: 18, 10: 31, 11: 34, 12: 18, 13: 26, 14: 27, 15: 20, 16: 30, 17: 32, 18: 33, 19: 30, 20: 31, 21: 28, 22: 27, 23: 27, 24: 34, 25: 26, 26: 29, 27: 30, 28: 26, 29: 28, 30: 25, 31: 31, 32: 24, 33: 33, 34: 31, 35: 26, 36: 31, 37: 31, 38: 34, 39: 35, 40: 30, 41: 22, 42: 25, 43: 33, 44: 23, 45: 26, 46: 20, 47: 25, 48: 25, 49: 16, 50: 29, 51: 30}, 'BAR': {1: 22, 2: 35, 3: 37, 4: 37, 5: 9}, 'LJE': {1: 72}, 'S3Y': {1: 68}, 'SUS': {1: 64}, 'BEL': {1: 42}, '1MA': {1: 64, 2: 70, 3: 60, 4: 61, 5: 68, 6: 63, 7: 50, 8: 32, 9: 73, 10: 89, 11: 74, 12: 53, 13: 53, 14: 49, 15: 41, 16: 24}, '2MA': {1: 36, 2: 32, 3: 40, 4: 50, 5: 27, 6: 31, 7: 42, 8: 36, 9: 29, 10: 38, 11: 38, 12: 45, 13: 26, 14: 46, 15: 39}, '1ES': {1: 55, 2: 26, 3: 24, 4: 63, 5: 71, 6: 33, 7: 15, 8: 92, 9: 55}, 'MAN': {1: 15}, 'PS2': {1: 7, 2: 2, 3: 7}, '3MA': {1: 29, 2: 33, 3: 30, 4: 21, 5: 51, 6: 41, 7: 23}, '2ES': {1: 40, 2: 48, 3: 36, 4: 52, 5: 56, 6: 59, 7: 140, 8: 63, 9: 47, 10: 60, 11: 46, 12: 51, 13: 58, 14: 48, 15: 63, 16: 78}, '4MA': {1: 35, 2: 24, 3: 21, 4: 26, 5: 38, 6: 35, 7: 23, 8: 29, 9: 32, 10: 21, 11: 27, 12: 19, 13: 27, 14: 20, 15: 32, 16: 25, 17: 24, 18: 24}}

def chooseVerse(bibleBooks, bibleStats):
    while True:
        print("1. Start a new search\n2. Use a saved set of verses for your search")
        searchOption = input("\nChoose an option (or Ctrl-c to quit at any moment): ")
        print()
        try:
            searchOption = int(searchOption)
        except:
            print("\nPlease choose from the available options\n")
            continue
        if searchOption == 1:
            verses = list()
            def newSearch(verses, bibleBooks, bibleStats):
                foolist = list(bibleBooks.keys()) + ['']
                for a, b, c in zip(foolist[:int(len(foolist)/3)], foolist[int(len(foolist)/3):int(len(foolist)/3*2)], foolist[int(len(foolist)/3*2):]):
                    print('{:<30}{:<30}{:<}'.format(a, b, c))
                while True:
                    book = input("\nWhat bible book: ").lower()
                    if book not in bibleBooks:
                        print("Please choose from the list of bible books or check the spelling\n")
                        continue
                    else:
                        break
                while True:
                    print("The number of chapters in {}: {}".format(book, len(bibleStats[bibleBooks[book]])))
                    chapter = input("What chapter: ")
                    try:
                        if int(chapter) - 1 in range(len(bibleStats[bibleBooks[book]])):
                            break
                        else:
                            print("Please choose from the available chapters\n")
                            continue
                    except:
                        print("Please enter a number\n")
                        continue
                while True:
                    print("The number of verses in {} {}: {} ".format(book, chapter, (bibleStats[bibleBooks[book]][int(chapter)])))
                    verse = input("What verse: ")
                    try:
                        if int(verse) - 1 in range(bibleStats[bibleBooks[book]][int(chapter)]):
                            break
                        else:
                            print("Please choose from the available verses\n")
                            continue
                    except:
                        print("Please enter a number\n")
                        continue
                verses.append((book, int(chapter), int(verse)))
                print("\nSearch for:")
                for verse in verses:
                    verse = verse[0] + ' ' + str(verse[1]) + ":" + str(verse[2])
                print('    ' + verse)
                while True:
                    again = input("Add another verse to your search? (y/n) ")
                    if again == 'y':
                        return newSearch(verses, bibleBooks, bibleStats)
                    elif again == 'n':
                        return verses
                    else:
                        print("Please enter 'y' or 'n'\n")
                        continue
            verses = newSearch(verses, bibleBooks, bibleStats)
            while True:
                save = input("Save this verse set for future searches? (y/n) ")
                if save == 'y':
                    name = input("Give a name for this set: ")
                    with open('bible_verse_extractor_saved_searches.txt', 'a') as f:
                        f.write(name + " = " + str(verses) + '\n')
                    return verses
                elif save == 'n':
                    return verses
                else: 
                    print("Please enter 'y' or 'n'")
                    continue

        elif searchOption == 2:
         
            def strToList(i):
                i2 = i.split(" = ")
                searchList = i2[1].strip().strip('][').strip('()').split('), (')
                searchList = [(i2.split(', ')[0].strip("''"), int(i2.split(', ')[1].strip("''")), int(i2.split(', ')[2].strip("''"))) for i2 in searchList]
                return i2, searchList

            with open('bible_verse_extractor_saved_searches.txt', 'r') as f:
                savedSearches = f.readlines()
                for item in savedSearches:
                    item2, searchList = strToList(item)
                    searchListPrint = [searchList[i][0] + ' ' + str(searchList[i][1]) + ":" + str(searchList[i][2]) for i in range(len(searchList))]
                    searchListPrint = ', '.join(searchListPrint)
                    print(str(savedSearches.index(item)+1) + '. ' + item2[0] + ":\n    " + searchListPrint + '\n')
            while True:
                choice = input("Choose a set from the list above:  ")
                try: 
                    choice = int(choice)
                except:
                    print("\nPlease choose from the available options\n")
                    continue
                if choice in range(1, len(savedSearches)+1):
                    i2, searchList = strToList(savedSearches[choice-1])
                    print("Your choice: {}.\n".format(i2[0]))
                    return searchList
                else:
                    print("\nPlease choose from the available options\n")
                    continue
        else:
            print("\nPlease choose from the available options\n")
            continue

verses = chooseVerse(bibleBooks, bibleStats)

data = [[verse[0] + ' ' + str(verse[1]) + ':' + str(verse[2])] for verse in verses]

mainPage = 'http://www.bible.com/languages'

languages = dict()

def checkDownload(downloadedPage):
    try:
        return downloadedPage.raise_for_status()
    except:
        print("Download failed.")

def getPage(link):
    page = requests.get(link)
    checkDownload(page)
    soupPage = bs.BeautifulSoup(page.text, features='lxml')
    return soupPage

def getLanguageList(soupObject):
    languageLinks = soupObject.select('td > a')
    languageList = dict()
    for languageLink in languageLinks:
        try:
            languageCode = re.search(codePattern, languageLink.get('title')).group()
            languageList[languageLink.getText().strip()] = languageCode
        except:
            continue
    return languageList, languageLinks

translations = list()
def whatLanguage(languages, languageList, languageLinks, translations):
    language = input("What language: ")
    if language.strip() == '':
        print("Please enter something.\n")
        return whatLanguage(languages, languageList, languageLinks, translations)
    matches = list()
    for languageName, languageCode in languageList.items():
        if language.lower() in languageName.lower():
            matches.append(languageName)
        elif language.lower() in languageCode.lower():
            matches.append(languageName)
    def another(languages, languageList, translations):
        anotherLanguage = input("Add another language? (y/n) ")
        print()
        if anotherLanguage.lower() == 'y':
            return whatLanguage(languages, languageList, languageLinks, translations)
        elif anotherLanguage.lower() == 'n':
            return languages, translations
        else:
            print("Please choose 'y' or 'n'\n")
            return another(languages, languageList, translations)
    if len(matches) > 1:
        def whichLanguage(matches):
            print("\nThere are several languages matching your search:")
            for language in matches:
                print('{}. {}'.format(matches.index(language)+1, language))
            choice = input("\nWhich language: ")
            try:
                if int(choice) < 1:
                    print("Please choose from the available options\n")
                    return whichLanguage(matches)
                print("Getting the list of bible translations in {}...".format(matches[int(choice)-1]))
                translationTitle, code1 = getBibleTextCode(matches[int(choice)-1], languageList, languageLinks)
                if translationTitle == False:
                    return another(languages, languageList, translations)
                else:
                    languages.setdefault(languageList[matches[int(choice)-1]], []).append(code1)
                    translations.append(matches[int(choice)-1] + ": " + translationTitle)
                    return another(languages, languageList, translations)
            except:
                raise
                print("Please choose from the available options \n")
                return whichLanguage(matches)
        return whichLanguage(matches)
    elif len(matches) == 1:
        print("Getting the list of bible translations in {}...".format(matches[0]))
        translationTitle, code1 = getBibleTextCode(matches[0], languageList, languageLinks)
        if translationTitle == False:
            return another(languages, languageList, translations)
        else:
            languages.setdefault(languageList[matches[0]], []).append(code1)
            translations.append(matches[0] + ": " + translationTitle)
            return another(languages, languageList, translations)
    else:
        print("No such language found. Try again")
        while True:
            stop = input("Continue searching for another language? (y/n) ")
            if stop == 'n':
                return languages, translations
            elif stop == 'y':
                return whatLanguage(languages, languageList, languageLinks, translations)
            else:
                print("Please enter 'y' or 'n'\n")
                continue

def getLanguage(language, languageList, languageLinks):
    for name, code in languageList.items():
        if language in code or language in name:
            for languageLink in languageLinks:
                try:
                    if code in languageLink.get('title') and name in languageLink.getText():
                        return languageLink.get('href'), name
                except:
                    continue

def getTranslationList(soup):
    translationList = dict()
    for item in soup.select('a[role="button"]'):
        try:
            if '/versions/' in item.get('href'):
                translationList[item.getText()] = item.get('href')
        except:
            continue
    return translationList 

def chooseTranslation(translationList, language):
    print("The list of available translations for {}:".format(language))
    for i in range(len(translationList.keys())):
        print('{}. {}'.format(i+1, list(translationList.keys())[i]))
    choice = input("Choose a translation (or enter 'n' to cancel adding this language): ")
    try:
        print("Your choice: {}".format(list(translationList.keys())[int(choice)-1]))
        if int(choice) not in range(1, len(translationList)+1):
            print('Choose from the available translations')
            return chooseTranslation(translationList, language)
        else:
            variantLink = list(translationList.values())[int(choice)-1]
            code = re.search(translationPattern, variantLink).group()
            return list(translationList.keys())[int(choice)-1], re.search(translationPattern, variantLink).group()
    except:
        raise
        if choice.lower() == 'n':
            return False, (False, False)
        else:
            print("Please choose from the available options\n")
            return chooseTranslation(translationList, language)

def getBibleTextCode(language, languageList, languageLinks):
    link, languageName = getLanguage(language, languageList, languageLinks)
    translationListSoup = getPage(mainPage + link[10:])
    translationList = getTranslationList(translationListSoup)
    translationTitle, code1 = chooseTranslation(translationList, languageName)
    return translationTitle, code1

mainPageSoup = getPage(mainPage)
languageList, languageLinks = getLanguageList(mainPageSoup)
languages, translations = whatLanguage(languages, languageList, languageLinks, translations)

languageNames = [{v: k for k, v in languageList.items()}[language] for language in languages.keys()]

verseCodes = [(bibleBooks[verse[0].lower()], verse[1], verse[2]) for verse in verses]

def checkLink(link):
    chapterSoup = getPage(link)
    actualLink = chapterSoup.select_one('link[rel="canonical"]').get('href')
    correctLinkCode = link.split('.')[-3][-3:] + link.split('.')[-2]
    actualLinkCode = actualLink.split('.')[-3][-3:] + actualLink.split('.')[-2]
    return actualLink, chapterSoup, correctLinkCode, actualLinkCode

counter = 0
for l in languages.keys():
    #This loop is to get data for each chosen translation in the same language
    for codePair in languages[l]:
        print("Processing data in {}".format(translations[counter]))
        getCodeLink = getPage('http://www.bible.com/bible/{}/GEN.1.'.format(codePair))
        code2 = getCodeLink.select_one('title').getText().replace(')', '(').split('(')[-2]
        for verse in verseCodes:
            print('    ' + data[verseCodes.index(verse)][0])    
            correctLink = 'http://www.bible.com/bible/{}/{}.{}.{}'.format(codePair, verse[0], verse[1], code2)
            actualLink, chapterSoup, correctLinkCode, actualLinkCode = checkLink(correctLink)
            if correctLinkCode != actualLinkCode:
                #For translations like https://www.bible.com/bible/2385/LUK.6_1.NODLNNT
                correctLink = 'http://www.bible.com/bible/{}/{}.{}_1.{}'.format(codePair, verse[0], verse[1], code2)
                actualLink, chapterSoup, correctLinkCode, actualLinkCode = checkLink(correctLink)
                if correctLinkCode != actualLinkCode:
                    #For translations like https://www.bible.com/bible/1094/GEN.21_1.گیلکی
                    correctLink = 'http://www.bible.com/bible/{}/{}.{}_1.{}'.format(codePair, verse[0], 10+int(verse[1]), code2)
                    actualLink, chapterSoup, correctLinkCode, actualLinkCode = checkLink(correctLink)
                    if correctLinkCode != actualLinkCode:
                        print('    There is no translation for {} or a chapter of it in {}.'.format({v: k for k, v in bibleBooks.items()}[verse[0]], translations[counter]))
                        data[verseCodes.index(verse)].append('No translation of this book or this chapter is available')
                        continue
            spans = chapterSoup.select('span[class="content"]')
            #Some verses are highlighted in red and stored in <span class="wj"> objects (e.g. in World English Bible)
            fullVerse = list()
            for span in spans:
                try:
                    if 'v{}'.format(verse[2]) in span.parent['class'] or 'v{}'.format(verse[2]) in span.parent.parent['class']:
                        if span.getText() != ' ':
                            fullVerse.append(span.getText().strip())
                except:
                    continue
            fullVerse = ' '.join(fullVerse)
            if fullVerse == '':
                data[verseCodes.index(verse)].append('THIS VERSE IS MISSING FROM THE TEXT')
            else:
                data[verseCodes.index(verse)].append(fullVerse)
        counter += 1 

headers = ['verse'] + [translations[i] for i in range(len(translations))]

with open('bible_verse_extractor_results.csv', 'w', newline='', encoding='utf-8-sig') as f:
    outputWriter = csv.writer(f)
    outputWriter.writerow(headers)
    for row in data:
        outputWriter.writerow(row)

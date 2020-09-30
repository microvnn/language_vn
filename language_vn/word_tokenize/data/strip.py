from os import path
from util.io import readlines, write
import string

curdir = path.dirname(__file__)
f_check = path.join(curdir, 'check.txt')
f_loc_vietnam = path.join(curdir, 'loc_vietnam.txt')
f_vocabulary_standard = path.join(curdir, 'vocabulary_standard.txt')
check = [x.lower().replace(' ', '_')
         for x in readlines(f_check)]
loc_vietnam = [x.lower().replace(' ', '_')
               for x in readlines(f_loc_vietnam)]
vocabulary_standard = [x.lower().replace(' ', '_')
                       for x in readlines(f_vocabulary_standard)]

vocabulary_veryfied = [x for x in vocabulary_standard if (
    x in check) or (x not in loc_vietnam)]
f_vocabulary_veryfied = path.join(curdir, 'vocabulary_veryfied.txt')
write(f_vocabulary_veryfied, '\n'.join(vocabulary_veryfied))

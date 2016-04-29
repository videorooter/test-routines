#! /usr/bin/python2
"""
This is the main test script which identifies all forks of a particular
project (or several projects) and runs the test algorithms on each fork.
"""
import fileinput
import fcntl
import json
import sys
import requests
import ConfigParser
import os.path
import datetime
import shutil
from pygithub3 import Github
from subprocess import call
from string import Template

flock = open('.videorooter.lock', 'w')
try:
   fcntl.lockf(flock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
   sys.exit(0)

config = ConfigParser.ConfigParser()
config.read('tests.conf')
gh = Github(login=config.get('tests', 'username'),
            password=config.get('tests', 'password'))

base_repo = [ u'videorooter/algo-repository-template',
              u'commonsmachinery/blockhash' ]

derived_repos = []
derived_branches = []

#
# Iterate over all forks (and forks of forks) of above repositories
# to find the complete list of forks in any generation. Add each fork
# to derived_repos.
#
while base_repo:
  repo = base_repo.pop()
  i = repo.split('/')

  forks = gh.repos.forks.list(user=i[0], repo=i[1])
  repo_meta = gh.repos.get(user=i[0], repo=i[1])
  derived_repos.append("%s/%s" % (repo, repo_meta.fork))
  for i in forks.iterator():
     base_repo.append("%s/%s" % (i.owner.login, i.name))

#
# For each repo identified in derived_repos as not a fork, add
# all of its branches to the list of derived branches.
#
for repo in list(set(derived_repos)):
  r = repo.split('/')
  if r[2] == "False":
    branches = gh.repos.list_branches(user=r[0], repo=r[1])
    for i in branches.iterator():
      derived_branches.append({'base': "%s/%s" % (r[0], r[1]),
                               'branch': i.name,
                               'sha': i.commit.sha})

#
# For each fork, only add its branches to the derived branches if the
# last commit is different from the origin.
#
for repo in list(set(derived_repos)):
  r = repo.split('/')
  if r[2] == "True":
   branches = gh.repos.list_branches(user=r[0], repo=r[1])
   for i in branches.iterator():
     found = 0
     for l in derived_branches:
        if l['sha'] == i.commit.sha:
           found = 1
     if found == 0:
        derived_branches.append({'base': "%s/%s" % (r[0], r[1]),
                                 'branch': i.name,
                                 'sha': i.commit.sha})
#
# For each branch, check if we have a cached copy of tests run against
# its' latest commit. If we don't have a cached copy, call
# single-test-image.sh to run the tests. The script returns the
# data in src/output.html, so copy this over to the cache.
#
for i in derived_branches:
  if i['base'] == 'videorooter/algo-repository-template':
    continue
  if not os.path.isfile("%s/%s" % (config.get('tests', 'cachepath'), i['sha'])):
    #
    # Check if we actually have a videorooter.conf to work from
    #
    r = i['base'].split('/')
    l = gh.repos.commits.list(user=r[0], repo=r[1], sha=i['branch'], path='videorooter.conf')
    if len(l.all()) > 0:
      res = call(['./single-test-image.sh', "http://github.com/%s" % i['base'], i['branch'], i['sha']])
      if not res:
         shutil.copyfile('src/output.html', "%s/%s" % (config.get('tests', 'cachepath'), i['sha']))

# 
# Go through all branches again, get statistics from the output files.
# The "best" result is the one with highest spread at the same threshold,
# ie. calculating accuracy minus false positives. A higher spread means
# a high accuracy and low false positives.
#
# This is ugly, isn't there a better way to parse formatted strings?
#
content = ""
for i in derived_branches:
  if i['base'] == 'videorooter/algo-repository-template':
    continue
  if os.path.isfile("%s/%s" % (config.get('tests', 'cachepath'), i['sha'])):
    f = open("%s/%s" % (config.get('tests', 'cachepath'), i['sha']))
    acc = {}
    cc = {}
    best_result = 0
    best_t = 0
    for line in f:
      if 'ACC' in line:
         l = line.split()
         acc[int(l[1].strip('t').strip('='))] = float(l[2].strip('%'))
      elif 'CC' in line:
         l = line.split()
         cc[int(l[1].strip('t').strip('='))] = float(l[2].strip('%'))
    for j in acc:
       if (acc[j]-cc[j]) > best_result:
          best_result = acc[j]-cc[j]
          best_t = j
    f.seek(0)

    template = open('tmpl/test.html.tmpl')
    src = Template(template.read())
    subst = { 'testname': "%s/%s" % (i['base'], i['branch']),
              'id': i['sha'], 
              'result': best_result,
              't': best_t,
              'output': f.read() }
    f.close()
    i['output'] = src.substitute(subst)
    content += i['output']
    template.close()

#
# Now we do the actual output!
#
template = open('tmpl/index.html.tmpl')
src = Template(template.read())
subst = { 'runtime':  datetime.datetime.utcnow(),
          'content': content }

f = open("%s/index.html" % config.get('tests', 'outpath'), 'w')
f.write(src.substitute(subst))
f.close()
template.close()

flock.close()

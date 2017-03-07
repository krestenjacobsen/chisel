#encoding: utf-8

# Chisel
# David Zhou, github.com/dz
#
# Updates and enhancements added/included by ckunte:
# 14.05.2012:
# - RSS feed generator script, hat-tip: Ronan Jouchet, github.com/ronjouch
# - Smartypants content parsing included by ckunte, github.com/ckunte
# - Permalink url updated to include only the year followed by post title,
#   i.e., http://staticsite.com/2012/post.html or http://staticsite.com/2012/post
#
# Updates and enhancements added/included by krestenjacobsen:
# 27.09.2013:
# - Localization of dates using pythons "locale"
# 02.03.2017
#- Linked list functionality added (including the theme)
#
# Requires:
# jinja2, markdown, PyRSS2Gen

import sys, re, time, os, codecs, gzip, datetime, locale
import jinja2, markdown, PyRSS2Gen # install with pip

#Settings
# For folders that look like the following (this is primarily
# done to keep native post files and the generated html files
# separate; don't have to be -- just my personal preference):
# Sites
#     /chisel (the generator)
#     /posts (in markdown stored offline)
#     /www (the generated html site from post files)
# the locations are used thus:
#
BASEURL = "http://log.logiskhave.dk/" #end with slash
# The following tells chisel where to look for native posts:
SOURCE = "./posts/" #end with slash
#  The following tells chisel where to generate site:
DESTINATION = "./www/" #end with slash
HOME_SHOW = 5 #numer of entries to show on homepage
TEMPLATE_PATH = "./theme/" #end with slash
TEMPLATE_OPTIONS = {}
TEMPLATES = {
    'home': "home.html",
    'detail': "detail.html",
    'archive': "archive.html",
    'colophon': "colophon.html",
    'marathon': "marathon.html",
    'halfmarathon2014': "halfmarathon2014.html",
    'wishlist': "wishlist.html",
    '404': "404.html",
    'cv': "cv.html",
    }
# Set locale to preferred language (e.g. "en_US.UFT-8" or "da_DK.UTF-8")
locale.setlocale(locale.LC_TIME, "da_DK.UTF-8")
TIME_FORMAT = "%d. %B, %Y"
ENTRY_TIME_FORMAT = "%d-%m-%Y"
#FORMAT should be a callable that takes in text
#and returns formatted text
FORMAT = lambda text: markdown.markdown(text, ['footnotes', 'codehilite', 'video'])
# default URLEXT = ""
# set URLEXT = "" if server recognizes .html URLs and can be linked-to without the extension part.
URLEXT = ".html"
# default PATHEXT = ".html"
# set PATHEXT = "" if URLEXT = ".html" and vice versa.
PATHEXT = ""
RSS = PyRSS2Gen.RSS2(
    title = "krestens log",
    link = BASEURL + "rss.xml",
    description = "Kresten Jacobsens log",
    lastBuildDate = datetime.datetime.now(),
    items = [])
#########

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print "Starting " + func.__name__ + "...",
        func(*args, **kwargs)
        print "Done."
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            path = os.path.join(root, name)
            f = open(path, "rU")
            title = f.readline()
            date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
            year, month, day = date[:3]
            link = f.readline()
            # The following if / else clause is a temporary workaround, that needs cleanup.
            if link == "\n":
                files.append({
                    'title': title,
                    'epoch': time.mktime(date),
                    'content': FORMAT(''.join(f.readlines()[1:]).decode('UTF-8')),
                    #'url': '/'.join([str(year), "%.2d" % month, "%.2d" % day, os.path.splitext(name)[0] + ".html"]),
                    # Uncheck the following line if you have no rewrite (URLs end with .html).
                    'url': '/'.join([str(year), os.path.splitext(name)[0] + URLEXT]),
                    'pretty_date': time.strftime(TIME_FORMAT, date),
                    'date': date,
                    'year': year,
                    'month': month,
                    'day': day,
                    'filename': name,
                })
            else:
                files.append({
                    'title': title,
                    'epoch': time.mktime(date),
                    'link': link,
                    'content': FORMAT(''.join(f.readlines()[1:]).decode('UTF-8')),
                    #'url': '/'.join([str(year), "%.2d" % month, "%.2d" % day, os.path.splitext(name)[0] + ".html"]),
                    # Uncheck the following line if you have no rewrite (URLs end with .html).
                    'url': '/'.join([str(year), os.path.splitext(name)[0] + URLEXT]),
                    'pretty_date': time.strftime(TIME_FORMAT, date),
                    'date': date,
                    'year': year,
                    'month': month,
                    'day': day,
                    'filename': name,
                })
            f.close()
    return files

def compare_entries(x, y):
    result = cmp(-x['epoch'], -y['epoch'])
    if result == 0:
        return -cmp(x['filename'], y['filename'])
    return result

def write_file(url, data):
    path = DESTINATION + url + PATHEXT
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    file = open(path, "w")
    file.write(data.encode('UTF-8'))
    file.close()

def write_sitemap(url, data):
    path = DESTINATION + url
    with gzip.open(path, "wb") as file:
        file.write(data.encode('UTF-8'))

@step
def generate_homepage(f, e):
    """Generate homepage"""
    template = e.get_template(TEMPLATES['home'])
    write_file("index" + URLEXT, template.render(entries=f[:HOME_SHOW]))

@step
def generate_rss(f, e):
    """Generate rss"""
    for file in f[:HOME_SHOW]:
        RSS.items.append(PyRSS2Gen.RSSItem(title=file['title'], link=BASEURL + file['url'], description=file['content'], author="Kresten Jacobsen", guid = PyRSS2Gen.Guid(BASEURL + file['url']), pubDate=datetime.datetime(file['year'], file['month'], file['day'])))
    RSS.write_xml(open(DESTINATION + "rss.xml", "w"))

@step
def master_archive(f, e):
    """Generate master archive list of all entries"""
    template = e.get_template(TEMPLATES['archive'])
    write_file("archive" + URLEXT, template.render(entries=f))

@step
def generate_colophon(f, e):
    """Generate a colophon page"""
    template = e.get_template(TEMPLATES['colophon'])
    write_file("colophon" + URLEXT, template.render(entries=f))

@step
def generate_cv(f, e):
    """Generate a cv page"""
    template = e.get_template(TEMPLATES['cv'])
    write_file("cv" + URLEXT, template.render(entries=f))

@step
def generate_marathon(f, e):
    """Generate a marathon page"""
    template = e.get_template(TEMPLATES['marathon'])
    write_file("marathon" + URLEXT, template.render(entries=f))

@step
def generate_404(f, e):
    """Generate a 404 page"""
    template = e.get_template(TEMPLATES['404'])
    write_file("404" + URLEXT, template.render(entries=f))

@step
def detail_pages(f, e):
    """Generate detail pages of individual posts"""
    template = e.get_template(TEMPLATES['detail'])
    for file in f:
        write_file(file['url'], template.render(entry=file))

@step
def gen_sitemap(f, e):
    write_sitemap('sitemap.xml.gz', e.get_template('sitemap.html').render(entries=f))

def main():
    print "Chiseling..."
    print "\tReading files...",
    files = sorted(get_tree(SOURCE), cmp=compare_entries)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print "Done."
    print "\tRunning steps..."
    for step in STEPS:
        print "\t\t",
        step(files, env)
    print "\tDone."
    print "Done."

if __name__ == "__main__":
    sys.exit(main())
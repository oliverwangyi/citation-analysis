from bs4 import BeautifulSoup
import urllib2
import sys, os
import re, random, time
import smtplib

GOOG_URL = "http://scholar.google.com"
START_URL = "http://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:{0}"
MAX_LOOP = 100

def parse_a_url_for_citations(url, fout = None):
    next_link = None
    # <a class="cit-dark-large-link"
    # <a href="/citations?view_op=search_authors&amp;hl=en&amp;mauthors=label:network_science&amp;after_author=lOECAK7J__8J&amp;astart=10" class="cit-dark-link">Next &gt;</a>
    try:
        response = urllib2.urlopen(url)
        html_source = response.read()
        soup = BeautifulSoup(html_source)
    except:
        print '[ERROR]...', sys.exc_info()
    
    
    # Get names and citation strings
    links = soup.find_all('a', attrs={'class': 'cit-dark-large-link'})
    cite_ptn = re.compile("Cited by \d+<br>")
    cites = cite_ptn.findall(html_source)
    if len(links) != len(cites):
        return next_link
    
    # Save to file
    for i,link in enumerate(links):
        name = link.get_text().strip()
        cite = int(cites[i][9:-4])
        print name, cite
        if fout:
            fout.write('{0},{1}\n'.format(name.encode('utf8'), cite))
    
    # Get next link string
    next_link = soup.find('a', attrs={'class','cit-dark-link'}, text=u"Next >")['href']
    next_link = GOOG_URL + next_link
    return next_link



def main(label):
    url = START_URL.format(label)
    fout = open("scholar_citation_{0}.csv".format(label), "w")
    loop = 0
    while url and loop < MAX_LOOP:
        loop += 1
        print "Parsing ...", url
        next_url = parse_a_url_for_citations(url, fout)
        url = next_url
        # Wait random seconds
        sec = random.randint(0,5); print 'Wait', sec, 'seconds ...'
        time.sleep(sec)
    fout.close()



if __name__ == "__main__":
    label = sys.argv[1]
    main(label)

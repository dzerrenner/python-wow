# Copyright (c) 2009, Christian Kreutzer, David Zerrenner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from urllib2 import urlopen, URLError, quote, Request

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
    
REGION = 'eu'
BASE_URL = 'http://%s.wowarmory.com/search.xml' % (REGION)
BASE_DATA_URL = 'http://%s.wowarmory.com/_data/dungeons.xml' % (REGION)
BASE_LOC_URL = 'http://%s.wowarmory.com/data/dungeonStrings.xml' % (REGION)
QUERY_STRING_ITEM = 'searchQuery=%s&fl[source]=all&fl[type]=all&fl[usbleBy]=all&fl[rqrMin]=&fl[rqrMax]=&fl[rrt]=all&advOptName=none&fl[andor]=and&searchType=items&fl[advOpt]=none'
QUERY_STRING_RAID = 'fl[source]=dungeon&fl[dungeon]=%s&fl[boss]=%s&fl[difficulty]=%s&fl[type]=all&fl[usbleBy]=all&fl[rqrMin]=&fl[rqrMax]=&fl[rrt]=all&advOptName=none&fl[andor]=and&searchType=items&fl[advOpt]=none'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.2) Gecko/20100115 Firefox/3.6',
    'Accept-Language': 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3'
}
    
# dungeon, boss, difficulty
    
def _fetch(url, node=None):
    """fetches the response of a simple xml-based webservice. If node is omitted 
    the root of the parsed xml doc is returned as an ElementTree object
    otherwise the requested node is returned. The node is the first node which
    is found in the ElementTree, including all sub-elements."""
    retval = None
    try:
        xmldoc = urlopen(url)
    except URLError, e:
        try:
            print(str(e))
        except:
            return str(e)
    else:
        result = et.parse(xmldoc)
        root = result.getroot()
        if not node:
            retval = root
        else:
            retval = root.find(node) 
    return retval
    
def raid_loot(dungeon, boss = 'all', difficulty='normal', lang='de-de', node=None):
    """fetches all items which are dropped in a certain dungion by a certain
    boss on a certain difficulty mode. If the boss value is omitted, all
    possible bosses are used. If difficulty is omitted, the normal difficulty
    mode is used."""
    HEADER['Accept-Language'] = lang
    request = Request(BASE_URL, QUERY_STRING_RAID % (dungeon, boss, difficulty), HEADER)
    return _fetch(request, node)
    
def search_item(name, lang='de-de', node=None):
    HEADER['Accept-Language'] = lang
    request = Request(BASE_URL, QUERY_STRING_ITEM % (name), HEADER)
    return _fetch(request, node)

def load_dungeons(lang='de-de', node=None):
    HEADER['Accept-Language'] = lang
    request = Request(BASE_DATA_URL, '', HEADER)
    return _fetch(request, node)
    
def load_translations(lang='de-de', node=None):
    HEADER['Accept-Language'] = lang
    request = Request(BASE_LOC_URL, '', HEADER)
    return _fetch(request, node)
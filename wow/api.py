# Copyright (c) 2009, David Zerrenner
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

import fetch

def dungeon_list(type='raid'):
    """Retrieves a list of available dungeons, raid instances or both. If type 
    is omitted, the returned list contains all known raid instance shortnames.
    If type is 'dungeon', the list will contain all 5-player dungeon shortnames.
    The third option for type is 'all' which containes both dungeon and raid
    shortnames.
    """
    dungeon_data = fetch.load_dungeons('.//dungeons')
    if type is 'all':
        return [d.get('key') for d in dungeon_data.findall('.//dungeon')]
    else:
        return [d.get('key') for d in dungeon_data.findall('.//dungeon') if d.get('raid') == {'raid':'1', 'dungeon':'0'}[type]]
        
class Raid(set): 
    def __init__(self, name, difficulty = 'normal'):
        self.name = name
        
        # search for the items in this Raid
        itemlist = fetch.raid_loot(name, difficulty)
        for item_data in itemlist.getiterator('item'):
            self.add(Item(item_data))
    

class Item(object):
    """
    <item icon="inv_misc_gem_pearl_14" id="51026" name="Kristalline Essenz von Sindragosa" rarity="1" url="i=51026">
          <filter name="itemLevel" value="80" />
          <filter areaId="4812" areaKey="icecrowncitadel10" areaName="Eiskronenzitadelle (10)" creatureId="36853" creatureName="Sindragosa" difficulty="n" dropRate="6" name="source" value="sourceType.creatureDrop" />
          <filter name="relevance" value="0" />
    </item>
    """
    def __init__(self, data):
        if data:
            self.filter = {}
            try:
                for key in data.keys():
                    self.__dict__[key] = data.get(key)
                for filter in data.findall(".//filter"):
                    f = dict([(key, filter.get(key)) for key in filter.keys()])
                    self.filter[f['name']] = f
            except Exception, e:
                raise Exception('parse error:', e)
        else:
            raise Exception('no item data provided')
        
        self.iLevel = self.filter['itemLevel']['value']
        self.boss = ''
        
        if 'creatureName' in self.filter['source'].keys():
            self.boss = self.filter['source']['creatureName']
        
    def __unicode__(self):
        return u'%s (iLvl: %s)' % (self.name, self. iLevel)
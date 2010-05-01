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

from wow import fetch

DEFAULT_LANGUAGE = 'de-de'

class Translator(object):
    """The Translator translates dungeon or raid shortnames into human readable
    names. The target language can be choosen at object creation time. The
    following languages seem to work: 'de-de', which is also the default value,
    'en-us', 'fr-fr', 'ru-ru'. Since the language only determines the 'Accept-
    Language' header in the HTTP-Request which is sent to Blizzard's server,
    other languages may work."""
    
    def __init__(self, lang = DEFAULT_LANGUAGE):
        self.lang = lang
        # fetch translation tables
        transtable = fetch.load_translations(self.lang)
        self.names = dict([(d.get('key'), d.get('name')) for d in transtable.findall('.//dungeon')])
    
    def translate(self, key):
        """Tries to look up the key in the fetched dungeon names. If there is no
        translation for the key, the key itself is returned."""
        if key in self.names.keys():
            return self.names[key]
        else:
            return key
About
-----

python-wow is a pythonic client library for fetching and using Blizzard's `World of Warcraft Arsenal`_, especially the item database.

.. _World of Warcraft Arsenal: http://www.wowarmory.com/

Installation
------------

still to come

Documentation
-------------

The `wow` package consists of the following modules

- the wow.fetch module provides a wrapper function for Blizzard's armory (which is all xml entirely)
- the wow.api module provides an clean and object oriented interface on top of those services
- the wow.translation module provides some tools to translate some machine information into human readable format, like item ids or dungeon shortnames

Fetching XML data
+++++++++++++++++

The `wow.fetch` module provides very basic and low level access to Blizzard's xml files. For more complex use cases it is recomended to use the object oriented module `wow.api`.
Note: All functions in the `wow.fetch` module return XML data as ElementTree objects. This module is highly inspired by Christian Kreutzer's `python-tvrage`_ project which provieds a similar `feeds`-module.

.. _python-tvrage: http://pypi.python.org/pypi/python-tvrage

Retrieving dungeon data::

    $ python
    >>> from wow.fetch import load_dungeons
    >>> from xml.etree.ElementTree import dump
    >>> dungeons = load_dungeons().findall('.//dungeon')
    >>> for dungeon in dungeons:
    ...     dump(dungeon)
    ...
    <dungeon hasHeroic="1" id="4812" key="icecrowncitadel25" levelMax="80" levelMin="80" nameId="4812" partySize="25" raid="1" release="2" showPartySize="true">
    <bosses>
    <boss id="37957" key="lordmarrowgar" nameId="36612" type="npc">
        <lootTable difficulty="n" id="37957" type="npc" />
        <lootTable difficulty="h" id="37959" type="npc" />
    </boss>
    <boss id="38106" key="ladydeathwhisper" nameId="36855" type="npc">
        <lootTable difficulty="n" id="38106" type="npc" />
        <lootTable difficulty="h" id="38297" type="npc" />
    </boss>
    ...
    </dungeon>
    
The dungeon names (`key` in each dungeon node) and boss names (`key` in each boss node) can be translated with the `Translator` class in the wow.translation module.

The object oriented API
+++++++++++++++++++++++

Translations
++++++++++++

The `wow.translation` module provides some basic functionality on translating the shortnames or ids contained in the xml data into human readable names.
This module does not provide any possibility to translate names from one language into another.

The translation tables are loaded from the Armory each time a Translator object is created, which means one should keep the reference once a Translator is created.

    $ python
    >>> from wow.translation import Translator
    >>> de = Translator()
    >>> de.translate('ahnkahet')
    u"Ahn'kahet: Das Alte K\xf6nigreich"
    >>> fr = Translator('fr-fr')
    >>> fr.translate('ahnkahet')
    u"Ahn'kahet\xa0: l'Ancien royaume"

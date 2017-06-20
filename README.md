### ReadMe contents ###

on this page...
- [qualifier](#qualifier)
- [code overview](#codecontext-overview)
- [contacts](#contacts)


### Qualifier ###

This is ancient code recently updated just enough to release publicly. It was one of my first python projects; there's still lots of evidence of my camelCase everything's-a-class java background.


### Code/Context overview ###

Items are arrive at our offsite storage facility, the [Annex](http://library.brown.edu/about/annex/), either because they're new arrivals there, or because they've been borrowed and are being returned.

This code...

- processes the standard end-of-day reports output by the the [GFA software](http://www.gfatech.com/software-LAS.html)
- creates files for catalogers to access via ftp
- emails the catalogers that the new files are ready
- the catalogers then access the files, and update our [III Millennium ILS](https://www.iii.com/products/millennium)

Related code...

- A [separate script](https://github.com/birkin/josiah_print_pageslips) prepares and exports requests for Annex items.

- Another [separate script](https://github.com/birkin/annex_process_pageslips) periodically checks to see if a new file has arrived, and parses that pageslip file into the files needed for the Annex's inventory-control software.


### Contacts ###

Domain contact: bonnie_buzzell@brown.edu

Programmer: birkin_diana@brown.edu

---

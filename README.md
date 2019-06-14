_on this page..._

- [qualifier](#qualifier)
- [code overview](#codecontext-overview)
- [contacts](#contacts)

---

### Qualifier ###

- This is ancient code initially updated just enough to release publicly. It was one of my first python projects; there's still lots of evidence of my camelCase everything's-a-class java background.


### Code/Context overview ###

Items are arrive at our offsite storage facility, the [Annex](http://library.brown.edu/about/annex/), either because they're new arrivals there, or because they've been borrowed and are being returned.

This code...

- processes the standard end-of-day reports output by the the [GFA software](http://www.gfatech.com/software-LAS.html)
- creates files for catalogers to access via ftp
- posts counts to a separate [annex-counts webservice](https://github.com/birkin/annex_counts_project)
- emails the catalogers that the new files are ready
    - the catalogers then access the files, and update our [Sierra](https://www.iii.com/products/sierra-ils/) [ILS](https://en.wikipedia.org/wiki/Integrated_library_system)

Related code...

- A [separate script](https://github.com/Brown-University-Library/transfer_annex_pageslips) gets Annex requests in the form of pageslips to a location where they will be subsequently parsed.
- Another [separate script](https://github.com/Brown-University-Library/annex_process_email_pageslips) periodically checks to see if a new pageslips-file has arrived, and parses that pageslips-file into the files needed for the Annex's inventory-control software.


### Contacts ###

developer: birkin_diana@brown.edu

---

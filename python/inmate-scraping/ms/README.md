# MS data scrapping
MS has a relatively open database (no CAPTCHA, etc.). However, data about race 
and unit are stored in a details page. Details pages ca only be accessed once a 
browser session has been opened and an initial search has been conducted.

This workflow avoids the problem of needing to access each details page by
first downloading all the search results, sampling from the results based
on facility, and then only retrieving the details for the sampled results.

This full detail structures are then sampled for race and facility.

##  Workflow

download_db.py -> cleanup_db.py -> sample_facility -> download_inmate_details.py -> cleanup_inmate_details.py -> sample_race_and_facility.py

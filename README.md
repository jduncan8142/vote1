# Vote1

## vote1 scripts:

* generate_voter_codes.py -> Creates voter codes for myvote.io an online voting app.
	* Once created use the myvote.io portal to update the code for your poll. 
* post_check.py -> Does a set of post processing steps once voting is complete. 
	* Reviews the poll-results-export.csv and poll-votes.csv files to make sure voters
	  only voted once. Voter records with more than 1 vote are excluded from the results.

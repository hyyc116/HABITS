###Diseases-Scales-Therapies Network
This directory mainly includes the codes of DSTN based therapy finding.

	1. Crawled stroke related papers from PubMed with Crawler, data file is one record one line, line format is pmid \t abstract.
	2. Extract all NPs by using np_extractor.py. <br/>
	python np_extractor.py saved_NPs.txt stroke_abs.txt 1>>saved_NPs.txt 2>run.log 
	3. Identify scales and therapies from NPs extracted. <br/>
	python therapy_filter.py saved_NPs.txt > stroke_therapy.txt <br/>
	python scale_filter.py saved_NPs.txt > stroke_scale.txt <br />
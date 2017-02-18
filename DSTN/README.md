###Diseases-Scales-Therapies Network
This directory mainly includes the codes of DSTN based therapy finding.

###Prerequisites
	[NLTK](http://www.nltk.org)  
	[CHUNK PARSER](https://github.com/biplab-iitb/practNLPTools) 



####1. Fetch stroke related papers from PubMed with Crawler. 
	Data file named as stroke.txt in which one record one line, line format is pmid \t abstract.
####2. Extract all NPs by using np_extractor.py. 
	python np_extractor.py saved_NPs.txt stroke_abs.txt 1>>saved_NPs.txt 2>run.log 
####3. Identify scales and therapies from NPs extracted. 
	python therapy_filter.py saved_NPs.txt > stroke_therapy.txt 
	python scale_filter.py saved_NPs.txt > stroke_scale.txt
####4. Domain expert checking, filter out error items.
	The results are labeled as "KNOWN_SCALES" and "KNOWN_THERAPIES".

####5. Fetch articles of all scales in KNOWN_SCALES.
	File is named as scales.txt in which one record one line, line format is pmid \t abstract.

####6. Extract all possible therapies from crawled scales data.
	python np_extractor.py scale_NPs.txt stroke_abs.txt 1>>scale_NPs.txt 2>run.log 
	python therapy_filter.py scale_NPs.txt > scale_therapy.txt 

####7. Filter out therapies already in KNOWN_TERAPIES and got a collection NEW_THERAPIES and the intermediate SCALE name between new therapy and stroke.
	In this step, we could use the therapies in stroke_therapy.txt as KNOWN_THERAPIES to filter the result.

####8. Human Checking and get the final result.
	Although, we have got a result, but due to the precision in therapy extraction, there are still some nosies in the NEW_THERAPIES which will be filtered by human checking. 
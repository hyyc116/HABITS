### Diseases-Scales-Therapies Network
This directory mainly includes the codes of DSTN based therapy finding.

### Prerequisites
	[NLTK](http://www.nltk.org)
	[CHUNK PARSER](https://github.com/biplab-iitb/practNLPTools)

#### 1. Fetch stroke related papers from PubMed with Crawler.
	Data file named as stroke_abstract.txt in which one record one line, line format is pmid \t abstract. two zip files are located in data folder.

	unzip stroke_abstract_1.txt.zip
	unzip stroke_abstract_2.txt.zip
	cat stroke_abstract_1.txt stroke_abstract_2.txt > stroke_abstract.txt

#### 2. Extract all NPs by using np_extractor.py.
	python np_extractor.py data/saved_NPs.txt data/stroke_abstract.txt 1>>data/saved_NPs.txt 2>run_extraction.log

#### 3. Identify scales and therapies from NPs extracted.
	python therapy_filter.py data/saved_NPs.txt > data/stroke_therapy.txt
	python scale_filter.py data/saved_NPs.txt > data/stroke_scale.txt

#### 4. Domain expert checking, filter out error items.
	The results are labeled as "KNOWN_SCALES" and "KNOWN_THERAPIES".

#### 5. Fetch articles of all scales in KNOWN_SCALES.
	File is named as data/scales_abstract.txt saved as zip file in data folder in which one record one line, line format is pmid \t abstract.

#### 6. Extract all possible therapies from crawled scales data.
	python np_extractor.py data/scale_NPs.txt data/scales_abstract.txt 1>>data/scale_NPs.txt 2>run.log
	python therapy_filter.py data/scale_NPs.txt > data/scale_therapy.txt

#### 7. Filter out therapies already in KNOWN_TERAPIES and got a collection NEW_THERAPIES and the intermediate SCALE name between new therapy and stroke.
In this step, we could use the therapies in stroke_therapy.txt as KNOWN_THERAPIES to filter the result.

	python scale_new_therapy_linking.py data/stroke_therapy.txt data/stroke_scale.txt data/scale_therapy.txt data/scale_NPs.txt > data/stroke_new_therapy_links.txt


#### 8. Human Checking and get the final result.
	Although, we have got a result, but due to the precision in therapy extraction,
	there are still some nosies in the NEW_THERAPIES which will be filtered out by human checking.


(we share the data crawled from pubmed in data folder, the internal files generated in the processing can be gotten by running the code.)
{\rtf1\ansi\ansicpg1252\cocoartf1504\cocoasubrtf810
{\fonttbl\f0\fswiss\fcharset0 ArialMT;\f1\fnil\fcharset222 Thonburi;}
{\colortbl;\red255\green255\blue255;\red26\green26\blue26;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c13333\c13333\c13333;\cssrgb\c100000\c100000\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww21960\viewh13820\viewkind0
\deftab720
\pard\pardeftab720\sl220\partightenfactor0

\f0\fs30 \cf2 \cb3 \expnd0\expndtw0\kerning0
Before you start up the program, you need to install these packages.\cb1 \
\cb3 - \cb1 MongoDB\cb3 \'a0(https://docs.mongodb.com/manual/installation/)\cb1 \
- pip install scipy\
- pip install sklearn\
- pip install nltk\
- pip install cloudpickle\
-\'a0pip install pymongo.\
\
Since we don't have twitter data yet, I use CiteUlike\'a0data as the demo.\
For the first time you have to run \
- Run createDB.py\'a0to initialize the database (Add data to MongoDB)\
- Run Main.py\'a0to startup system\
- Send POST request (http://128.230.213.66:8080/train) without body, so the system can initialize the model. (This initialization\'a0may take times 30mins-1hour depend on you machine)\
\
Next time you can just run Main.py to startup system.\
We provide 3 POST request\
- http://128.230.213.66:8080/query (The output will rank from the most relevant text)\
	JSON Body:\
	\{\
		"userID":"1",\
		"metaCard":[\
			"The metabolic world of escherichia coli is not small",\
			"Comprehensive protein protein interaction maps promise to reveal many aspects of the complex regulatory network underlying cellular function.",\
			"Techniques are also increasing in complexity as the relevant technologies evolve. A standard representation of both the\'85..\'94\
		]\
	\}\
	JSON Return:\
	\{\
  		"0": "Comprehensive protein protein interaction maps promise to reveal many aspects of the complex regulatory network underlying cellular function.",\
  		"1": "The metabolic world of escherichia coli is not small",\
  		"2": "Techniques are also increasing in complexity as the relevant technologies evolve. A standard representation of both \'85\'85.\'94\
	\}\
\
-\'a0http://128.230.213.66:8080/update (This will update the user preference list)\
	JSON Body:\
	\{\
		"userID":"0",\
		"items":[\
			\{"itemID\'94:\'940A\'94, "itemDes":"Test Des item 0A\'94\},\
			\{"itemID\'94:\'941A\'94, "itemDes":"Test Des item 1A\'94\},\
			\{"itemID\'94:\'942A\'94, "itemDes":"Test Des item 2A\'94\}\
		]\
	\}\
	JSON Return:\
	\{'status': 'Update Done'\}\
\
-\'a0http://128.230.213.66:8080/train\
	JSON Body: -\
	JSON Return:\
	\{'status': 'Update Done'\}\
	\
If you want to use 
\f1 your own
\f0  data. You can clean up the database by using mongoDB shell and use command (db.dropDatabase()),\
and start Main.py. \
- Then you update all the data by using update endpoint.\
- Call http://128.230.213.66:8080/train\
- Do query\
\
\
\
}
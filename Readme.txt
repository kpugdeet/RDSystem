Before you start up the program, you need to install these packages.
- MongoDB (https://docs.mongodb.com/manual/installation/)
- pip install scipy
- pip install sklearn
- pip install nltk
- pip install cloudpickle
- pip install pymongo.

Since we don't have twitter data yet, I use CiteUlike data as the demo.
For the first time you have to run 
- Run createDB.py to initialize the database (Add data to MongoDB)
- Run Main.py to startup system
- Send POST request (http://128.230.213.66:8080/train) without body, so the system can initialize the model. (This initialization may take times 30mins-1hour depend on you machine)

Next time you can just run Main.py to startup system.
We provide 3 POST request
- http://128.230.213.66:8080/query (The output will rank from the most relevant text)
	JSON Body:
	{
		"userID":"1",
		"metaCard":[
			"The metabolic world of escherichia coli is not small",
			"Comprehensive protein protein interaction maps promise to reveal many aspects of the complex regulatory network underlying cellular function.",
			"Techniques are also increasing in complexity as the relevant technologies evolve. A standard representation of both the…..”
		]
	}
	JSON Return:
	{
  		"0": "Comprehensive protein protein interaction maps promise to reveal many aspects of the complex regulatory network underlying cellular function.",
  		"1": "The metabolic world of escherichia coli is not small",
  		"2": "Techniques are also increasing in complexity as the relevant technologies evolve. A standard representation of both …….”
	}

- http://128.230.213.66:8080/update (This will update the user preference list)
	JSON Body:
	{
		"userID":"0",
		"items":[
			{"itemID”:”0A”, "itemDes":"Test Des item 0A”},
			{"itemID”:”1A”, "itemDes":"Test Des item 1A”},
			{"itemID”:”2A”, "itemDes":"Test Des item 2A”}
		]
	}
	JSON Return:
	{'status': 'Update Done'}

- http://128.230.213.66:8080/train
	JSON Body: -
	JSON Return:
	{'status': 'Update Done'}
	
If you want to use your own data. You can clean up the database by using mongoDB shell and use command (db.dropDatabase()),
and start Main.py. 
- Then you update all the data by using update endpoint.
- Call http://128.230.213.66:8080/train
- Do query





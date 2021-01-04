MoonActive OCR challenge: vehicle registration plate detection
by: Omri Zedan

In this project I perform vehicle registration plate detection on registration plate images in a small local dataset.
Based on the retrieved registration plate number, a decision is made as for whether the car should be permitted to enter a hypothetical parking lot. the decision alongside it's reason are then saved to relational database.

prerequisites:
	
1.	OpenCV: python package for loading images.
	docs and installation guide: https://pypi.org/project/opencv-python/
	
2.	PostgreSQL: Relational database. Utilized for this project is Postgres.
	installation guide: https://medium.com/@amitrani/getting-started-with-postgresql-5990b54f7169
	
3.	pytesseract: OCR capabilities. pytesseract is a python wrapper for Google’s Tesseract-OCR Engine.
	docs and installation guide: https://pypi.org/project/pytesseract/
	
4.	SQLAlchemy: python package for data base connection. 
	docs and installation guide: https://pypi.org/project/SQLAlchemy/
	
5.	Pandas: python pckage for data handling and easy conversion from raw data to SQL table. 
	installation guide: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
	pandas&postgres: https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43
	

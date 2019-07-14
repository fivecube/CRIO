# Programming_Problem_Solver
A PyQT5 desktop Application That analyse user's programming query and fetch the most relevant answers of the most relevant questions.

### Quick Installation:
>>> Inside the repositry type:
```pip install -r requirements.txt```
 and than to download Spacy English Model(11mb) type:
```python -m spacy download en_core_web_sm``` 
## --------------------------------------------------------------
>>> If you wish to install them the long way:
1) Python 3.6
2) Pandas
```pip install pandas```  
3) spacy
```pip install spacy```  
3) ibm_watson_cloud_sdk
```pip install --upgrade ibm-watson```  
4) PyQt5
```pip install pyQt5```  
5) pyQtWebEngine
```pip install PyQtWebEngine```  
6) numpy
```pip install numpy```  
7) nltk
```pip install nltk```
8) Spacy English Model
```python -m spacy download en_core_web_sm```  
## --------------------------------------------------------------

## How to run this application:
```python code.py```

You will get a screen like this:

![Alt Text](images/Capture1.PNG)

Enter the query on the Text Box where "Powered by Ibm cloud is printed" and WAIT for 1 minute(Aprox) for WATSON,and other task to happen
For Example:

![Alt Text](images/Capture2.PNG)

You can see all the top answers by next and previous button provided in the gui:

![Alt Text](images/Capture4.png)

You can also see the command prompt to see what is happening in the background:

![Alt Text](images/Capture3.PNG)


>>> Speciality:  
1). We can clearly see in the 3rd image in ```RELEVANT TAGS DECIDING PHASE``` that where-clause was ```removed``` by our Custom Model trained on IBM WATSON KNOWLEDGE STUDIO to check if a tag is relevant or not.  
2). Best Answers are shown highlighted  first and than next answers can be seen by next arrow.  
3). Complex features are made based on Quesiton title to check the text similarity with the user's query  

## PPT LINK:  
https://drive.google.com/file/d/1wX_WRGH3No4DQZ8CONdEZlwj1qK3flGO/view?usp=sharing

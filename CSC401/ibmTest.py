# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
# 		the specifications exactly. DO NOT modify the headers of any
#		functions. Doing so will cause your program to fail the autotester.
#
#		You may use whatever libraries you like (as long as they are available
#		on CDF). You may find json, request, or pycurl helpful.
#		You may also find it helpful to reuse some of your functions from ibmTrain.py.
#

import urllib
import urllib2
import base64
import requests
import json
import csv




def get_classifier_ids(username,password):
	# Retrieves a list of classifier ids from a NLClassifier service 
	# an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#		
	# Returns:
	#	a list of classifier ids as strings
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason
	#
	result = requests.get("https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers", auth=(username, password) )

	unparsed = result.text.split(" ")
	count = 0
	urls = []
	for word in unparsed:
		word = word.replace('"', "")
		word = word.replace('\n', "")
		if word[0:6] == "https:":
			urls.append(word.encode('utf-8')[:-1])

		count+=1
	return urls



def assert_all_classifiers_are_available(username, password, classifier_id_list):
	# Asserts all classifiers in the classifier_id_list are 'Available' 
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id_list - a list of classifier ids as strings
	#		
	# Returns:
	#	None
	#
	# Error Handling:
	#	This function should throw an exception if the classifiers call fails for any reason AND 
	#	It should throw an error if any classifier is NOT 'Available'
	#
	for url in classifier_id_list:
		result = requests.get(url, auth=(username, password) )
		if  result.text.split("\n")[-2] != '  "status_description" : "The classifier instance is now available and is ready to take classifier requests."':
			return False
	return True

def classify_single_text(username,password,classifier_id,text):
	# Classifies a given text using a single classifier from an NLClassifier 
	# service
	#
	# Inputs: 
	# 	username - username for the NLClassifier to be used, as a string
	#
	# 	password - password for the NLClassifier to be used, as a string
	#
	#	classifier_id - a classifier id, as a string
	#		
	#	text - a string of text to be classified, not UTF-8 encoded
	#		ex. "Oh, look a tweet!"
	#
	# Returns:
	#	A "classification". Aka: 
	#	a dictionary containing the top_class and the confidences of all the possible classes 
	#	Format example:
	#		{'top_class': 'class_name',
	#		 'classes': [
	#					  {'class_name': 'myclass', 'confidence': 0.999} ,
	#					  {'class_name': 'myclass2', 'confidence': 0.001}
	#					]
	#		}
	#
	# Error Handling:
	#	This function should throw an exception if the classify call fails for any reason 
	#
	result = requests.get(classifier_id+"/classify?text="+text, auth=(username, password) )
	lines = result.text.split("\n")
	if "0" in lines[4]:
		className = "0"
	else:
		className = "4"
	zeroConfidence = float(lines[7].split(" ")[-1].encode('utf-8'))
	dict = {'top_class':className,
				  'classes': [
							{'class_name': '0', 'confidence': zeroConfidence} ,
						  	{'class_name': '4', 'confidence': 1 - zeroConfidence}
							  ]
		}

	return (dict)


def classify_all_texts(username,password,input_csv_name):
        # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
        # service.
        #
        # Inputs:
        #       username - username for the NLClassifier to be used, as a string
        #
        #       password - password for the NLClassifier to be used, as a string
        #      
        #       input_csv_name - full path and name of an input csv file in the 
        #              6 column format of the input test/training files
        #
        # Returns:
        #       A dictionary of lists of "classifications".
        #       Each dictionary key is the name of a classifier.
        #       Each dictionary value is a list of "classifications" where a
        #       "classification" is in the same format as returned by
        #       classify_single_text.
        #       Each element in the main dictionary is:
        #       A list of dictionaries, one for each text, in order of lines in the
        #       input file. Each element is a dictionary containing the top_class
        #       and the confidences of all the possible classes (ie the same
        #       format as returned by classify_single_text)
        #       Format example:
        #                      [
        #                              {'top_class': 'class_name',
        #                              'classes': [
        #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
        #                                         {'class_name': 'myclass2', 'confidence': 0.001}
        #                                          ]
        #                              },
        #                              {'top_class': 'class_name',
        #                              ...
        #                              }
        #                      ]
        #                      [
        #
        #                      ]
        #
        #              }
        #
        # Error Handling:
        #       This function should throw an exception if the classify call fails for any reason
        #       or if the input csv file is of an improper format.
        #
		with open(input_csv_name, 'rb') as csvfile:
			count = 0
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			dicts1 = []
			dicts2 = []
			dicts3 = []
			results = {"500": dicts1,
					   "1000": dicts2,
					   "2500": dicts3}
			for line in csvreader:
				dicts1.append(classify_single_text(username,password,ids[0],line[5]))
				dicts2.append(classify_single_text(username,password,ids[1],line[5]))
				dicts3.append(classify_single_text(username,password,ids[2],line[5]))

		csvfile.close()
		return results



def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the accuracy of this
	# classifier according to the input csv file
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#
	with open(input_csv_file_name, 'r') as csvfile:
		correct = 0.0
		total = 0.0
		for line in csvfile:
			score = str(line.split(",")[0]).replace("\"", "" )
			if score == str(classifier_dict[int(total)]['top_class'])[-1]:
				correct += 1.0
			total+=1
	csvfile.close()
	
	return correct/float(total)

def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
	# Given a list of "classifications" for a given classifier, compute the average 
	# confidence of this classifier wrt the selected class, according to the input
	# csv file. 
	#
	# Inputs:
	# 	classifier_dict - A list of "classifications". Aka:
	#		A list of dictionaries, one for each text, in order of lines in the 
	#		input file. Each element is a dictionary containing the top_class
	#		and the confidences of all the possible classes (ie the same
	#		format as returned by classify_single_text) 	
	# 		Format example:
	#			[
	#				{'top_class': 'class_name',
	#			 	 'classes': [
	#						  	{'class_name': 'myclass', 'confidence': 0.999} ,
	#						  	{'class_name': 'myclass2', 'confidence': 0.001}
	#							]
	#				},
	#				{'top_class': 'class_name',
	#				...
	#				}
	#			]
	#
	#	input_csv_name - full path and name of an input csv file in the  
	#		6 column format of the input test/training files
	#
	# Returns:
	#	The average confidence of the classifier, as a number between [0.0-1.0]
	#	See the handout for more info.
	#
	# Error Handling:
	# 	This function should throw an error if there is an issue with the 
	#	inputs.
	#

	with open(input_csv_file_name, 'r') as csvfile:
		correct = 0.0
		incorrect = 0.0
		correctTotal = 0.0
		incorrectTotal = 0.0
		total = 0.0
		for line in csvfile:
			score = str(line.split(",")[0]).replace("\"", "" )
			if score == str(classifier_dict[int(total)]['top_class'])[-1]:
				confidences = classifier_dict[int(total)]['classes']
				if confidences[0]['class_name'] == str(classifier_dict[int(total)]['top_class']):
					correct += float(confidences[0]['confidence'])
					correctTotal+=1
				else:
					correct += float(confidences[1]['confidence'])
					correctTotal+=1
			else:
				confidences = classifier_dict[int(total)]['classes']
				if confidences[0]['class_name'] == str(classifier_dict[int(total)]['top_class']):
					incorrect += float(confidences[0]['confidence'])
					incorrectTotal+=1
				else:
					incorrect += float(confidences[1]['confidence'])
					incorrectTotal+=1
			total+=1


	csvfile.close()
	

	
	return [correct/correctTotal, incorrect/incorrectTotal]


if __name__ == "__main__":

	input_test_data = '/u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv'
	accuracy = [0,0,0]
	confidence = [[],[],[]]
	username = "7422dc1e-036c-4376-9410-c5aae79bed98"
	password = "O06Y0bsqbXIX"
	ids = get_classifier_ids(username,  password)
	#STEP 1: Ensure all 11 classifiers are ready for testing
	if assert_all_classifiers_are_available(username,  password, ids):
                #STEP 2: Test the test data on all classifiers
		dict = classify_all_texts(username,  password, input_test_data)
		count = 0
		for classifier in ["500", '1000', "2500"]:
			accuracy[count] = compute_accuracy_of_single_classifier(dict[classifier], input_test_data)
			confidence[count] = compute_average_confidence_of_single_classifier(dict[classifier], input_test_data)
			count+=1
		count = 0
		for classifier in ["500", '1000', "2500"]:
                        #STEP 3: Compute the accuracy for each classifier
			print("Accuracy for classifier : "+classifier)
			print (str(accuracy[count])+"\n")
			#STEP 4: Compute the confidence of each class for each classifier
			print("Confidence for classifier : "+classifier)
			print (str(confidence[count])+"\n")
			count+=1
	else:
		print ("Not all machines trained")
	

	
	
	
	
	
	
	
	

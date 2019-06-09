# NLP-Dialog-Act-Classification

Dialog act classification is an important component of a dialog system; it helps the system  determine what it should do next (e.g., ask a question, ask for a clarification). Using the training and test data provided in the DialogAct.train and DialogAct.test files respectively, train and evaluate a dialog act classifier.

For each advisor turn in the data, you will use the previous turn (statement) to extract features, and use the dialog act of the advisor as the label. For this part of the assignment, you will simply have to adapt the Naive Bayes classifier implementation from the third assignment: train the classifier on the dialog acts in the training data, and use the classifier to predict the dialog acts in the test data. Similar to the third assignment, the features consist of the words in the turns.

Assume the following example:
Student: I was hoping to take 280 next semester.
Advisor: [push-general-info-inform] You have to enroll in 183 before you can enroll in 280.
Student: So maybe I should take 183 instead?
Advisor: [push-tailored-info-suggest] Yes, I recommend that you take 183.

This will result in two learning instances:
 
Features extracted from “I was hoping to take 280 next semester.” Label: push-general-info-inform Features extracted from “So maybe I should take 183 instead?” Label: push-tailored-info-suggest

Programming guidelines:
Write a Python program DialogAct.py that implements the Naive Bayes algorithm to predict a dialog act. Your program should perform the following steps:

➔ Collect all the counts you need from your training data.
➔ Use this Naive Bayes classifier to predict the dialog acts in the test data.
➔ Apply the Naive Bayes classification on the test data.
➔ Evaluate the performance of your system by comparing the predictions made by your Naive Bayes classifier on the test data against the ground truth annotations (available as dialog act labels in the test data).

Considerations for the Naive Bayes implementation:

➔ All the words found in the previous turn (statement) will represent the features to be considered
➔ Address zero counts using add-one smoothing
➔ Work in log space, to avoid underflow due to the repeated multiplication of small numbers

The DialogAct.py program should be run using a command like this:
% python DialogAct.py DialogAct.train DialogAct.test

The program should produce at the standard output the accuracy of the system, as a percentage. It should also generate a file called DialogAct.test.out, which includes all the turns in the test data   and the predicted dialog acts next to each advisor turn.

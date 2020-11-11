# -*- coding: utf-8 -*-
"""Copy of 2020-10-18_Anish_Lesson16

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UFSi7h2aUdiwvzGkVN7tjMqpbnhbS0SA

# Lesson 16: Hunting Exoplanets In Space - Deploying A Prediction Model

### Teacher-Student Activities

In the last class, we learnt how to create line plots and scatter plots to visualise data. 

In this class, we will deploy a prediction model to predict which stars in the test dataset have a planet and which do not. The prediction model, through the training dataset, will learn the properties of a star that has a planet and also the properties of a star which does not have a planet. Once the model has learnt the required properties, it will look for these properties in the test dataset and according to the properties it sees, it will predict whether a star has a planet or not.

In this class, we will learn how to deploy the **Random Forest Classifier** model (a machine learning algorithm). Machine learning is a branch of artificial intelligence in which a machine learns through data the different features on its own without being programmed by a computer programmer. 


<img src='https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/images/lesson-14/ml-vs-ai.png' width=700>

In this case, the machine will learn to recognise the flux values of stars having a planet on its own. When a new dataset containing only the flux values of a star is shown to the machine, it will tell the star having a planet and not having a planet.

There are many machine learning models or algorithms to do this kind of prediction. One of them is **Random Forest Classifier**. It is used to classify outcomes into classes (or labels) based on some features. For e.g., an animal that makes a 'Meow! Meow!' sound is classified (or labelled) as a cat, an animal that makes a 'Woof! Woof!' sound is classified as a dog, an animal which makes a hissing sound is classified as a snake etc.

In this lesson, we will use the Random Forest Classifier model to classify whether a star has a planet or not. The stars which have at least one planet are labelled as `2` while the stars not having a planet are labelled as `1`. 


Let's run all the codes in the code cells that we have already covered in the previous classes and begin this class from **Activity 1: The `value_counts()` Function** section.  You too run the code cells until the first activity.

---

#### Loading The Datasets

Create a Pandas DataFrame every time you start a Jupyter notebook.

Dataset links (Don't click on them):

1. Train dataset 

   https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/kepler-exoplanets-dataset/exoTrain.csv

2. Test dataset 
   
   https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/kepler-exoplanets-dataset/exoTest.csv
"""

# Loading both the training and test datasets.
import pandas as pd

exo_train_df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/kepler-exoplanets-dataset/exoTrain.csv')
exo_test_df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/kepler-exoplanets-dataset/exoTest.csv')

# Number of rows and columns in the DataFrames.
print(exo_train_df.shape)
exo_test_df.shape

"""In the previous classes, we have already checked that the training dataset does not have any missing value. So, we can skip the missing values check part.

---

#### Activity 1: The `value_counts()` Function
Our prediction model should classify the stars either as `1` or `2`. Let's find out how many stars in the test dataset are classified as `1` and `2`.

To compute how many times a value occurs in a series, we use the `value_counts()` function.
"""

# Student Action: Count the number of times a value occurs in a Pandas series.
exo_test_df['LABEL'].value_counts()

"""There are `565` stars which are classified as `1` and `5` stars classified as `2` which means only `5` stars have a planet. Interestingly, if our prediction model mindlessly classifies every star as `1`, then it is a very accurate model. Why?

Because the accuracy of a model is calculated as **a percentage of the correct predictions out of the total number of predictions**. In this case, the percentage of the correct predictions is

 $\frac{565\times100}{570} = 99.122$ %

Thus, without actually deploying a proper prediction model, we can predict the stars having a planet with 99% accuracy. 

This is **WRONG**! This is where we need to be careful. Because we have very imbalanced data. The ultimate goal of the Kepler space telescope is to detect exoplanets in outer space. Hence, a machine learning model, based on some data should also **correctly** detect stars having planets. This means a prediction model will be considered useful if it correctly detects almost all the stars having a planet.

So, the prediction model which always labels every star as `1` is useless. Because it must detect almost all the stars having a planet.

Now, we are going to deploy the Random Forest Classifier model so that it can detect all the five (or at least three) stars having a planet.

---

### Random Forest Classifier^ 

A Random Forest is a collection (a.k.a. ensemble) of many decision trees. A decision tree is a flow chart which separates data based on some condition. If a condition is true, you move on a path otherwise, you move on to another path.


For e.g., in case of finding a star having a planet, you can construct the following decision tree: 

<img src='https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/images/lesson-14/decision-tree.png' width=600>

You could ask a question whether there is decrease in the flux values of a star. If the answer is no, then it clearly means the star does not have a planet. However, if the answer is yes, then you could ask another question to check whether the decrease is periodic or not. Again, if the answer is no, then the star does not have a planet. Otherwise, it has a planet.

This is one of the examples of a decision tree. Based on a problem, the decision tree could get more and more complex. 

A collection of `N` number of trees is a random forest wherein each tree gives some predicted value (in this case either class `1` or class `2`). 

<img src='https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/images/lesson-14/rfc-image.jpg' width=800>

The final predicted value is the majority class, i.e, the class that is predicted by the most number of decision trees in a random forest.

For the time being, just consider the Random Forest Classifier as some kind of a black-box which classifies data into different classes (in this case, either class `1` or class `2`) by learning the properties of every class through a training dataset.

---

#### Activity 2: Importing `RandomForestClassifier`

We need to import a module called `RandomForestClassifier` from a package called `sklearn.ensemble`. The `sklearn` (or **scikit-learn**) is a collection of many machine learning modules. Almost every machine learning algorithm can be directly applied without a knowledge of math using the **scikit-learn** library. It is kind of a plug-and-play device.

You can read about it in the link provided in the **Activities** section under the title **`scikit-learn` - Random Forest Classifier**
"""

# Teacher Action: Import the required modules from the 'sklearn' library.
# Import the 'RandomForestClassifier' module from the 'sklearn.ensemble' library.
from sklearn.ensemble import RandomForestClassifier

"""---

#### Activity 3: Target & Feature Variables Separation

The `RandomForestClassifier` module has a function called `fit()` which takes two inputs. The first input is the collection of feature variables. 

*The features are those variables which describe the features or properties of an entity.* In this case, the `FLUX.1` to `FLUX.3197` are feature variables. Hence, the values stored in these columns are the features of a star in exoplanets dataset.

The second input is the target variable. 

*The variable which needs to be predicted is called a target variable.* In this case, the `LABEL` is the target variable because the prediction model needs to predict which star belongs to which class in the test dataset. Hence, the values stored in the `LABEL` column are the target values. 

So, we need to extract the target variable and the feature variables separately from the training dataset. 

Let's store the feature variables in the `x_train` variable and the target variable in the `y_train` variable. We will separate the features using the `iloc[]` function. 

We need all the rows from the training set. So, inside the `iloc[]` function, we will enter the colon (`:`) sign to get all the rows. We do not need the first column, i.e., the `LABEL` column. Therefore, inside the `iloc[]` function, as part of column indexing, enter `1` as the starting index followed by the colon (`:`) sign to include the rest of the columns from the training dataset.
"""

# Student Action: Extract the feature variables from the training dataset using the 'iloc[]' function.
x_train = exo_train_df.iloc[ :,1:]
x_train.head()

"""Now, let's get only the target variables from the training dataset."""

# Student Action: Using the 'iloc[]' function, retrieve only the first column, i.e., the 'LABEL' column from the training dataset.
y_train = exo_train_df.iloc[ :,0]
y_train.head()

"""---

#### Activity 4: Fitting The Model

Now that we have separated the feature and target variables for deploying the `RandomForestClassifier` model, let's train the model with the feature variables using the `fit()` function. The steps to be followed are described below.

1. First, call the `RandomForestClassifier` module with inputs as `n_jobs=-1` and `n_estimators=50`. Store the function in a variable with the name `rf_clf`.

  For the time being, ignore the reason behind providing the `n_jobs=-1` parameter as an input.

  ```
  rf_clf = RandomForestClassifier(n_jobs=-1, n_estimators=50)
  ```

  The `n_estimators` parameter defines the number of decision trees in a Random Forest. Therefore, `n_estimators=50` means that the forest contains `50` decision trees. If `n_estimators` parameter is not defined by a user, then by default, the forest contains `100` decision trees.

2. Call the `fit()` function with `x_train` and `y_train` as inputs.

  ```
  rf_clf.fit(x_train, y_train)
  ```
3. Call the `score()` function with `x_train` and `y_train` as inputs to check the accuracy score of the model. This step is actually not required. If you wish, you can skip this step.
  
  ```
  rf_clf.score(x_train, y_train)
  ```
"""

# Teacher Action: Train the 'RandomForestClassifier' model using the 'fit()' function.

# 1. First, call the 'RandomForestClassifier' module with inputs as 'n_jobs = - 1' & 'n_estimators=50'. Store it in a variable with the name 'rf_clf'.
# For the time being, ignore the reason behind providing the 'n_jobs=-1' parameter as an input.
rf_clf= RandomForestClassifier(n_jobs=-1, n_estimators=50)
# 2. Call the 'fit()' function with 'x_train' and 'y_train' as inputs.
rf_clf.fit(x_train,y_train)
# 3. Call the 'score()' function with 'x_train' and 'y_train' as inputs to check the accuracy score of the model.
rf_clf.score(x_train,y_train)

"""As you can see, we have deployed the `RandomForestClassifier` model with an accuracy of 100% (the number `1.0` signifies 100% accuracy).

---

#### Activity 5: Target & Feature Variables From Test Dataset^^

Now we need to make predictions on the test dataset. So, we just need to extract feature variables from the test dataset using the `iloc[]` function.
"""

# Student Action: Using the 'iloc[]' function, extract the feature variables from the test dataset.
x_test = exo_test_df.iloc[ :,1:]
x_test.head()

"""Let's also extract the target variable from the test dataset so that we can compare the actual target values with the predicted values later."""

# Student Action: Using the 'iloc[]' function, extract the target variable from the test dataset.
y_test = exo_test_df.iloc[ :,0]
y_test.head()

"""---

#### Activity 6: The `predict()` Function^^^

Now, let's make predictions on the test dataset by calling the `predict()` function with the features variables of the test dataset as an input.
"""

# Student Action: Make predictions on the test dataset by using the 'predict()' function.
y_predicted = rf_clf.predict(x_test)
y_predicted

"""The predict function returns a NumPy array of the predicted values. You can verify it using the `type()` function."""

# Student Action: Using the 'type()' function, verify that the predicted values are obtained in the form of a NumPy array.
type(y_predicted)

"""The actual target values are stored in a Pandas series. So, for the sake of consistency, let's convert the NumPy array of the predicted values into a Pandas series."""

# Student Action: Convert the NumPy array of predicted values into a Pandas series.
y_predicted = pd.Series(y_predicted)
y_predicted.head()

"""Now, let's count the number of stars classified as `1` and `2`."""

# Student Action: Using the 'value_counts()' function, count the number of times 1 and 2 occur in the predicted values.
y_predicted.value_counts()

"""As you can see, we did not get the expected results. The model should have classified all the stars having a planet as `2`. Ideally, the Random Forest Classifier model should have classified `565` values as `1` and the remaining `5` values as `2`. 

In this case, even though the accuracy of a prediction model is high but according to the problem statement, it is not giving the desired result. Hence, **accuracy alone is not the metric to test the efficacy of a prediction model.** 

In the next class, we will try to investigate why Random Forest Classifier failed to classify even a single star as `2`. Based on the investigation, we will try to improve the model and then deploy it again.

---
"""
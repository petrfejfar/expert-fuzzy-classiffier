# Expert fuzzy classifier

Petr Fejfar, pfejfar \_at\_ gmail.com

---

## Introduction

This task is lab assignment 3 for Learning systems course at Mälardalen University Sweden - Erasmus+ program 2016.

## Task definition

Task goal is to evaluate precision of fuzzy classifier.

There are extra questions to be answered:

1. What is the AND operator in your implementation?
    - Answer is in section [Fuzzy classifer evaluation](#evaluation)
2. What is the OR operator in your implementation?
    - Answer is in section [Fuzzy classifer evaluation](#evaluation)
3. What is the data flow from inputs to decision given the normalized attribute values as (0.3, 0.8, 0.2, 0.7)? You have to make fuzzy reasoning with hand at this stage. This is a preparation stage to help you make sure that you understand the whole fuzzy reasoning procedure. As long as you truly understand, you will find implementation with programming easy and enjoyable.
    - Answer is in section [Sample evaluation](#sample_evaluation)
4. What is the accuracy of your implemented fuzzy classifier on the Iris data?
    - Answer is in section [Results](#results)

### Classifier definition <a name="classifier"></a>

Classifier is set by expert. Membership function set to
![Membership function](/doc/img/membership_function.png "Membershio function")

and the data needs to be normalized.

Normalization of data is done according to *x'<sub>i</sub> = ( x<sub>i</sub>-min(i) ) / max(i) - min(i)*, where *min(i)* is minimum value of *x<sub>i</sub>* and *max(i)* is maximum value of *x<sub>i</sub>*.

Expert sets the rules as below:

- **r<sub>1</sub>:** If (x<sub>1</sub> = *short*&#8744;*long*) &#8743; (x<sub>2</sub> = *middle*&#8744;*long*) &#8743; (x<sub>3</sub> = *middle*&#8744;*long*) &#8743; (x<sub>4</sub> = *middle*) Then iris **versicolor**.
- **r<sub>2</sub>:** If (x<sub>3</sub> = *short*&#8744;*middle*) &#8743; (x<sub>4</sub> = *short*) Then iris **setosa**.
- **r<sub>3</sub>:** If (x<sub>2</sub> = *short*&#8744;*middle*) &#8743; (x<sub>3</sub> = *long*) &#8743; (x<sub>4</sub> = *long*) Then iris **virginica**.
- **r<sub>4</sub>:** If (x<sub>1</sub> = *middle*) &#8743; (x<sub>2</sub> = *short*&#8744;*middle*) &#8743; (x<sub>3</sub> = *short*) &#8743; (x<sub>4</sub> = *long*) Then iris **versicolor**.

### Data set <a name="dataset"></a>

Data set is taken from benchmark [Iris data](ftp://ftp.ics.uci.edu/pub/machine-learning-databases/). There is 50 samples of three class of iris.


| First column        | Second column      | Third column        | Third column       | Third column                |
| ------------------- | ------------------ | ------------------- | ------------------ | --------------------------- |
| Sepal length (*x1*) | Sepal width (*x2*) | Petal length (*x3*) | Petal width (*x4*) | Class&#8712;{*1*, *2* ,*3*} |

Where class *1* is *iris setosa*, class *2* is *iris versicolor* and class *3* is *iris virginica*.

Example data:

    5.1 3.5 1.4 0.2 1
    4.9 3.0 1.4 0.2 1
    4.7 3.2 1.3 0.2 1
    ...

## Fuzzy classifier evaluation <a name="evaluation"></a>

Algorithm is sequence of following steps:

1. Normalize data
2. Fuzzification
3. Rule matching
4. Fuzzy inference and aggregation
5. Defuzzification

Normalization is done accordign function given in section [Classifier](#classifer).

In *fuzzification* step we calculate degree of membership of each variable to corresponding set (*short*, *middle* and *long*).

In *rule matching* step and *fuzzy inference and aggregation* step we take degree of membership and we combine these values accordingly to *a&#8744;b = max(a, b)* and is *a&#8743;b = min(a, b)*. Result is strength of the rule. We aggregate these strength by summing strength on each class.

*Defuzzification* is done by choosing class with highest value.

### Sample evaluation <a name="sample_evaluation"></a>

We take sample from data:

    5.1 3.5 1.4 0.2 1

We find minimums of data set

    4.3 2.0 1.0 0.1

and maximums

    7.9 4.4 6.9 2.5

Then we normalize data to

    ~0.222 ~0.625 ~0.068 ~0.041 1

We fuzzificate normalized data

| membership of | *x1*   | *x2*   | *x3*   | x4     |
| ------------- | ------ | ------ | ------ | ------ |
| *Short*       | ~0.630 | 0      | ~0.887 | ~0.930 |
| *Middle*      | ~0.370 | ~0.937 | ~0.113 | ~0.070 |
| *Long*        | 0      | ~0.062 | 0      | 0      |

Then we match the rules and we fire strengths of rules

| *r<sub>1</sub>* | *r<sub>2</sub>* | *r<sub>3</sub>* | *r<sub>4</sub>* |
| --------------- | --------------- | --------------- | --------------- |
| ~0.069          | ~0.887          | 0               | 0               |

We fuzzy interfere and aggregate fired rules. In our classifier it means that we sum rule strength for each class. Result is

| *Iris setosa* | *Iris versicolor* | *Iris virginica* |
| ------------- | ----------------- | ---------------- |
| ~0.887        | ~0.069            | 0                |

After defuzzification we get class **Iris setosa**.

## Results <a name="results"></a>

We ran fuzzy classifier at test data and there was determined 117 class correctly and 33 incorrectly. Threfore overall fuzzy classifier precision on given data set is about **78.00%**.

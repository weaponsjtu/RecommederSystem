# Code Document for Recommendation System

This document will describe the code base for Recommendation System (RS) project of Sales Science Team. We implemented basic RS algorithms, including user-based, item-based, content-based, SVD, etc. For the convenience communication, we use Python language. This code base is composed of six modules, including data processing, data model, recommenders, evaluation, graph tools, utils, etc.

If you have any suggestion, please contact me (javawebzwp AT gmail DOT com).

## Code Architecture

1. Data Processing (excel, txt, etc)
2. Data Model (vector, matrix, etc)
3. Recommender (User-based, Item-based, SVD, etc)
4. Evaluation (ROC, RMSE, MAP, F1, NDCG, etc)
5. Graph Tool (ROC, PR curve)
6. Utils (Similarity, etc)

**Library Requirements: Python>=2.7, matplotlib, PyExcel**

## Module API

### Data Processing

1. **class** PreProcessing
   - def process( file\_name ), return matrix
2. **class** ExcelTool
   - def read\_excel( file\_name ), return matrix
   - def write\_excel( matrix, file\_name )

### Data Model

1. **class** MatrixModel
   - def set\_data( matrix )
   - def split\_data( matrix, train\_conf, test\_conf )
   - def is\_train\_sample( date )
   - def is\_test\_sample( date )
   - def sort\_by\_row( matrix )
   - def sort\_by\_col( matrix )
2. **class** User
   - def get\_attr()
   - def set\_attr()
3. **class** Item
   - def get\_attr()
   - def set\_attr()

### Recommender

1. **class** UserBased
   - def user\_similarity( matrix )
   - def related\_users( user\_sim, K )
   - def predict( matrix, related\_users )
2. **class** ItemBased
   - def item\_similarity( matrix )
   - def related\_items( item\_sim, K )
   - def predict( matrix, related\_items )
3. **class** SVD
   - def matrix\_factorization( matrix )
4. **class** ContentBased

### Evaluation

1. **class** Evaluation
   - def eval\_f1( results, test\_data )
   - def eval\_roc( results, test\_data )
   - def eval\_ndcg( results, test\_data )
   - def percent( scores, labels, K, N )

### Graph Tool

1. **class** GraphTool
   - def plot\_pr ()
   - def plot\_roc ()

### Utils

1. **class** Utils 
   - def file2dic( file )
   - def similarity( vector\_a, vector\_b )
   - def save_evaluation( eval\_result, file\_name )
   - def save_ranking( rank\_dic, file\_name )

## How to Use
ITS example

## Code Repository
GMU machine

## About Us
Author: Dongsheng Li, Jin Huang, Weipeng Zhang
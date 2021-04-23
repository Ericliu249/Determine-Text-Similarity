# Text Similarity

- Author: Yang Liu (Eric)
- Contact: eric.liu.249@gmail.com

## Objective

The goal of this project is to run a simple flaks web app inside a docker container that can determine the similiarity between two texts through a HTTP request. Documents that are exactly the same should get a score of 1, and documents that don’t have any words in common should get a score of 0.
## Considerations

1. **Tokenization**

   The process of breaking a stream of textual content up into words, terms, symbols, or some other meaningful elements called tokens. The puncation will be **removed** in this step as they are mostly meaningless.

2. **Stopwords**

    - Stop words: a set of commonly used words, have very little meaning, and cannot differentiate a text from others, such as "and", "the" etc. 
    - Stop words are typically ignored in NLP processing or by search engine
    - Stop words usually are application specific. You can define your own stop words!
    - In this application, stop words are **ignored** for the given texts. If you want to consider stop words when doing the comparision, add ***stopwords=False*** when making the **POST /similarity** request (see example below)

3. **Ordering of words**

   The ordering of words are not considered for the sake of simplicity (and most of the time ordering is also not important). 

4. **Mesure for similiarity**

   - The app will first count the **word frequency** after the tokening the input texts. 

   - Calculate the **Term Frequency and Inverse Dcoument Frequency** (TF-IDF)

     - **Term Frequecy (TF)**

       - Measures how frequently a term, say w, occurs in a document, say 𝑑. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. 
       - Thus, the frequency of 𝑤 in 𝑑, denoted as 𝑓𝑟𝑒𝑞(𝑤,𝑑) is often divided by the document length (a.k.a. the total number of terms in the document, denoted as |𝑑|) as a way of normalization: 𝑡𝑓(𝑤,𝑑)=𝑓𝑟𝑒𝑞(𝑤,𝑑)/|𝑑|

     - **Inverse Document Frequency (IDF)**

       - Measures how important a term is within the corpus.

       - However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance.

       - Thus we need to weigh down the frequent terms while scale up the rare ones.

       - Let |𝐷||D| denote the number of documents, 𝑑𝑓(𝑤,𝐷)df(w,D) denotes the number of documents with term 𝑤w in them. Then,𝑖𝑑𝑓(𝑤)=𝑙𝑛(|𝐷|/𝑑𝑓(𝑤,𝐷))+1

         Or a smoothed version:𝑖𝑑𝑓(𝑤)=𝑙𝑛((|𝐷|+1)/(𝑑𝑓(𝑤,𝐷)+1))+1

     - **TF-IDF**

       Let 𝑠(𝑤,𝑑)=𝑡𝑓(𝑤,𝑑)∗𝑖𝑑𝑓(𝑤)s(w,d)=tf(w,d)∗idf(w), normalize the TF-IDF score of each word in a document normalized by the Euclidean norm, then

       𝑡𝑓𝑖𝑑𝑓(𝑤,𝑑)=𝑠(𝑤,𝑑)√∑𝑤∈𝑑𝑠(𝑤,𝑑)2

   - Use the **Cosine Similarity** to measure the similiary between two texts

     Cosine Similarity is the similarity between two documents is a function of the angle between their vectors in the if-idf vector space.

## Prerequisites

1. Ensure docker is running on you laptop.
   1. To install docker, go to https://docs.docker.com/get-docker, check the version based on the platform you want to run.
   2. After the installation, start the docker desktop.
2. The flask app runs on port **5001**. Please check the port is not taken by other application/service before you run the container.



## Installation

```
$ git clone https://github.com/Ericliu249/Text-Similarity-Docker-Flask-App.git
$ cd Text-Similarity-Docker-Flask-App
$ docker-compose up
```

Access the application via http://localhost:5001

## API

- `GET ${hostname}:5001`

  - Description

    Return the README.md of this project

  - Parameter Values

    None

  - Reuquest Body

    None

  - Response Code

    200

  - Example

    ```
    curl http://localhost:5001
    ```

  - Sample Response

    README of the this project

    ```
    <h1>Text Similarity</h1>
    <ul>
    	<li>Author: Yang Liu (Eric)</li>
    	<li>Contact: eric.liu.249@gmail.com</li>
    </ul>
    <h2>Objective</h2>
    <p>The goal of this project is to run a simple flaks web app
    ...
    ...
    ...
    ```

    

- `POST ${hostname}:5001/similiary?stopwords=True`

  - Description

    Return the similiary score between two given texts. Documents that are exactly the same should get a score of 1, and documents that don’t have any words in common should get a score of 0. Please use the samples below to develop your application.

  - Parameter Values:

    - stopwords (*optional*): Boolean. True (default) or False. If value is True, the stopwords are considered when comparaing the texts. If value is False, stopwords will be treated as normal words and will have impact on the similiary score.

  - Request Body

    ```json
    {
      "text_a": "sample text a",
      "text_b": "sample text b"
    }
    ```

  - Reponse Code

    200

  - Example

    ```
    curl -X POST -H "Content-Type: application/json" -d '{"text_a": "sample text a", "text_b": "sample text b"}' http://localhost:5001/similarity
    ```

  - Sample Response

    ```json
    {
        "message": "Computed the similarity between two texts successfully",
        "similarity": 0.75,
        "success": true
    }
    ```

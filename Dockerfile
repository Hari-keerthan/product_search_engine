FROM python:latest
WORKDIR /usr/src/
RUN pip install flask lxml bs4 requests fuzzywuzzy python-Levenshtein
RUN apt-get install git
RUN git clone https://github.com/hkee96/product_search_engine.git
CMD ["python","/usr/src/product_search_engine/tmpla_test.py"]
EXPOSE 5000

"""
A module that handles all communication with CouchDB database and couchdb-lucene index
"""
import logging
import http.client
import json


class Database():
    """
    http://instance1:5985/local/campaigns/_design/lucene/search?q=is_root:true&include_docs=True
    """
    __DATABASE_URL = 'http://instance1.cern.ch'
    __DATABASE_PORT = 5984
    __DATABASE_HOST = __DATABASE_URL.replace('https://', '').replace('http://', '')
    __LUCENE_URL = 'http://instance1.cern.ch'
    __LUCENE_PORT = 5985
    __LUCENE_HOST = __LUCENE_URL.replace('https://', '').replace('http://', '')
    __TIMEOUT = 90

    def __init__(self, database_name=None):
        """
        Constructor of database interface
        """
        self.database_name = database_name
        self.__database_connection = None
        self.__lucene_connection = None
        self.logger = logging.getLogger()

    def __del__(self):
        """
        Destructor of database interface
        """
        if self.__database_connection:
            self.__database_connection.close()
            self.__database_connection = None

        if self.__lucene_connection:
            self.__lucene_connection.close()
            self.__lucene_connection = None

    def __get_database_connection(self, reuse=True):
        """
        Return an HTTP connection to CouchDB database
        Reuse if there is an existing connection
        reuse=False forces to create a new connection
        """
        if not self.__database_connection or not reuse:
            if self.__database_connection:
                self.__database_connection.close()
                self.__database_connection = None

            self.__database_connection = http.client.HTTPConnection(self.__DATABASE_HOST,
                                                                    port=self.__DATABASE_PORT,
                                                                    timeout=self.__TIMEOUT)

        return self.__database_connection

    def __get_lucene_connection(self, reuse=True):
        """
        Return an HTTP connection to couchdb-lucene index
        Reuse if there is an existing connection
        reuse=False forces to create a new connection
        """
        if not self.__lucene_connection or not reuse:
            if self.__lucene_connection:
                self.__lucene_connection.close()

            self.__lucene_connection = http.client.HTTPConnection(self.__LUCENE_HOST,
                                                                  port=self.__LUCENE_PORT,
                                                                  timeout=self.__TIMEOUT)

        return self.__lucene_connection

    def __make_request(self, connection, path, method='GET', data=None):
        """
        Make a HTTP request to a given connection to given path
        """
        if data:
            data_string = json.dumps(data)
        else:
            data_string = None

        headers = {'Accept': 'application/json'}
        connection.request(method, path, data_string, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            self.logger.error('Code %s while doing a %s request to %s: %s',
                              response.status,
                              method,
                              path,
                              response.read())
            return None

        try:
            response_data = response.read()
            response_data_decoded = response_data.decode('utf-8')
            response_dict = json.loads(response_data_decoded)
            return response_dict
        except json.JSONDecodeError as jde:
            self.logger.error('Error parsing %s response to %s: %s',
                              method,
                              path,
                              jde)
            return None


    def get_count(self):
        """
        Get number of documents in the database
        """
        connection = self.__get_database_connection()
        response = self.__make_request(connection, '/%s' % (self.database_name))
        return response.get('doc_count', 0)


    def get(self, document_id):
        """
        Get a single document with given identifier
        """
        document_id = document_id.strip()
        if not document_id:
            return None

        connection = self.__get_database_connection()
        response = self.__make_request(connection, '/%s/%s' % (self.database_name, document_id))
        return response

    def document_exists(self, document_id):
        """
        Do a HEAD request to check whether document exists
        """
        document_id = document_id.strip()
        if not document_id:
            return False

        connection = self.__get_database_connection()
        response = self.__make_request(connection,
                                       '/%s/%s' % (self.database_name, document_id),
                                       method='HEAD')
        return bool(response)

    def delete_document(self, document):
        """
        Delete a document
        """
        document_id = document.get('_id', '')
        document_id = document_id.strip()
        if not document_id:
            return

        document_rev = document.get('_rev', '')
        document_rev = document_rev.strip()
        if not document_rev:
            return

        connection = self.__get_database_connection()
        self.__make_request(connection,
                            '/%s/%s?rev=%s' % (self.database_name, document_id, document_rev),
                            method='DELETE')

    def save(self, document):
        """
        Save a document
        """
        document_id = document.get('_id', '')
        if not document_id:
            return

        connection = self.__get_database_connection()
        self.__make_request(connection,
                            '/%s/%s' % (self.database_name, document_id),
                            method='PUT',
                            data=document)

    def query(self, query_dict, page=0, page_size=20):
        """
        Perform a query in a database
        """
        pass

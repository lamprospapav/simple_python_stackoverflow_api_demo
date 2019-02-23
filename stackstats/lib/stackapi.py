from datetime import datetime
import time
import requests
from dateutil.parser import parse
import json
from itertools import chain


class stacks(object):
    def __init__(self, name=None, version="2.2", **kwargs):
        """The object used to interact with the Stack Exchange API
        
        :Args:
            :param name:        (string) **(Required)** A valid ``api_site_parameter``
                                (available from http://api.stackexchange.com/docs/sites) which will
                                be used to connect to a particular site on the Stack Exchange
                                Network.
            
            :param version:     (float) **(Required)** The version of the API you are connecting to.
                                The default of ``2.2`` is the current version
        :Kwargs:
            :param pagesize:    (int) (optional) The number of elements per page. The API limits this to
                                a maximum of 100 items on all end points except ``site``
            
            :param filter:      (str) (optional) There are a lot of filters provide by the Api.
                                The default that it used here is 'default'
            
            :param page:        (int) (optional) Nearly all methods in the API accept the page and pagesize
                                parameters for fetching specific pages of results from the API.
                                The default  page starts at and defaults to 1

        This version support only kwargs = [pagesize,filter,page] any other input it will cause ValuError
        """

        if not name:
            raise ValueError('No Site name provided')
        else:
            self._site = name
        # Valid kwargs
        kwargs_keys = ['page', 'pagesize', 'filter','maxpages']
        for k in kwargs.keys():
            if k not in kwargs_keys:
                raise ValueError('Not a valid kwarg')

        self._body_url = 'https://api.stackexchange.com/{}/'.format(version)
        self._version = version
        self._pagesize = kwargs.get('pagesize', 100)
        self._filter = kwargs.get('filter', 'default')
        self._page = kwargs.get('page', 1)

    def fetch_data(self, pre_site_method_url, params):
        """Returns the results of an API call.

        It builds the API query string and sends the request to Stack Exchange. If there are multiple
        pages of results, it use "has_more" to paginate the received data. If you want to use it you must
        first use an implementation pre_site_method. In this version supported:
                - /answers
                - /answers/{ids}

        Returned json data stored in a single dictionary.

        :param pre_site_method_url: (string) This is a part of url API that is created from
                                    an implentation pre_site_method into this class. You can create it 
                                    if you use Per-Site Method as it descripted in http://api.stackexchange.com/docs


        :param params: (Dictionary). It has paramas that it used at the and of pre_site_method url

        """

        # Create the main body of Api url with the pre_site_method part
        url = "{}{}".format(self._body_url, pre_site_method_url)

        data = []
        while True:
            # Request to api with the url that created and params
            response = requests.get(url, params=params)
            response.encoding = 'utf-8-sig'
            response = response.json()
            data.append(response)
            # If 'has_more' at the end of the response
            # param page increase by 1 and a new request is created
            if 'has_more' in response and response['has_more']:
                params["page"] += 1
            else:
                break
        if 'error_id' in response.keys():
            raise ValueError('Api blocks me to get data.Api return error_name: throttle_violation')

        r = []
        for d in data:
            r.extend(d['items'])

        return list(chain(r))

    def stacks_answer(self, **kwargs):
        """Implementation pre_site_method:answers https://api.stackexchange.com/docs/answers
            Returns all the undeleted answers in the system.
            The sorts accepted by this method operate on the following fields of the answer object:

                - activity  last_activity_date
                - creation  creation_date
                - votes  score

        Returned pre_method_url and params that it can be used for this pre_method.

        :Kwargs:
            :param pagesize:    (int) (optional) The number of elements per page. The API limits this to
                                a maximum of 100 items on all end points except ``site``
            
            :param page:        (int) (optional) Nearly all methods in the API accept the page and pagesize
                                parameters for fetching specific pages of results from the API.
                                The default  page starts at and defaults to 1
            
            :param fromdate:    (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                The fromdate that api will provide results. 
            
            :param todate:      (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                The todate that api will provide results.
            
            :param min:         (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                Min specify the range of a field must fall in (that field being specified by sort) 
                                to be returned        
            
            :param max:         (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                Max specify the range of a field must fall in (that field being specified by sort) 
                                to be returned    
            
            :param sort:        (str) (optional) The sorts accepted by this method
                                The default value is 'activity'
            
            "param order:       (str) (optional) The order accepted by this method
                                The default value is 'desc'             
            """
        # Kwargs accepted keys
        kwargs_keys = ['page', 'pagesize', 'fromdate',
                       'todate', 'order', 'min', 'max', 'sort']
        for k in kwargs.keys():
            if k not in kwargs_keys:
                raise ValueError('Not a valid kwarg')
        page = kwargs.get('page', self._page)
        page_size = kwargs.get('page_size', self._pagesize)
        self._order = kwargs.get('asc', 'desc')

        if self._order not in ['asc', 'desc']:
            raise ValueError(
                "Given sort ({0}) not valid! Expected sort 'activity','creation','votes'".format(self._order))
        self._sort = kwargs.get('sort', 'activity')

        if self._sort not in ['activity', 'creation', 'votes']:
            raise ValueError(
                "Given sort ({0}) not valid! Expected sort 'activity','creation','votes'".format(self._sort))
        # Datetime must be convert to unix epoch time
        date_time_keys = ['fromdate', 'todate', 'since', 'until', 'min', 'max']
        for k in date_time_keys:
            if k in kwargs:
                if isinstance(kwargs[k], datetime):
                    kwargs[k] = int(time.mktime(kwargs[k].utctimetuple()))
                if kwargs[k] is None:
                    kwargs.pop(k, None)

        # pre_site_method url
        pre_site_method_url = 'answers'
        # Params
        params = {
            "page": page,
            "page_size": page_size,
            "filter": self._filter,
            "order": self._order,
            "site": self._site,
        }

        params.update(kwargs)
        return params, pre_site_method_url

    def stacks_comments_on_answers(self, **kwargs):
        """Implementation pre_site_method: /answers/{ids}/comments. https://api.stackexchange.com/docs/comments-on-answers

            If you know that you have an answer id and need the comments, use this method.
            Gets the comments on a set of answers.
            The sorts accepted by this method operate on the following fields of the answer object:

            - creation  creation_date
            - votes  score

        Returned pre_method_url and params that it can be used for this pre_method.

        :Kwargs:
            :param ids:             (list) **(Required)**Python list with the answer ids that you need the comments.   

            :param pagesize:        (int) (optional) The number of elements per page. The API limits this to
                                    a maximum of 100 items on all end points except ``site``

            :param page:            (int) (optional) Nearly all methods in the API accept the page and pagesize
                                    parameters for fetching specific pages of results from the API.
                                    The default  page starts at and defaults to 1

            :param fromdate:        (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                    The fromdate that api will provide results. 

            :param todate:          (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                    The todate that api will provide results.
            
            :param fromdate:        (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                    The fromdate that api will provide results
            
            :param min:             (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                    Min specify the range of a field must fall in (that field being specified by sort) 
                                    to be returned        
            
            :param max:             (datetime) (optional) 'Datetime in format "YYYY-MM-DD" or "YYYY-MM-DD HH:mm"'
                                    Max specify the range of a field must fall in (that field being specified by sort) 
                                    to be returned    
            
            :param sort:            (str)(optional) The sorts accepted by this method
                                    The default value is 'activity'
            "param order:           (str) (optional) The order accepted by this method
                                    The default value is 'desc'

            """

        kwargs_keys = ['page', 'pagesize', 'fromdate',
                       'todate', 'order', 'min', 'max', 'sort', 'ids']
        for k in kwargs.keys():
            if k not in kwargs_keys:
                raise ValueError('Not a valid kwarg')
        page = kwargs.get('page', self._page)
        page_size = kwargs.get('page_size', self._pagesize)
        self._order = kwargs.get('asc', 'desc')
        if self._order not in ['asc', 'desc']:
            raise ValueError(
                "Given sort ({0}) not valid! Expected sort 'activity','creation','votes'".format(self._order))
        self._sort = kwargs.get('sort', 'creation')
        if self._sort not in ['creation', 'votes']:
            raise ValueError(
                "Given sort ({0}) not valid! Expected sort 'activity','creation','votes'".format(self._sort))

        date_time_keys = ['fromdate', 'todate', 'since', 'until', 'min', 'max']
        for k in date_time_keys:
            if k in kwargs:
                if isinstance(kwargs[k], datetime):
                    kwargs[k] = int(time.mktime(kwargs[k].utctimetuple()))
                if kwargs[k] is None:
                    kwargs.pop(k, None)

        if 'ids' in kwargs:
            ids = ';'.join(str(x) for x in kwargs['ids'])
            kwargs.pop('ids', None)
            pre_site_method_url = "answers/{}/comments".format(ids)

        params = {
            "page": page,
            "page_size": page_size,
            "filter": self._filter,
            "order": self._order,
            "site": self._site,
        }

        params.update(kwargs)
        return params, pre_site_method_url

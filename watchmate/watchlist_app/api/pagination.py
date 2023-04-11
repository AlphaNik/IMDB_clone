from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination,
                                       CursorPagination)


class ShowPNPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'p'
    page_size_query_param ='size'   #below is  client side customisation 
    max_page_size = 10 #restrication to client(if he sends size as 100,#it will show only as per this attribute)
    last_page_strings = 'end'  #by default it is 'last'


class ShowLOPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 5
    limit_query_param = 'limit'  #default is 'limit'
    offset_query_param = 'start'  #default is 'offset'


class ShowCPagination(CursorPagination):
    page_size = 2
    ordering = 'created'  #by default it is '-created' (new to old data)
    cursor_query_param = 'record'  #default is 'cursor'
    

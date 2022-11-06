
import aiohttp
import asyncio
import time

start_time = time.time()


class AsyncRequest:

        
        """
                Simple async class that request books by isbn13


        """

        def __init__(self,endpoint: str,params: dict | None = None,headers: dict | None=None):
                                
                self.endpoint = endpoint
                self.params = params
                self.headers = headers
                self.books = []


        def set_isbn(self,isbn):
                """ Set isbn list"""
                self.isbn = isbn if type(isbn) is list else [isbn]
                
        async def run_request(self):
                ''' Add task to asyncio '''
                async with aiohttp.ClientSession()  as session:
                        tasks = []                        
                        for i in self.isbn:
                                tasks.append(asyncio.ensure_future(self.get_book(session,i)))                                
                        self.books = await asyncio.gather(*tasks)
        
        async def get_book(self,session,i):
                '''  Request a book by isbn13. '''
                _params = AsyncRequest.format_params(self.params,i)
                async with session.get(self.endpoint,params=_params,headers=self.headers) as response:
                        book = await response.json()                        
                        return book

        @staticmethod                
        def format_params(params,isbn):
                ''' Add isbn # to url param'''
                params['bibkeys'] = f'ISBN:{isbn}'
                return params

        def get_books(self):
                '''run async task'''
                asyncio.run(self.run_request())
                return self.books


# isbn = ['9781603095020','9781603094542','9781603094924','9781603095136']


params = {"bibkeys":"","jscmd":"data","format":"json"}
endpoint = 'https://openlibrary.org/api/books'

search_provider = AsyncRequest(endpoint,params)




# print("--- %s seconds ---" % (time.time() - start_time))
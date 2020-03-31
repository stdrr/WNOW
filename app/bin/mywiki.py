# =============================================================================
# This class is a Facade of the modules mwclient and wikipedia
# =============================================================================

from mwclient import Site
import wikipedia as wk
import pandas as pd
from bin.errors import APIError, PageNotExists

class Wiki:
    def __init__(self, host='en.wikipedia.org', user_agent='Wnow?/1.0 (wnow@gmail.com)'):
        self.site = Site(host, clients_useragent=user_agent)
        
    def get_id(self, title):
        return wk.page(title=title).pageid
    
    def get_title(self, pageid):
        return wk.page(pageid=pageid).title
    
    # This method returns the summary provided by wk.summary()
    # **kwargs could be either the title of the page or its pageid
    def get_summary(self, **kwargs) -> str:
        try:
            if 'title' in kwargs:
                return wk.summary(title=kwargs['title'])
            if 'pageid' in kwargs:
                return wk.page(pageid=kwargs['pageid']).summary
        except:
            print('\tSummary not available')
            raise APIError
    
    # This method returns the content provided by wk.page[].content
    # **kwargs could be either the title of the page or its pageid
    def get_content(self, **kwargs) -> str:
        try:    
            if 'title' in kwargs:
                return wk.page(title=kwargs['title']).content
            if 'pageid' in kwargs:
                return wk.page(pageid=kwargs['pageid']).content
        except:
            print('\tContent not available')
            return 'Content not available'
    
    # This method returns the object mwclient.page.Page
    # **kwargs could be either the title of the page or its pageid
    def get_page(self, **kwargs):
        try:
            if 'title' in kwargs:
                return self.site.pages[kwargs['title']]
            if 'pageid' in kwargs:
                return self.site.pages[kwargs['pageid']]
        except:
            raise APIError
        
    # This method builds the url to the page given its title
    def get_page_link(self, title) -> str:
        return 'en.wikipedia.org/wiki/' + title.replace(' ', '%20')
        
    # This method gets the recent changes list using mwclient.Site.api()
    # It filters pages in namespace 0 and gets only pages created or modified
    def __recentchanges_list(self, limit, start, end) -> pd.DataFrame:
        try:
            rc = self.site.api('query', list='recentchanges', rclimit=limit, rcstart=start, rcend=end, rctype='new|edit', rcnamespace='0')
        except:
            raise APIError
        r = pd.DataFrame(data=rc['query']['recentchanges'])
        r.drop(columns=['ns', 'revid', 'old_revid', 'rcid', 'timestamp'], inplace=True)
        return r
    
    # This method gets the recent changes by calling __recentchanges_list(..)
    # Attribute rclimit is required to set up the maximum number of recent changes you can get; to set up the maximum value permitted by MediaWiki'API, type 'max'
    # Attributes rcstart and rcend are required to set up the time range in which getting recent changes; rcstart must be grater than rcend 
    def recentchanges(self, rclimit, rcstart, rcend) -> pd.DataFrame:
        images = []
        summaries = []
        links = []
        try:
            result = self.__recentchanges_list(limit=rclimit, start=rcstart, end=rcend)
        except:
            print('\tAn API error occured during recent changes retrieving')
            raise APIError
        for pageid in result['pageid']:
            try:
                page = self.get_page(pageid=pageid) # get the page from the pageid provided
                if not page.exists:
                    raise PageNotExists
            except APIError:
                print('\tAn API error occured during single page retrieving')
                result.query('pageid != ' + str(pageid), inplace=True) # if an API error occures, remove the pageid of the page that caused the error from the recent changes list 
                continue
            except PageNotExists:
                result.query('pageid != ' + str(pageid), inplace=True) # if a PageNotExists error occures, remove the pageid of the page that caused the error from the recent changes list 
                continue
            try:
                summary = self.get_summary(pageid=pageid) # get the summary of the page given the pageid
                if not summary: # if summary is empty (there's no summary), raise error
                    raise PageNotExists
                summaries.append(summary) # insert summary into the list summaries
            except:
                result.query('pageid != ' + str(pageid), inplace=True) # if a PageNotExists error occures, remove the pageid of the page that caused the error from the recent changes list 
                continue
            try:
                images.append(page.images(generator=True).next().imageinfo['url']) # get the first url image from the page calling mwclient.page.Page.images()
            except:
                images.append('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Wikipedia_logo_v3.svg/1024px-Wikipedia_logo_v3.svg.png') # append a default image (Wikipedia logo)
            try:
                links.append(self.get_page_link(page.name)) # build the page link
            except:
                links.append('en.wikipedia.org/wiki/Main_Page') # if an error occures, append a default link
        result.insert(3, column='image', value=images)
        result.insert(4, column='link', value=links)
        result.insert(5, column='summary', value=summaries)
        return result

    # This method returns a dictionary containing pages from the category provided
    # According to MediaWiki API's syntax, category must be like 'Category:mycategory'
    # Attribute pages_num specifies the number of pages that at most will be returned
    def get_raw_category_pages(self, category, pages_num):
        search_list = [category] # make the list which will contain all the subcategories found recursively in category
        page_set = []
        with tqdm(total=pages_num, desc=category) as cbar: # display progress bar
            while search_list and len(page_set) <= pages_num: # while search_list is not empty and the number of pages is less than required
                query_result = self.site.api('query', list='categorymembers', cmtitle=search_list.pop(0), cmprop='title', cmtype='page|subcat', cmsort='timestamp', cmlimit='max')
                for element in query_result['query']['categorymembers']: # for each page/category in the query's result
                    if len(page_set) >= pages_num: # the number of pages is greater than required
                        break
                    elif 'Category:' in element['title']: # element is a category
                        search_list.append(element['title']) # push the category found into the categories list
                    else: # element is a page
                        try:
                            summary = wk.summary(element['title'], sentences=3) # request page's summary
                            if summary: # if summary is not empty
                                page_set.append(summary) # append summary
                                cbar.update(1) # increment progress bar
                        except:
                            continue # if an error occures while querying the API for summary, skip the error
        category = category.replace('Category:', '') # get rid of Category: prefix in attribute category provided
        return {'text':page_set, 'category':category} # return dictonary made up of all pages' summaries and the category label
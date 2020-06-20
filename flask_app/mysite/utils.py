class PageContentMapper:

    """ Holds variables to fill html templates with"""

    def __init__(self):
        self.content_map = {'public/home.html': {'page_header': 'Hello, welcome to my home page'},
                            'public/blog.html': {'page_header': 'Thoughts and Musings'}}

    def load_page_content(self, page_ref):
        return self.content_map[page_ref]

    def add_page_content(self, page_ref, page_var, content):
        """ Add content to a page in the content map, replacing the page template variable value if it
            already exists
        """
        if page_ref in self.content_map:
            self.content_map[page_ref][page_var] = content
        else:
            self.content_map[page_ref] = {page_var: content}

class PageContentMapper:

    def __init__(self):
        self.content_map = {'public/home.html': {'page_header': 'Hello, welcome to my home page'}}

    def load_page_content(self, page_ref):
        return self.content_map[page_ref]

    def add_page_content(self, page_ref, page_var, content):
        if page_ref in self.content_map:
            self.content_map[page_ref][page_var] = content
        else:
            self.content_map[page_ref] = {page_var: content}
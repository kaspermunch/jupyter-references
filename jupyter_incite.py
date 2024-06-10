# def year_cite():
#     match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)',
#         clipboard.osx_clipboard_get(), re.DOTALL)
#     if match:
#         url, year, title, author = match.groups()
#         return f'{author} [({year})]({url} "{title}")'
#     return ''
# if __name__ == "__main__":
#     link_text = year_cite()
#     get_ipython().run_line_magic('load', '-n link_text')
    
import re
from IPython.lib import clipboard
cb = clipboard.osx_clipboard_get()
bibtex_entries = re.findall(r'\@[^\@]+', cb)
if len(bibtex_entries) > 1:
    print('clipboard has bibtex entries:', cb)
else:
    match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)',
        cb, re.DOTALL)
    if match:
        ref_list = {}
        url, year, title, author = match.groups()
        link_text = f'{author} et al. [({year})](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")'
        get_ipython().run_line_magic('load', '-n link_text')    
        # get_ipython().run_cell_magic('markdown', '', link_text)    
    else:
        print('clipboard is not bibtex:', cb)


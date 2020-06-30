import re

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class IssuePipeline:
    ISSUE_FROM_FILE = re.compile(r'\d{4}[-_](\d{2}).*\.(pdf|djvu)')
    ISSUE_FROM_TEXT = re.compile(r'\D?(\d+)(\D?\d?)')
    YEAR = re.compile(r'.*([1-2][0-9]{3})')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        match = re.match(self.YEAR, adapter['file'])
        if match is not None:
            adapter['year'] = match.group(1)

        if 'text' in adapter:
            match = re.search(self.ISSUE_FROM_TEXT, adapter['text'])
            if match is not None:
                adapter['issue'] = match.group(1)

                optional = match.group(2)
                if len(optional) > 1:
                    adapter['issue'] += optional
            del adapter['text']
        else:
            match = re.search(self.ISSUE_FROM_FILE, adapter['file'])
            if match is not None:
                issue = match.group(1).lstrip('0')
                if int(issue) > 12:
                    issue = issue[:1] + '–' + issue[1:]

                adapter['issue'] = issue

        return item


class DropSamplesPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        if adapter['file'].endswith('_sample.pdf'):
            raise DropItem()

        return item

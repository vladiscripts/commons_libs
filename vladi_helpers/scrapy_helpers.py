import scrapy.exceptions.DropItem
import re


class DuplicatesPipeline(object):
    def __init__(self):
        self.uniques = set()

    def process_item(self, item, spider):
        if item['lot'] in self.uniques:
            raise DropItem("Duplicate item found, 'lot': %s" % item['lot'])
        else:
            self.uniques.add(item['lot'])
            return item


class StripTagsPipeline(object):
    re_striptags = re.compile(r'^<[^>]*>(.*?)</[^>]*>$', flags=re.DOTALL)

    def process_item(self, item, spider):
        for k, v in item.items():
            if v and isinstance(v, str):
                v = self.re_striptags.sub(r'\1', v)
                # v = v.strip('-').strip()
                item[k] = v
        return item

    # for k, v in i.items():
    #     if v:
    #         v = re.sub('^<.*?>(.*?)</.*?>$', r'\1', v, flags=re.DOTALL)
    #         v = v.strip('-').strip()
    #         i[k] = v

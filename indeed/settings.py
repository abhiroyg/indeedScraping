# Scrapy settings for indeed project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'indeed (+http://www.yourdomain.com)'

LOG_FILE = './scrapy_indeed.log'
LOG_STDOUT = True
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s %(filename)s %(funcName)s %(levelname)s %(lineno)d %(message)s %(name)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S%z'

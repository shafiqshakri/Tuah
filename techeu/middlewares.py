from random import choice
from scrapy import signals
from scrapy.exceptions import NotConfigured
import re
import random
import base64
import logging

class Mode:
    RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)

class RotateUserAgentMiddleware(object):
    """Rotate user-agent for each request."""
    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])

        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        o = cls(user_agents)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)

        return o

    def spider_opened(self, spider):
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        if not self.enabled or not self.user_agents:
            return
        request.headers['user-agent'] = choice(self.user_agents)

"""class ProxyMiddleware(object):
    def process_request(self, request,spider):
        # Set the location of the proxy
        self.proxy_list = ['http://153.149.158.154:3128',
                        'http://170.248.46.39:8888',
                        'http://179.187.33.195:8080',
                        'http://179.191.196.65:3128',
                        'http://194.226.167.142:3128',
                        'http://194.226.167.143:3128',
                        'http://36.73.167.120:3128',
                        'http://36.85.185.84:80',
                        'http://37.187.55.124:3128',
                        'http://37.235.53.118:8080',
                        'http://5.44.217.124:80',
                        'http://61.5.207.102:80',
                        'http://78.111.246.138:8080',
                        'http://80.84.116.234:3128',
                        'http://95.211.198.252:80',
                        'http://95.213.194.94:3128'
                        ]
        for list in self.proxy_list:

            request.meta['proxy'] = list

            # Use the following lines if your proxy requires authentication
            proxy_user_pass = "USERNAME:PASSWORD"
            # setup basic authentication for the proxy
            encoded_user_pass = base64.b64encode(proxy_user_pass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass"""

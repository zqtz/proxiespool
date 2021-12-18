class ResourceDepletionError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy source is Exhausted')

class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('the proxy pool is empty')

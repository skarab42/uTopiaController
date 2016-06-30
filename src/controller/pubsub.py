# coding: utf-8
class pubsub(object):
    _topics = {}

    @classmethod
    def publish(cls, topic, **kwargs):
        for callback in cls._topics.get(topic, []):
            callback(**kwargs)

    @classmethod
    def subscribe(cls, topic, callback):
        cls._topics.setdefault(topic, [])
        cls._topics[topic].append(callback)

from pipeline.storage import PipelineMixin
from storages.backends.s3 import S3Storage


class StaticStorage(PipelineMixin, S3Storage):
    pass

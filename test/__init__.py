import vcr

# In order to customize VCR, please refer to:
# https://vcrpy.readthedocs.io/en/latest/configuration.html

VCR = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='fixtures/cassettes',
    filter_headers=[('authorization', 'token FOOBAR')]
)

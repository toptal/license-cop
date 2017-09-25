

class PackageDescriptorResolution:
    def __init__(self, descriptor, runtime_resolutions, development_resolutions):
        self.descriptor = descriptor
        self.runtime_resolutions = runtime_resolutions
        self.development_resolutions = development_resolutions

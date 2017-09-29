from io import StringIO


class PackageDescriptorResolution:

    def __init__(self, descriptor, runtime_resolutions, development_resolutions):
        self.descriptor = descriptor
        self.runtime_resolutions = runtime_resolutions
        self.development_resolutions = development_resolutions

    def __repr__(self):
        io = StringIO()
        print('+ {0}'.format(self.descriptor), file=io)
        self.__print_resolutions(io, self.runtime_resolutions)
        self.__print_resolutions(io, self.development_resolutions)
        return io.getvalue()

    def __print_resolutions(self, io, resolutions):
        for resolution in resolutions:
            io.write(resolution.__repr__(1))

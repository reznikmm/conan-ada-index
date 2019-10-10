import os

from conans import ConanFile, CMake, tools


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "txt"

    def build(self):
        self.run("cp ../../main.* .")
        self.run("gprbuild -P main.gpr")

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(".%smain" % os.sep)

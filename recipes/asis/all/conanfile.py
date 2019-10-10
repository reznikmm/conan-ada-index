from conans import ConanFile, tools
from conans.tools import download, untargz, check_sha1
import os
import shutil


class AsisConan(ConanFile):
    name = "ASIS"
    version = "2019"
    license = "GPL-3"
    author = "AdaCore <report@adacore.com>"
    url = "https://www.adacore.com/asis"
    description = """ASIS is a library that gives applications access to
the complete syntactic and semantic structure of an Ada compilation unit.
This library is typically used by tools that need to perform some sort of
static analysis on an Ada program."""

    topics = ("Ada", "syntax", "semantic", "analysis")
    settings = {
        "os": None,         # None => any
        "compiler": None,   # None => any
        "gnat": "2019",
        "build_type": ["Debug", "Release"],
        "arch": None        # None => any
    }
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "txt"
    _source_base_name = "asis-2019-20190517-18AB5-src"

    def source(self):
        zip_name = self._source_base_name + ".tar.gz"
        url = "https://community.download.adacore.com/v1/52c69e7295dc301ce670334f8150193ecbec580d"
        download(url + "?filename=" + zip_name, zip_name)
        check_sha1(zip_name, "52c69e7295dc301ce670334f8150193ecbec580d")
        untargz(zip_name)

    def build(self):
        self.run('make setup-snames', cwd=self._source_base_name)
        args = "-XBLD=%s " % ("debug" if self.settings.build_type == "Debug" else "prod")
        args = args + "-XASIS_COMPONENTS=lib -XPROCESSORS=0"
        self.run('echo gprbuild -Pasis %s' % args, cwd=self._source_base_name)
        self.run('gprbuild -Pasis %s' % args, cwd=self._source_base_name)

    def package(self):
        self.run('gprinstall -p --prefix=prefix -Pasis -XASIS_COMPONENTS=lib', cwd=self._source_base_name)
        self.copy("*.ads", src=self._source_base_name + "/prefix")
        self.copy("*.adb", src=self._source_base_name + "/prefix")
        self.copy("*.ali", src=self._source_base_name + "/prefix")
        self.copy("*.a", src=self._source_base_name + "/prefix")
        self.copy("*.gpr", src=self._source_base_name + "/prefix")

    def package_info(self):
        self.env_info.GPR_PROJECT_PATH.append(os.path.join(self.package_folder, "share", "gpr"))

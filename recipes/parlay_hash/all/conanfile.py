from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.51.3"

class PackageConan(ConanFile):
    name = "parlay_hash"
    description = "A Header-Only Scalable Concurrent Hash Map."
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/cmuparlay/parlayhash"
    topics = ("unordered_map", "hashmap", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _minimum_cpp_standard(self):
        return 17

    @property
    def _compilers_minimum_version(self):
        return {
            "Visual Studio": "15.7",
            "msvc": "191",
            "gcc": "7",
            "clang": "7",
            "apple-clang": "11",
        }

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, self._minimum_cpp_standard)
        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and Version(self.settings.get_safe("compiler.version")) < minimum_version:
            raise ConanInvalidConfiguration(f"{self.ref} requires C++{self._minimum_cpp_standard}, which your compiler does not support.")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        pass

    def package(self):
        copy(self, pattern="LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, pattern="*.h", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")

        self.cpp_info.set_property("cmake_file_name", "parlay_hash")
        self.cpp_info.set_property("cmake_target_name", "parlay_hash::parlay_hash")

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.filenames["cmake_find_package"] = "parlay_hash"
        self.cpp_info.filenames["cmake_find_package_multi"] = "parlay_hash"
        self.cpp_info.names["cmake_find_package"] = "parlay_hash"
        self.cpp_info.names["cmake_find_package_multi"] = "parlay_hash"

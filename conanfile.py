import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import get, collect_libs, patch


class OpenIGTLinkRecipe(ConanFile):
    name = "openigtlink"
    version = "3.0.0" 
    license = "BSD"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = "*.patch"

    def source(self):
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is a bad practice and not allowed by Conan
        get(self, "https://github.com/openigtlink/OpenIGTLink/archive/refs/tags/v3.0.zip",
                  strip_root=True)
                
        patch_file = os.path.join(self.export_sources_folder, "conan-openigtlink.patch")
        patch(self, patch_file=patch_file)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTING"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ["lib","lib/igtl"]
        self.cpp_info.libs = collect_libs(self)
        print("Libraries: {}".format(self.cpp_info.libs))
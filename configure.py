import os
import sipconfig
import glob

# The name of the SIP build file generated by SIP and used by the build
# system.
build_file = "SkCanvas.sbf"

# Get the SIP configuration information.
config = sipconfig.Configuration()
config.qt_framework = False

# Get the extra SIP flags needed by the imported PyQt modules.  Note that
# this normally only includes those flags (-x and -t) that relate to SIP's
# versioning system.
# pyqt_sip_flags = config.pyqt_sip_flags

# Run SIP to generate the code.  Note that we tell SIP where to find the qt
# module's specification files using the -I flag.
os.system(
    " ".join([
        config.sip_bin, "-c", ".", "-b",
        build_file,
        "SkCanvas.sip"
    ])
)

# We are going to install the SIP specification file for this module and
# its configuration module.
installs = []
installs.append(["SkCanvas.sip", os.path.join(config.default_sip_dir, "SkCanvas")])
installs.append(["skia_config.py", config.default_mod_dir])
# installs.extend(
#     f for f in glob.iglob(os.path.join("..", "skia", "out", "Release")))

# Create the Makefile.
makefile = sipconfig.SIPModuleMakefile(config, build_file, installs=installs)

# Add the library we are wrapping.  The name doesn't include any platform
# specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
# ".dll" extension on Windows).
makefile.extra_lib_dirs = [
    os.path.join("..", "skia", "out", "Release"),
]
makefile.extra_include_dirs = [
    os.path.join("..", "skia", "include", "core"),
    os.path.join("..", "skia", "include", "config"),
]
makefile.extra_libs = ["skia_core", "skia_gr"]

# Generate the Makefile itself.
makefile.generate()

# Now we create the configuration module.  This is done by merging a Python
# dictionary (whose values are normally determined dynamically) with a
# (static) template.
content = {
    # Publish where the SIP specifications for this module will be
    # installed.
    "SkCanvas_sip_dir": config.default_sip_dir,

    # Publish the set of SIP flags needed by this module.  As these are the
    # same flags needed by the qt module we could leave it out, but this
    # allows us to change the flags at a later date without breaking
    # scripts that import the configuration module.
#     "hello_sip_flags":  pyqt_sip_flags
}

# This creates the helloconfig.py module from the helloconfig.py.in
# template and the dictionary.
sipconfig.create_config_module("skia_config.py", "skia_config.py.in", content)
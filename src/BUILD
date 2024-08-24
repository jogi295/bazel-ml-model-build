load("@rules_python//python:defs.bzl", "py_binary")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "ml_app",
    srcs = ["app.py"],
    main = "app.py",  # Explicitly specify the main file
    data = [
        "//src/models:model_files",
        "//src/templates:template_files",
    ],
    deps = [
        requirement("flask"),
        requirement("numpy"),
        requirement("scikit-learn"),
    ],
)
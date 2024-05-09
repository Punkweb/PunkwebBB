from setuptools import setup

setup(
    name="punkweb_bb",
    version="0.1.3",
    author="Punkweb",
    author_email="punkwebnet@gmail.com",
    packages=["punkweb_bb"],
    url="https://github.com/Punkweb/PunkwebBB",
    license="BSD-3-Clause",
    description="Django application that provides a simple and modern forum board software for your Django website.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    package_data={"": ["README.md"]},
    install_requires=[
        "django>=4.0",
        "django-precise-bbcode",
        "pillow",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)

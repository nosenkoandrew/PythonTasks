from setuptools import setup

setup(
    name = "task4",
    version = "0.1",
    install_requires = ['Click',],
    py_modyles = ['task4'],
    entry_points = '''
    [console_scripts]
    non_repeating = task4:non_repeating_elems
    '''
)
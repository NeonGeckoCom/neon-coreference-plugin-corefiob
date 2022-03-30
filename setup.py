#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'neon-coreference-plugin-corefiob=neon_coref_plugin_corefiob:CorefIOBSolver'
setup(
    name='neon-coreference-plugin-neon_coref_plugin_corefiob',
    version='0.0.1',
    description='A coreference resolution plugin for mycroft',
    url='https://github.com/NeonGeckoCom/neon-coreference-plugin-corefiob',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['neon_coref_plugin_corefiob'],
    install_requires=["ovos-plugin-manager"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={'intentbox.coreference': PLUGIN_ENTRY_POINT}
)

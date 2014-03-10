__author__ = 'eatmuchpie'

from distutils.core import setup

setup(name='Distutils',
      version='1.0',
      description='OpenGL Playground',
      author='Sam Wright',
      url='samwright.github.io',
      packages=['opengl_playground'],
      requires=['pyglet', 'numpy', 'nose']
)

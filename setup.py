from setuptools import setup

setup(
    name='lektor-netlify',
    version='0.1',
    author=u'A. Jesse Jiryu Davis',
    author_email='jesse@emptysquare.net',
    description='Publish to Netlify your site built with the Lektor static site generator.',
    license='MIT',
    py_modules=['lektor_netlify'],
    url='https://github.com/ajdavis/lektor-netlify',
    entry_points={
        'lektor.plugins': [
            'netlify = lektor_netlify:NetlifyPlugin',
        ]
    }
)

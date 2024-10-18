from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name="alerta-webhook",
    version=version,
    description='Alerta webhook plugin',
    url='https://github.com/alerta/alerta-contrib',
    license='Apache License 2.0',
    author='Rudder labs',
    author_email='',
    packages=find_packages(),
    py_modules=['alerta_webhook'],
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'webhook = alerta_webhook:AlertaWebhookPlugin'
        ]
    }
)

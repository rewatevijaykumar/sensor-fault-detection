from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    requirement_list:list[str] = []

    with open('requirements.txt','r') as f:
        requirement_list.append(f.readline())
        
    return requirement_list

setup(
    name='sensor',
    version='0.0.1',
    author='Vijaykumar Rewate',
    author_email='rewatevijaykumar@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)
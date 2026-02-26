from bs4 import BeautifulSoup
import json
import sys

with open('results.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

properties = []
# Assuming properties are in some specific class or tag, let's first check what tags are used
# I'll extract headers or div classes that might represent a property.
# Wait, I need to know the HTML structure.
# Let's write a script to just get a few sample elements.
sample = soup.find('body').text[:1000]
print(sample)

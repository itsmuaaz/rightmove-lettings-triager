from reporter import Reporter

prop = {
    'image_url': 'http://example.com/img.jpg',
    'price': '£2,000 pcm',
    'commute_time': 25,
    'commute_cycling': 15,
    'distance': 1.5,
    'bedrooms': 2,
    'type': 'Flat',
    'address': 'Test St, London',
    'published_on': '2023-10-27T10:00:00Z',
    'url': '/prop/1'
}

reporter = Reporter()
md = reporter.generate_markdown([prop], for_html=False)
with open('test_report.md', 'w') as f:
    f.write(md)

md_html = reporter.generate_markdown([prop], for_html=True)
html = reporter.convert_to_html(md_html)
with open('test_report.html', 'w') as f:
    f.write(html)

print("Generated test_report.md and test_report.html")

from exporter import ScholarExporter

# Example from user id:
s = ScholarExporter.from_user('JicYPdAAAAAJ')  # Geoffrey Hinton user
s.export('index.html')

# Example from url:
s = ScholarExporter('https://scholar.google.co.uk/citations?user=JicYPdAAAAAJ&hl=en')  # Geoffrey Hinton url
s.export('index.html')

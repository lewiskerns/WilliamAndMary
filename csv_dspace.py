#!/usr/bin/env python

import cgi, csv, os, os.path, re, shutil
from optparse import OptionParser

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO




# Convert inputs into a standard XML string
def to_xml(key, qualifier, value):
        """Serialize this Dublin Core object to XML.
	   <dcvalue element=xxx qualifier=xxx>value</dcvalue>
        """

        output = ''
        indent = '  '	# used to indent the element lines

        attributes = 'element="%s"' % cgi.escape(key, quote=True)

        attributes += ' qualifier="%s"' % cgi.escape(qualifier, quote=True)

      	output += '''%s<dcvalue %s>%s</dcvalue>''' % (indent, attributes, cgi.escape(value, quote=True))

        return output

# Process the source file
# Create a sudirectory for each row in the table
# place the XML and a content file in each subdirectory to specify the metadata and files

def process_source(src, dest):

	print '''Processing Meta data file: %s''' % (src)
	print '''Output will be located in: %s''' % (dest)

	csv_file = src
	dir = dest

	# Create the root directory 
	# if not already there, remove it first to clear out old files
 	if os.path.exists(dir):
		shutil.rmtree(dir)
        os.mkdir(dir)

	# Open the source CSV file
	reader = csv.reader(open(csv_file, 'r'), dialect='excel')
	reader.next() # Skip the header row
	i = 0
	# Read each record in the CSV File
	for record in reader:

	    if len(record) >= 17:
		# Create output directory for this element
		# number the directories sequencially
		i += 1
	 	item_dir = os.path.join(dir, 'item_%03d' % i)
		os.mkdir(item_dir)

		# Create the XML FILE for this element
	    	xml_file_name = os.path.join(item_dir, 'dublin_core.xml')
		xml_file = open(xml_file_name, 'w')
		xml_file.write('<?xml version="1.0" encoding="UTF-8"?>')
		xml_file.write("<dublin_core>")

	        xml_file.write(to_xml("title", "none", record[0]))			# Title
	        xml_file.write(to_xml("contributor", "author", record[1]))		# Contributor
	        xml_file.write(to_xml("subject", "none", record[2]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[3]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[4]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[5]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[6]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[7]))			# Subject
	        xml_file.write(to_xml("subject", "none", record[8]))			# Subject
	        xml_file.write(to_xml("date", "issued", record[9]))			# Date.Issued
	        xml_file.write(to_xml("genre", "none", record[10]))			# genre
	        xml_file.write(to_xml("identifier", "collectionId", record[11]))	# Identifier.CollectionID
	        xml_file.write(to_xml("description", "none", record[12]))		# Description
	        xml_file.write(to_xml("description", "abstract", record[13]))	# Description.abstract
	        xml_file.write(to_xml("contributor", "committeeMember", record[14]))	# Contributor.committeemember


	        if record[15] != '':
			# Thesis data exists
			# Create a metadata XML file for this schema metadata_thesis.xml
			meta_file_name = os.path.join(item_dir, 'metadata_thesis.xml')
			meta_file = open(meta_file_name, 'w')
			meta_file.write('<?xml version="1.0" encoding="UTF-8"?>')
			meta_file.write('<dublin_core schema="thesis">')
		        meta_file.write(to_xml("degree","discipline", record[15]))			# degree. discipline
		        meta_file.write(to_xml("degree","level", record[16]))				# Degree.level
			meta_file.write(to_xml("degree","grantor", "College of William and Mary"))  	# degree.grantor default value
			meta_file.write("</dublin_core>")
		        meta_file.close()


		xml_file.write("</dublin_core>")
	        xml_file.close()

		# Create a Content File for this element with the file names
	    	content_file_name = os.path.join(item_dir, 'content')
		content_file = open(content_file_name, 'w')
		files = record[17].split(";")
		for s in files:
			s = s.strip()
			content_file.write("%s\tbundle:original\n" % (s))
			#copy this file to destination directory
			if os.path.exists(s):
				destfile = os.path.join(item_dir,s)
				shutil.copyfile(s,destfile)
	        content_file.close()

		print "Complete"



if __name__ == '__main__':

    # ./csv-dspace.py -s source.csv -c destdir
    # if the destination directory exists, it will be deleted

    parser = OptionParser()
    parser.add_option('-s', '--source', action='store', default=None,
                      dest='metadata_src', metavar='FILE',
                      help='Use FILE as metadata for each item')
    parser.add_option('-c', '--destination', action='store',
                      dest='xml_destination', metavar='DIR',
                      help='Output directory for XML and create contents files.')
    (options, args) = parser.parse_args()

    if options.metadata_src and options.xml_destination:
    	process_source(options.metadata_src, options.xml_destination)
    else:
      	print "Usage. ./csv-dspace.py -s source.csv -c ouput_directory"
	print "The CSV file and the content files should be located in the current directory"




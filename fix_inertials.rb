#!/usr/bin/ruby

# Such a dirty, dirty hack

require 'nokogiri'

xml = begin
        input_file = ARGV[1] ? open(ARGV[1]) : STDIN
        xml = Nokogiri::XML(input_file)
        input_file.close
        xml
      end


model = xml.at_xpath('//model')

xml.xpath('//link/inertial').each do |inertial|
  link = inertial.parent

  next if link[:name] =~ /_inertial_dummy$/
  
  STDERR.puts " >> #{link[:name]}"

  dummy = Nokogiri::XML::Element.new('link', xml.document)
  dummy[:name] = "#{link[:name]}_inertial_dummy"
  dummy << inertial
  if pose = link.at_xpath('pose')
    dummy << pose.dup
  end

  link << "<!-- fix_inertials: <inertial> tag moved to link #{dummy[:name]}-->"
  link.add_next_sibling(dummy)
end

STDOUT.puts xml.to_xml





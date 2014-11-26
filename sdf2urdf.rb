#!/usr/bin/ruby

require 'nokogiri'

include Nokogiri

## TODO: At the end, check if this is still needed
class Object
    def map(&block)
        block.call(self) unless nil?
    end
end

class Nokogiri::XML::Node
    def child_named(name)
        existing = children.find {|c| c.name == name }
        return existing if existing
        
        child = XML::Element.new(name, self.document)
        self << child
        return child
    end
end

def assert(cond, err_msg)
    throw Exception.new(err_msg) if not cond
end

def transform_pose(elm, options={})
    tokens = elm.text.split
    origin = element('origin')
    if not options[:compact_origin] or not tokens.all? {|x| x.to_f == 0 }
        origin['xyz'] = tokens[0,3].join(" ")
        origin['rpy'] = tokens[3,3].join(" ")
    end
    origin
end

class Transformer
  def initialize(input_model)
    @input_model = input_model
    @outdoc = XML::Document.new
  end

  def transform
    transform_sdf(@input_model)
  end

  private

  def transform_sdf(elm)
    assert(@input_model.name == "sdf", "model element is not <sdf>, but <#{@input_model.name}>")

    model = elm.children.find {|c| c.name == "model" }
    assert((not model.nil?), "<model> element not found")

    return transform_model(model)
  end
  
  def transform_model(elm)
      elm.children.each do |child|
          case child.name
          when "pose" then 
              origin = transform_pose(child)
              base_link.child_named("visual") << origin
              base_link.child_named("collision") << origin
          when "link"  then 
              robot.child_named('link') << transform_link(child).children
          when "joint" then
              robot.child_named('joint') << transform_joint(child).children
          when "plugin" then {}
          else robot << discard(child)
          end
      end
  end
  
  
  def transform_link(elm)
    link = XML::Element.new('link', @outdoc)
    link['name'] = elm['name']
    elm.children.each {|c|
      case c.name
      when "pose" then 
        origin = transform_pose(c)
        link.child_named("visual") << origin
        link.child_named("collision") << origin
      when "inertial" then 
        link.child_named('inertial') << transform_link_inertial(c).children
      when "collision" then 
        link.child_named('collision') << transform_link_collision(c).children
      when "visual" then 
        link.child_named('visual') << transform_link_visual(c).children
      else link << discard(c)
      end
    }
    link
  end
  
  def transform_link_inertial(elm)
    
  end

  def transform_link_collision(elm)
    XML::Element.new('collision', @outdoc) # elm
  end

  def transform_link_visual(elm)
    XML::Element.new('visual', @outdoc) # elm
  end

  def transform_joint(elm)
    XML::Element.new('joint', @outdoc) # elm
  end

  def discard(elm)
    XML::Comment.new(@outdoc, "[DISCARDED]") # : #{elm.to_s}")
  end
end

## Input
input_f = ARGV.length > 0 ? File.open(ARGV[0]) : STDIN 
input = Nokogiri::XML(input_f)
abort("root element is not <sdf>, but <#{input.root.name}>") unless input.root.name == "sdf"

model = input.root.>('model').first
abort("No <model> tag") if model.nil?

## Output
@outdoc = XML::Document.new

def element(name, attrs={}, children=[])
    elm = XML::Element.new(name, @outdoc)
    attrs.each {|k,v| elm[k] = v }
    children.each {|n| elm << n }
    elm
end

## Translation
robot = element('robot', { 'name' => model['name'] })

base_link = element('link', { 'name' => 'base' })
robot << base_link

model.>('pose').each do |src_pose|
    origin = transform_pose(src_pose)
    base_link.child_named("visual") << origin
    base_link.child_named("collision") << origin.dup
end

model.>('link').each do |src_link|
    link = element('link', { 'name' => src_link['name'] })
    
    src_link.>('pose').each do |src_pose|
        origin = transform_pose(src_pose)
        link.child_named("visual") << origin
        link.child_named("collision") << origin.dup
    end
    
    src_link.>('inertial').first.map do |src_inertial|
        inertial = element('inertial')
        src_inertial.>("pose").first.map do |src_pose|
            inertial << transform_pose(src_pose, {:compact_origin => true})
        end
        
        src_inertial.>("mass").first.map do |src_mass|
            inertial << element('mass', { 'value' => src_mass.text })
        end
        
        src_inertial.>("inertia").first.map do |src_inertia|
            inertia = element('inertia')
            src_inertia.children.each do |item|
                inertia[item.name] = item.text # if item.name =~ /^i[xyz][xyz]$/
            end
            inertial << inertia
        end
        
        link << inertial
    end
    
    src_link.>('collision').first.map do |src_collision|
    end
    
    src_link.>('visual').first.map do |src_visual|
    end
    
    robot << link
end

@outdoc.root = robot
puts @outdoc.to_s


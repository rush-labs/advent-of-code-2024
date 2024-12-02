module Utils
  module_function

  # Read the file and parse into columns
  def read_and_parse(filename)
    data = []
    File.foreach(filename) do |line|
      numbers = line.split.map(&:to_i)
      data << numbers
    end
    data
  end
end
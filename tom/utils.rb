module Utils
  module_function

  # Read the file and parse to get array of numbers
  def read_and_parse_to_i(filename)
    data = []
    File.foreach(filename) do |line|
      numbers = line.split.map(&:to_i)
      data << numbers
    end
    data
  end
end
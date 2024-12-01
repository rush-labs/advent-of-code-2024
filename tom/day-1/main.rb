# Read the file and parse into columns
def read_and_parse(filename)
  data = []
  File.foreach(filename) do |line|
    numbers = line.split.map(&:to_i)
    data << numbers
  end
  data
end

# Returns [col1, col2, diff]
def process_data(data)
  column1 = data.map { |row| row[0] }.sort
  column2 = data.map { |row| row[1] }.sort

  column1.zip(column2).map do |a, b|
    [a, b, (a - b).abs]
  end
end


def part_one
  data = read_and_parse("tom/day-1/inputs.txt")
  results = process_data(data)

  total_diff = results.sum { |_, _, diff| diff}
  puts total_diff
end

def part_two
  data = read_and_parse("tom/day-1/inputs.txt")
  results = process_data(data)

  total = 0
  results.each do |row|
    val = row[0]
    count = results.count { |_, col2, _| col2 == val }
    total += val * count
  end
  puts total
end

part_two
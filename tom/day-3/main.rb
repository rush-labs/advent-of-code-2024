require_relative '../utils'

def mul(x, y)
  x.to_i * y.to_i
end

# Read the file and extract string
def mul_scanner(filename)
  factors = []
  File.foreach(filename) do |line|
    lines = line.scan(/mul\((\d{1,3}),(\d{1,3})\)/)
    factors << lines
  end
  factors
end

def part_one(file_name)
  factors = mul_scanner(file_name)
  total = factors.sum{|line| line.sum{|factor| mul(factor[0], factor[1]) }}
  puts "Total: #{total}"
end

def part_two(file_name)

end

part_one("tom/day-3/example.txt")
part_one("tom/day-3/inputs.txt")
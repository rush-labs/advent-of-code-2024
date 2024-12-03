require_relative '../utils'

def mul(x, y)
  x.to_i * y.to_i
end

# Read the file and extract string
def mul_scanner(filename)
  factors = []
  File.foreach(filename) do |line|
    factors = line.scan(/mul\((\d{1,3}),(\d{1,3})\)/)
  end
  factors
end

def part_one
  factors = mul_scanner("tom/day-3/inputs.txt")
  print factors
  total = factors.sum{|factor| mul(factor[0], factor[1]) }
  puts total
  # input = File.readlines("tom/day-3/example.txt").map(&:chomp)
  # puts input
  # string = input.to_s
  # puts string.split(/mul\((\d{1,3}),\1\)/)
end

part_one
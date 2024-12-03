require_relative '../utils'

def safe_report?(levels)
  differences = levels.each_cons(2).map { |a, b| b - a }
  valid_differences = differences.all? { |d| d.abs >= 1 && d.abs <= 3 }


  all_increasing = differences.all? { |d| d > 0 }
  all_decreasing = differences.all? { |d| d < 0 }

  valid_differences && (all_increasing || all_decreasing)
end

def safe_report_with_one_level_error?(levels)
  return false if levels.length < 2

  differences = levels.each_cons(2).map { |a, b| b - a }
  if differences.all? { |d| d.between?(1, 3) } || differences.all? { |d| d.between?(-3, -1) }
    return true
  end

  # Check if safe when removing one level
  levels.each_index do |i|
    modified_levels = levels[0...i] + levels[i+1..-1]
    modified_differences = modified_levels.each_cons(2).map { |a, b| b - a }

    if modified_differences.all? { |d| d.between?(1, 3) } || modified_differences.all? { |d| d.between?(-3, -1) }
      return true
    end
  end

  false
end

def part_one
  data = Utils.read_and_parse_to_i("tom/day-2/example.txt")
  safe_count = data.count { |report| safe_report?(report) }

  puts safe_count
end

def part_two
  data = Utils.read_and_parse_to_i("tom/day-2/inputs.txt")
  results = data.count { |report| safe_report_with_one_level_error?(report) }

  puts results
end

part_two
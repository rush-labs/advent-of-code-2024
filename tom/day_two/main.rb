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
  invalid_count = differences.count { |d| d.abs < 1 || d.abs > 3 }
  return false if invalid_count > 1

  valid_differences = differences.select { |d| d.abs >= 1 && d.abs <= 3 }
  return false if valid_differences.empty?

  all_increasing = valid_differences.all? { |d| d > 0 }
  all_decreasing = valid_differences.all? { |d| d < 0 }

  all_increasing || all_decreasing
end

def part_one
  data = Utils.read_and_parse("tom/day_two/example.txt")
  safe_count = data.count { |report| safe_report?(report) }

  puts safe_count
end

def part_two
  data = Utils.read_and_parse("tom/day_two/example.txt")
  safe_count = data.count { |report| safe_report_with_one_level_error?(report) }

  puts safe_count
end

part_two
defmodule Day5 do
  @base_path "./lib/day5/inputs/"
  def load_input(path) do
    File.read!(@base_path <> path)
  end

  def part2 do
    %{rules: rules, reports: reports} =
      load_input("input.txt")
      |> String.split("\n")
      |> Enum.reject(fn value -> value == "" end)
      |> Enum.map(fn value -> {sort_line(value), value} end)
      |> Enum.map(&parse_line(&1))
      |> Enum.reduce(%{rules: [], reports: []}, fn nextLine, state ->
        case nextLine do
          {:rule, value} -> %{rules: [value | state.rules], reports: state.reports}
          {:report, value} -> %{rules: state.rules, reports: [value | state.reports]}
        end
      end)

    reports
    |> Enum.reject(&is_report_valid(&1, rules))
    |> Enum.map(&find_middle_in_list(&1, rules))
    |> Enum.sum()
  end

  defp find_middle_in_list(report, rules) do
    limit = (length(report) - 1) / 2

    rules_in_report =
      rules
      |> Enum.filter(fn [a, b] -> Enum.member?(report, a) && Enum.member?(report, b) end)

    report
    |> Enum.find(fn value ->
      left_pages = rules_in_report |> Enum.count(fn [_a, b] -> b == value end)
      right_pages = rules_in_report |> Enum.count(fn [a, _b] -> a == value end)
      left_pages == limit && right_pages == limit
    end)
  end

  def part1 do
    %{rules: rules, reports: reports} =
      load_input("input.txt")
      |> String.split("\n")
      |> Enum.reject(fn value -> value == "" end)
      |> Enum.map(fn value -> {sort_line(value), value} end)
      |> Enum.map(&parse_line(&1))
      |> Enum.reduce(%{rules: [], reports: []}, fn nextLine, state ->
        case nextLine do
          {:rule, value} -> %{rules: [value | state.rules], reports: state.reports}
          {:report, value} -> %{rules: state.rules, reports: [value | state.reports]}
        end
      end)

    reports
    |> Enum.filter(&is_report_valid(&1, rules))
    |> Enum.map(&find_middle(&1))
    |> Enum.sum()
    |> IO.inspect(charlists: :as_lists)
  end

  defp find_middle(list) do
    Enum.at(list, trunc((length(list) - 1) / 2))
  end

  defp is_report_valid(report, rules) do
    rules
    |> Enum.filter(fn [a, b] -> Enum.member?(report, a) && Enum.member?(report, b) end)
    |> Enum.all?(&compare_rule_to_report(&1, report))
  end

  defp compare_rule_to_report([a, b], report) do
    case [Enum.member?(report, a), Enum.member?(report, b)] do
      [true, true] ->
        aIndex = Enum.find_index(report, &(&1 == a))
        bIndex = Enum.find_index(report, &(&1 == b))
        aIndex < bIndex

      _ ->
        false
    end
  end

  defp parse_line(line) do
    case line do
      {:rule, value} -> {:rule, parse_rule(value)}
      {:report, value} -> {:report, String.split(value, ",") |> Enum.map(&String.to_integer(&1))}
    end
  end

  defp sort_line(value) do
    if String.contains?(value, "|") do
      :rule
    else
      :report
    end
  end

  defp parse_rule(value) do
    case String.split(value, "|") do
      [a, b] -> [String.to_integer(a), String.to_integer(b)]
      _ -> raise "Invalid rule!"
    end
  end
end

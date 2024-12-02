defmodule Day1 do
  @base_path "./lib/day1/inputs/"

  def load_input(path) do
    case File.read(@base_path <> path) do
      {:ok, file} -> file
      {:error, :enoent} -> {:error}
    end
  end

  def distance(a, b) do
    a - b |> abs
  end

  def occurrences(el, list) do
    Enum.count(list, &(&1 == el))
  end

  def part1 do
    input = Day1.load_input("input.txt")
    [leftList, rightList] = String.split(input, "\n", trim: true)
      |> Enum.map(&String.split/1)
      |> Enum.map(fn value -> Enum.map(value, fn v -> String.to_integer(v) end) end)
      |> Enum.reduce(%{a: [], b: []}, fn [a, b], total ->
            %{a: total.a ++ [a], b: total.b ++ [b]}
          end)
      |> Enum.map(fn {key, value} -> {key, Enum.sort(value)} end) |> Map.new()
      |> Enum.map(fn {_key, value} -> value end)

    Enum.reduce(Enum.with_index(leftList), 0, fn {item, index}, total ->
      total + distance(item, Enum.at(rightList, index))
    end)
  end

  def part2 do
    input = Day1.load_input("input.txt")
    [leftList, rightList] = String.split(input, "\n", trim: true)
             |> Enum.map(&String.split/1)
             |> Enum.map(fn value -> Enum.map(value, fn v -> String.to_integer(v) end) end)
             |> Enum.reduce(%{a: [], b: []}, fn [a, b], total ->
      %{a: total.a ++ [a], b: total.b ++ [b]}
    end)
             |> Enum.map(fn {key, value} -> {key, Enum.sort(value)} end) |> Map.new()
             |> Enum.map(fn {_key, value} -> value end)

    Enum.reduce(leftList, 0, fn item, total ->
      total + occurrences(item, rightList) * item
    end)
  end
end

defmodule Day4 do
  @base_path "./lib/day4/inputs/"
  import Enum

  def load_input(path) do
    File.read!(@base_path <> path)
  end

  ######################
  # PART 1             #
  ######################

  def get_char_at_pos(_matrix, %{x: x, y: y}) when x < 0 or y < 0 do
    nil
  end

  def get_char_at_pos(matrix, %{x: x, y: y}) do
    case Enum.at(matrix, y) do
      nil -> nil
      row -> Enum.at(row, x)
    end
  end

  defp is_xmas(list) do
    list
    |> reject(&is_nil(&1))
    |> join("")
    |> case do
      "XMAS" -> 1
      _ -> 0
    end
  end

  def read_in_direction(:left, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x - value, y: y}) end)
  end

  def read_in_direction(:right, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x + value, y: y}) end)
  end

  def read_in_direction(:up, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x, y: y - value}) end)
  end

  def read_in_direction(:down, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x, y: y + value}) end)
  end

  def read_in_direction(:up_and_right, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x + value, y: y - value}) end)
  end

  def read_in_direction(:up_and_left, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x - value, y: y - value}) end)
  end

  def read_in_direction(:down_and_right, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x + value, y: y + value}) end)
  end

  def read_in_direction(:down_and_left, matrix, %{x: x, y: y}) do
    0..3
    |> Enum.map(fn value -> get_char_at_pos(matrix, %{x: x - value, y: y + value}) end)
  end

  def read_char("X", matrix, pos) do
    [:left, :right, :up, :down, :up_and_right, :up_and_left, :down_and_right, :down_and_left]
    |> map(fn value ->
      read_in_direction(value, matrix, pos)
      |> is_xmas()
    end)
    |> sum()
  end

  def read_char(_value, _matrix, _pos) do
    0
  end

  def count_xmas_for_row(matrix, row, y) do
    row
    |> with_index()
    |> map(fn {item, x} ->
      read_char(item, matrix, %{x: x, y: y})
    end)
  end

  def part1 do
    matrix =
      load_input("input.txt")
      |> String.split("\n")
      # Splits "abc" into ["a", "b", "c"]
      |> map(&String.graphemes/1)

    matrix
    |> with_index()
    |> map(fn {item, index} -> count_xmas_for_row(matrix, item, index) end)
    |> List.flatten()
    |> sum()
  end

  ######################
  # PART 2             #
  ######################

  defp read_char_2("A", matrix, %{x: x, y: y}) do
    first_diagonal =
      read_in_direction(:down_and_right, matrix, %{x: x - 1, y: y - 1})
      |> reject(&is_nil(&1))
      |> join("")
      |> String.slice(0..2)

    second_diagonal =
      read_in_direction(:down_and_left, matrix, %{x: x + 1, y: y - 1})
      |> reject(&is_nil(&1))
      |> join("")
      |> String.slice(0..2)

    case [first_diagonal, second_diagonal] do
      ["MAS", "MAS"] -> 1
      ["MAS", "SAM"] -> 1
      ["SAM", "MAS"] -> 1
      ["SAM", "SAM"] -> 1
      _ -> 0
    end
  end

  defp read_char_2(_value, _matrix, _pos) do
    0
  end

  defp count_cross_mas_for_row(matrix, row, y) do
    row
    |> with_index()
    |> map(fn {item, x} ->
      read_char_2(item, matrix, %{x: x, y: y})
    end)
  end

  def part2 do
    matrix =
      load_input("input.txt")
      |> String.split("\n")
      |> map(&String.replace(&1, ~r/[^MAS]/, "."))
      |> map(&String.graphemes/1)

    matrix
    |> with_index()
    |> map(fn {item, index} -> count_cross_mas_for_row(matrix, item, index) end)
    |> List.flatten()
    |> sum()
  end
end

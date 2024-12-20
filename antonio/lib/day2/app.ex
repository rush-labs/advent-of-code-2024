defmodule Day2 do
  @base_path "./lib/day2/inputs/"
  import Enum
  import List

  def load_input(path) do
    case File.read(@base_path <> path) do
      {:ok, file} -> file
      {:error, :enoent} -> {:error}
    end
  end

  def evaluate_report(report) do
    chunk_every(report, 2, 1, :discard)
    |> map(fn [a, b] -> a - b end)
    |> then(fn diffs ->
      cond do
        first(diffs) == 0 -> false
        first(diffs) < 0 -> all?(diffs, fn value -> value < 0 && abs(value) < 4 end)
        true -> all?(diffs, fn value -> value > 0 && abs(value) < 4 end)
      end
    end)
  end

  def part1 do
    Day2.load_input("input.txt")
    |> String.split("\n", trim: true)
    |> map(fn value -> String.split(value) |> map(&String.to_integer/1) end)
    |> map(fn report ->
      evaluate_report(report)
    end)
    |> count(fn value -> value == true end)
  end

  def get_direction(report) do
    [first | tail] = report
    next = find(tail, fn value -> value != first end)

    cond do
      first > next ->
        :incrementing

      first < next ->
        :decrementing
    end
  end

  def build_list_from_chunks(chunks) do
    map(chunks, fn chunk -> first(chunk) end)
  end

  def evaluate_report_2(report, attempt) do
    direction = get_direction(report)

    values =
      chunk_every(report, 2, 1)
      |> map(fn chunk ->
        case chunk do
          [a, b] ->
            case direction do
              :incrementing ->
                %{valid: a > b && abs(a - b) < 4, chunk: [a, b]}

              :decrementing ->
                %{valid: a < b && abs(a - b) < 4, chunk: [a, b]}
            end

          [a] ->
            %{valid: true, chunk: [a]}
        end
      end)

    valid = all?(values, fn %{valid: valid} -> valid == true end)

    cond do
      attempt == 0 && !valid ->
        any?(values, fn value ->
          Day2.evaluate_report_2(
            delete(
              values,
              value
            )
            |> map(fn %{chunk: chunk} -> chunk end)
            |> Day2.build_list_from_chunks(),
            1
          )
        end)

      true ->
        valid
    end
  end

  def part2 do
    Day2.load_input("input.txt")
    |> String.split("\n", trim: true)
    |> map(fn value -> String.split(value) |> map(&String.to_integer/1) end)
    |> map(&Day2.evaluate_report_2(&1, 0))
    |> count(fn value -> value == true end)
  end
end

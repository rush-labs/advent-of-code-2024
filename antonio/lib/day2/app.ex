defmodule Day2 do
  @base_path "./lib/day2/inputs/"

  def load_input(path) do
    case File.read(@base_path <> path) do
      {:ok, file} -> file
      {:error, :enoent} -> {:error}
    end
  end

  def evaluate_report(report) do
    Enum.chunk_every(report, 2, 1, :discard)
    |> Enum.map(fn [a, b] -> a - b end)
    |> then(fn diffs ->
      cond do
        List.first(diffs) == 0 -> false
        List.first(diffs) < 0 -> Enum.all?(diffs, fn value -> value < 0 && abs(value) < 4 end)
        true -> Enum.all?(diffs, fn value -> value > 0 && abs(value) < 4 end)
      end
    end)
  end

  def part1 do
    Day2.load_input("input.txt")
    |> String.split("\n", trim: true)
    |> Enum.map(fn value -> String.split(value) |> Enum.map(&String.to_integer/1) end)
    |> Enum.map(fn report ->
      evaluate_report(report)
    end)
    |> Enum.count(fn value -> value == true end)
  end

  def get_direction(report) do
    [first | tail] = report
    next = Enum.find(tail, fn value -> value != first end)

    cond do
      first > next ->
        :incrementing

      first < next ->
        :decrementing

      true ->
        :invalid
    end
  end

  def build_list_from_chunks(chunks) do
    Enum.map(chunks, fn chunk -> List.first(chunk) end)
  end

  def evaluate_report_2(report, attempt) do
    direction = get_direction(report)

    values =
      Enum.chunk_every(report, 2, 1)
      |> Enum.map(fn chunk ->
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

    valid = Enum.all?(values, fn %{valid: valid} -> valid == true end)

    #    cond do
    #      attempt == 0 && !valid ->
    #        evaluate_report_2(
    #          List.delete(
    #            values,
    #            Enum.find(values, fn map -> map.valid == false end)
    #          )
    #          |> Enum.map(fn %{chunk: chunk} -> chunk end)
    #          |> Day2.build_list_from_chunks(),
    #          1
    #        )
    #
    #      true ->
    #        valid
    #    end
    cond do
      attempt == 0 && !valid ->
        Enum.any?(values, fn value ->
          Day2.evaluate_report_2(
            List.delete(
              values,
              value
            )
            |> Enum.map(fn %{chunk: chunk} -> chunk end)
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
    |> Enum.map(fn value -> String.split(value) |> Enum.map(&String.to_integer/1) end)
    |> Enum.map(&Day2.evaluate_report_2(&1, 0))
    |> Enum.count(fn value -> value == true end)
  end
end

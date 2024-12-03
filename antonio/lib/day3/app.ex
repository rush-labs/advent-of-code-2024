defmodule Day3 do
  @base_path "./lib/day3/inputs/"
  import Enum

  def load_input(path) do
    File.read!(@base_path <> path)
  end

  def instruction_type(instruction) do
    cond do
      String.starts_with?(instruction, "mul(") -> :mul
      String.starts_with?(instruction, "do(") -> :do
      String.starts_with?(instruction, "don't(") -> :dont
    end
  end

  def handle_instruction(instruction) do
    instruction
    |> String.replace("mul(", "")
    |> String.replace(")", "")
    |> String.split(",")
    |> Enum.map(fn el -> String.to_integer(el) end)
    |> then(fn [a, b] ->
      a * b
    end)
  end

  def handle_instruction_2(instruction) do
    case Day3.instruction_type(instruction) do
      :mul ->
        instruction
        |> String.replace("mul(", "")
        |> String.replace(")", "")
        |> String.split(",")
        |> Enum.map(fn el -> String.to_integer(el) end)
        |> then(fn [a, b] ->
          {:mult, a * b}
        end)
      :dont -> {:dont}
      :do -> {:do}
    end
  end


  def part1 do
    load_input("input.txt")
    |> then(fn value -> Regex.scan(~r/mul\(\d{1,3},\d{1,3}\)/, value) end)
    |> List.flatten
    |> map(&Day3.handle_instruction(&1))
    |> sum()
  end

  def part2 do
    load_input("input.txt")
    |> then(fn value -> Regex.scan(~r/mul\([0-9]+,[0-9]+\)|do\(\)|don\'t\(\)/, value) end)
    |> List.flatten
    |> map(&Day3.handle_instruction_2(&1))
    |> IO.inspect
    |> reduce(%{enabled: true, total: 0}, fn nextInstruction, %{enabled: enabled, total: total} ->
      case nextInstruction do
        {:do} -> %{enabled: true, total: total}
        {:dont} -> %{enabled: false, total: total}
        {:mult, value} ->
          case enabled do
            true -> %{enabled: true, total: total + value}
            false -> %{enabled: false, total: total}
          end
      end
    end)
    |> then(fn value -> value.total end)
  end
end

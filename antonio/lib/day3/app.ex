defmodule Day3 do
  @base_path "./lib/day3/inputs/"
  import Enum

  def load_input(path) do
    File.read!(@base_path <> path)
  end

  ######################
  # PART 1             #
  ######################

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

  def part1 do
    load_input("input.txt")
    |> then(fn value -> Regex.scan(~r/mul\(\d{1,3},\d{1,3}\)/, value) end)
    |> List.flatten()
    |> map(&Day3.handle_instruction(&1))
    |> sum()
  end

  ######################
  # PART 2             #
  ######################

  defp parse_instruction("do(" <> _), do: :enable
  defp parse_instruction("don't(" <> _), do: :disable
  defp parse_instruction(multiplication), do: parse_multiplication(multiplication)

  def parse_multiplication(instruction) do
    instruction
    |> String.replace("mul(", "")
    |> String.replace(")", "")
    |> String.split(",")
    |> Enum.map(&String.to_integer(&1))
    |> case do
      [a, b] -> {:multiply, a * b}
    end
  end

  defp process_instruction(:enable, state) do
    %{state | enabled?: true}
  end

  defp process_instruction(:disable, state) do
    %{state | enabled?: false}
  end

  defp process_instruction({:multiply, value}, %{enabled?: true, total: total}) do
    %{enabled?: true, total: total + value}
  end

  defp process_instruction({:multiply, _value}, state) do
    state
  end

  def part2 do
    load_input("input.txt")
    |> then(fn value -> Regex.scan(~r/mul\([0-9]+,[0-9]+\)|do\(\)|don\'t\(\)/, value) end)
    |> List.flatten()
    |> map(&parse_instruction(&1))
    |> reduce(%{enabled?: true, total: 0}, &process_instruction/2)
    |> Map.get(:total)
  end
end

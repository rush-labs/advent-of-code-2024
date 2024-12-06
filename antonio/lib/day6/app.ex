defmodule Day6 do
  import Enum

  @base_path "./lib/day6/inputs/"
  @directions_offset %{
    up: {0, -1},
    right: {1, 0},
    down: {0, 1},
    left: {-1, 0}
  }

  defp load_input(path) do
    File.read!(@base_path <> path)
  end

  def part2 do
    grid =
      load_input("input.txt")
      |> String.split("\n")
      |> map(&String.graphemes(&1))

    possible_grids =
      grid
      |> with_index()
      |> flat_map(fn {row, y} ->
        row
        |> with_index()
        |> map(fn {cell, x} ->
          case categorize_cell(read_at_pos(grid, %{x: x, y: y})) do
            :empty -> update_at(grid, y, x, "#")
            _ -> nil
          end
        end)
      end)
      |> reject(&is_nil(&1))

    total = length(possible_grids)

    possible_grids
    |> Task.async_stream(
      fn grid ->
        {grid, solve_maze_2(grid, %{})}
      end,
      max_concurrency: System.schedulers_online(),
      ordered: true
    )
    |> Stream.with_index()
    |> Enum.reduce(0, fn {{:ok, {_grid, result}}, index}, acc ->
      IO.puts("#{index}/#{total}")
      if result == :time_loop, do: acc + 1, else: acc
    end)
  end

  def part1 do
    grid =
      load_input("input.txt")
      |> String.split("\n")
      |> map(&String.graphemes(&1))

    solved_grid = solve_maze(grid)
    # print_grid(solved_grid)
    count_visited_cells(solved_grid)
  end

  def part2 do
  end

  defp find_direction("^") do
    :up
  end

  defp find_direction(">") do
    :right
  end

  defp find_direction("v") do
    :down
  end

  defp find_direction("<") do
    :left
  end

  defp read_at_pos(_grid, %{x: x, y: _y}) when x < 0 do
    nil
  end

  defp read_at_pos(_grid, %{x: _x, y: y}) when y < 0 do
    nil
  end

  defp read_at_pos(grid, %{x: x, y: y}) do
    case at(grid, y) do
      nil -> nil
      row -> at(row, x)
    end
  end

  defp categorize_cell(".") do
    :empty
  end

  defp categorize_cell("o") do
    :visited
  end

  defp categorize_cell("#") do
    :obstacle
  end

  defp categorize_cell(value) when is_nil(value) do
    :out_of_bound
  end

  defp categorize_cell(value) do
    :guard
  end

  defp find_guard([row | rows]) do
    case find_guard_in_row(row, 0, 0) do
      nil -> find_guard_in_rows(rows, 1)
      pos -> pos
    end
  end

  defp find_guard_in_row([cell | rest], x, y) do
    if categorize_cell(cell) == :guard do
      %{x: x, y: y, cell: cell}
    else
      find_guard_in_row(rest, x + 1, y)
    end
  end

  defp find_guard_in_row([], _, _), do: nil

  defp find_guard_in_rows([row | rows], y) do
    case find_guard_in_row(row, 0, y) do
      nil -> find_guard_in_rows(rows, y + 1)
      pos -> pos
    end
  end

  defp find_guard_in_rows([], _), do: nil

  defp count_visited_cells(grid) do
    List.flatten(grid)
    |> count(fn cell -> categorize_cell(cell) == :visited end)
  end

  defp direction_to_direction_string(direction) do
    case direction do
      :right -> ">"
      :down -> "v"
      :left -> "<"
      :up -> "^"
    end
  end

  defp visit_cell(direction, from, to, grid) do
    grid
    |> update_at(from.y, from.x, "o")
    |> update_at(to.y, to.x, direction_to_direction_string(direction))
  end

  defp update_at(grid, y, x, value) do
    List.update_at(grid, y, &List.replace_at(&1, x, value))
  end

  defp rotate_right(direction) do
    case direction do
      :up -> :right
      :right -> :down
      :down -> :left
      :left -> :up
    end
  end

  defp print_grid(grid) do
    IO.puts("============= next grid =============")

    map(
      grid,
      fn row -> join(row, "") end
    )
    |> map(&IO.inspect(&1))
  end

  defp is_stuck_in_loop(x, y, direction, record) do
    key = get_map_key(x, y, direction)
    Map.get(record, key)
  end

  defp get_map_key(x, y, direction) do
    "#{x};#{y};#{direction}"
  end

  defp solve_maze(grid) do
    %{x: x, y: y, cell: cell} = find_guard(grid)
    direction = find_direction(cell)
    next_cell = get_cell_in_direction(grid, direction, %{x: x, y: y})
    next_type = categorize_cell(next_cell.value)

    case next_type do
      :empty ->
        solve_maze(visit_cell(direction, %{x: x, y: y}, next_cell, grid))

      :visited ->
        solve_maze(visit_cell(direction, %{x: x, y: y}, next_cell, grid))

      :obstacle ->
        next_direction = rotate_right(direction)
        solve_maze(update_at(grid, y, x, direction_to_direction_string(next_direction)))

      :out_of_bound ->
        List.replace_at(
          grid,
          y,
          List.replace_at(
            at(grid, y),
            x,
            "o"
          )
        )
    end
  end

  defp solve_maze_2(grid, record) do
    # IO.inspect(grid)
    %{x: x, y: y, cell: cell} = find_guard(grid)
    direction = find_direction(cell)
    next_cell = get_cell_in_direction(grid, direction, %{x: x, y: y})
    next_type = categorize_cell(next_cell.value)

    if is_stuck_in_loop(x, y, direction, record) do
      :time_loop
    else
      new_record = Map.put(record, get_map_key(x, y, direction), true)

      case next_type do
        :empty ->
          solve_maze_2(visit_cell(direction, %{x: x, y: y}, next_cell, grid), new_record)

        :visited ->
          solve_maze_2(visit_cell(direction, %{x: x, y: y}, next_cell, grid), new_record)

        :obstacle ->
          next_direction = rotate_right(direction)

          solve_maze_2(
            update_at(grid, y, x, direction_to_direction_string(next_direction)),
            new_record
          )

        :out_of_bound ->
          :solvable
      end
    end
  end

  defp update_direction(grid, x, y, {_, _, dir_char}) do
    update_at(grid, y, x, dir_char)
  end

  defp get_cell_in_direction(grid, direction, %{x: x, y: y}) do
    {x_offset, y_offset} = Map.get(@directions_offset, direction)
    next_position = %{x: x + x_offset, y: y + y_offset}
    %{x: next_position.x, y: next_position.y, value: read_at_pos(grid, next_position)}
  end
end

defmodule AntonioTest do
  use ExUnit.Case
  doctest Antonio

  test "greets the world" do
    assert Antonio.hello() == :world
  end
end

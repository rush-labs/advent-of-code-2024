import Foundation

enum Status {
    case safe     // Changed to lowercase to follow Swift naming conventions
    case unsafe   // Changed to lowercase to follow Swift naming conventions
}

struct Day2 {
    func readInputFile() -> [[Int]] {
        guard let input = try? String(contentsOfFile: "Sources/Day2/input.txt") else {
            fatalError("Could not read file")
        }
        let lines = input.components(separatedBy: .newlines)

        let floors: [[Int]] = lines.map { line in
            return line.split(separator: " ").compactMap { Int($0) }
        }.filter { !$0.isEmpty }

        return floors
    }

    func solvePart1() -> String {
        let floors = readInputFile()

        let status: [Status] = floors.map { floor in
            if floor.sorted() != floor && floor.sorted(by: >) != floor {
                return .unsafe
            }

            return floor.enumerated().reduce(.safe) { (s, tuple) in
                let (index, pos) = tuple

                guard index > 0 else { return s }

                if s == .unsafe {
                    return .unsafe
                }

                let diff = abs(pos - floor[index - 1])

                if diff > 3 || diff < 1 {
                    return .unsafe
                }

                return .safe
            }
        }

        return String(status.filter { $0 == .safe }.count)
    }

    func generatePartialFloors(mainFloor: [Int]) -> [[Int]] {
        return mainFloor.enumerated().map { index, _ in
            mainFloor.enumerated().filter { i, _ in
                index != i
            }.map { $0.1 }
        }
    }

    func solvePart2() -> String {
        let floors = readInputFile()

        let status: [Status] = floors.map { mainFloor in
            let statusForGeneratedFloors = generatePartialFloors(mainFloor: mainFloor).map { floor in
                if floor.sorted() != floor && floor.sorted(by: >) != floor {
                    return Status.unsafe
                }

                return floor.enumerated().reduce(.safe) { (s, tuple) in
                    let (index, pos) = tuple

                    guard index > 0 else { return s }

                    if s == .unsafe {
                        return .unsafe
                    }

                    let diff = abs(pos - floor[index - 1])

                    if diff > 3 || diff < 1 {
                        return .unsafe
                    }

                    return .safe
                }
            }

            return statusForGeneratedFloors.contains(where: { $0 == .safe }) ? .safe : .unsafe
        }

        return String(status.filter { $0 == .safe }.count)
    }
}

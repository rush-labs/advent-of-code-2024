import Foundation

enum Status {
    case Safe
    case Unsafe
}

struct Day2 {
    func readInputFile() -> [[Int]] {
        guard let input = try? String(contentsOfFile: "Sources/Day2/input.txt") else {
            fatalError("Could not read file")
        }
        let lines = input.components(separatedBy: .newlines)

        let floors: [[Int]] = lines.map { line in
            return line.split(separator: " ").map { numberString in Int(numberString) ?? 0}
        }.filter { floor in floor != []}


        return floors
    }

    func solvePart1() -> String {
        let floors = readInputFile()

        let status: [Status] = floors.map { floor in
            if(floor.sorted() != floor && floor.sorted(by: >) != floor){
                return Status.Unsafe
            }
            return floor.enumerated().reduce(Status.Safe) { (s, tuple) in
                let (index, pos) = tuple

                guard index > 0 else { return s}

                if s == .Unsafe {
                    return .Unsafe
                }

                let diff = abs(pos - floor[index-1])

                if diff > 3 || diff < 1 {
                    return .Unsafe
                }

                return .Safe

            }
        }

        return String(status.filter { s in s == Status.Safe}.count)
    }

}

import Foundation
struct Day1 {
    func solve() -> String {
        guard let input = try? String(contentsOfFile: "Sources/Day1/input.txt") else {
            fatalError("Could not read file")
        }

        let lines = input.components(separatedBy: .newlines)
        let leftLane = lines.map { line in
            let numbers = line.split(separator: " ")
            guard numbers.count > 0 else {
                return 0
            }
            return Int(numbers[0]) ?? 0
        }.sorted()

        let rightLane = lines.map { line in
            let numbers = line.split(separator: " ")
            guard numbers.count > 1 else {
                return 0
            }
            return Int(numbers[1]) ?? 0
        }.sorted()


        let distances = leftLane.enumerated().map { (index, leftNumber) in
            return abs(leftNumber - rightLane[index])
        }

        let totalDistance = distances.reduce(0) { (total, distance) in
            return  total + distance
        }

        return String(totalDistance)
    }
}

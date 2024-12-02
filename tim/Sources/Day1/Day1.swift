import Foundation

struct Lanes {
    let leftLane: [Int]
    let rightLane: [Int]
}

struct Day1 {
    func readInputFile() -> Lanes {
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
        return Lanes(leftLane: leftLane, rightLane: rightLane)
    }
    func solvePart1() -> String {
        let input = readInputFile()


        let distances = input.leftLane.enumerated().map { (index, leftNumber) in
            return abs(leftNumber - input.rightLane[index])
        }

        let totalDistance = distances.reduce(0) { (total, distance) in
            return  total + distance
        }

        return String(totalDistance)
    }
    func solvePart2() -> String {
        let input = readInputFile()

        let similarityScore = input.leftLane.reduce(0) { ( total, leftNumber) in
            return total + (input.rightLane.filter { rightNumber in
              rightNumber == leftNumber
             }.count * leftNumber)
        }


        return String(similarityScore)
    }
}

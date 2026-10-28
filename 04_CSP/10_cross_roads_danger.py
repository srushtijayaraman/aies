"""Column-wise backtracking solver for CROSS + ROADS = DANGER."""
# Self-contained cryptarithmetic CSP solver; assigns distinct digits to letters.

def solve_cryptarithm(addends, result):
    words = addends + [result]
    leading = {word[0] for word in words if len(word) > 1}
    letters = set("".join(words))
    if len(letters) > 10:
        raise ValueError("More than 10 distinct letters cannot map to distinct digits.")
    mapping, used = {}, set()

    def column(col, carry):
        if col == len(result):
            return mapping.copy() if carry == 0 else None
        chars = [w[-1-col] for w in addends if col < len(w)]
        def add_letters(i, subtotal):
            if i == len(chars):
                total = subtotal + carry
                digit, next_carry = total % 10, total // 10
                ch = result[-1-col]
                if ch in mapping:
                    return column(col+1, next_carry) if mapping[ch] == digit else None
                if digit in used or (digit == 0 and ch in leading):
                    return None
                mapping[ch] = digit; used.add(digit)
                answer = column(col+1, next_carry)
                if answer is not None:
                    return answer
                used.remove(digit); del mapping[ch]
                return None
            ch = chars[i]
            if ch in mapping:
                return add_letters(i+1, subtotal + mapping[ch])
            for d in range(10):
                if d in used or (d == 0 and ch in leading):
                    continue
                mapping[ch] = d; used.add(d)
                answer = add_letters(i+1, subtotal+d)
                if answer is not None:
                    return answer
                used.remove(d); del mapping[ch]
            return None
        return add_letters(0, 0)
    return column(0, 0)

def value(word, mapping):
    return int("".join(str(mapping[ch]) for ch in word))

if __name__ == "__main__":
    solution = solve_cryptarithm(["CROSS", "ROADS"], "DANGER")
    if solution:
        for letter in sorted(solution):
            print(f"{letter} = {solution[letter]}")
        a, b, total = (value(w, solution) for w in ["CROSS", "ROADS", "DANGER"])
        print(f"{a} + {b} = {total}")
    else:
        print("No solution found.")

"""Column-wise backtracking solver for SEND + MORE = MONEY."""

def solve_cryptarithm(addends, result):
    words = addends + [result]
    leading = {word[0] for word in words if len(word) > 1}
    letters = set("".join(words))
    if len(letters) > 10:
        raise ValueError("More than 10 distinct letters cannot map to distinct decimal digits.")
    mapping, used = {}, set()
    max_cols = len(result)

    def assign_column(col, carry):
        if col == max_cols:
            return mapping.copy() if carry == 0 else None
        chars = [w[-1-col] for w in addends if col < len(w)]

        def sum_chars(i, subtotal):
            if i == len(chars):
                total = subtotal + carry
                digit, next_carry = total % 10, total // 10
                rch = result[-1-col]
                if rch in mapping:
                    if mapping[rch] != digit:
                        return None
                    return assign_column(col + 1, next_carry)
                if digit in used or (digit == 0 and rch in leading):
                    return None
                mapping[rch], used_digit = digit, digit
                used.add(used_digit)
                answer = assign_column(col + 1, next_carry)
                if answer is not None:
                    return answer
                used.remove(used_digit)
                del mapping[rch]
                return None
            ch = chars[i]
            if ch in mapping:
                return sum_chars(i + 1, subtotal + mapping[ch])
            for digit in range(10):
                if digit in used or (digit == 0 and ch in leading):
                    continue
                mapping[ch] = digit
                used.add(digit)
                answer = sum_chars(i + 1, subtotal + digit)
                if answer is not None:
                    return answer
                used.remove(digit)
                del mapping[ch]
            return None
        return sum_chars(0, 0)

    return assign_column(0, 0)

def value(word, mapping):
    return int("".join(str(mapping[ch]) for ch in word))

if __name__ == "__main__":
    solution = solve_cryptarithm(["SEND", "MORE"], "MONEY")
    if solution:
        for letter in sorted(solution):
            print(f"{letter} = {solution[letter]}")
        a, b, total = (value(w, solution) for w in ["SEND", "MORE", "MONEY"])
        print(f"{a} + {b} = {total}")
    else:
        print("No solution found.")

"""A few sample functions."""


def calculate_average(numbers):
    """Calculate the average of several numbers from a sequence."""
    total_sum = 0
    count = 0

    for number in numbers:
        total_sum += number
        count += 1

    if count == 0:
        return 0
    else:
        return total_sum / count


def process_list(input_list, output_list=[]):
    """Process a list according to their position.

    This function takes an input list and processes its elements according to
    their position: if the index is even, it multiplies the element by 2, and
    if the index is odd, it squares the element

    """
    for i in range(len(input_list)):
        if i % 2 == 0:
            output_list.append(input_list[i] * 2)
        else:
            output_list.append(input_list[i] ** 2)

    return output_list


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result = calculate_average(numbers)

    input_list = [1, 2, 3, 4]
    output_list = [5, 6, 7, 8]
    process_list(input_list, output_list=[])

import re

# pragma: no cover


def filter_log(log: str, exclude_patterns: []) -> str:
    r"""Remove patterns from a log file

    # Example usage
    log = "<paste the log contents here>"

    exclude_patterns = [
        r"##\[group\]",
        r"##\[endgroup\]",
        # Add any other patterns that you want to exclude
    ]

    filtered_log = filter_log(log, exclude_patterns)
    print(filtered_log)


    """
    lines = log.split("\n")
    filtered_lines = []

    for line in lines:
        include_line = True

        for pattern in exclude_patterns:
            if re.search(pattern, line):
                include_line = False
                break

        if include_line:
            filtered_lines.append(line)

    # Join filtered lines into a cleaned up log
    cleaned_log = "\n".join(filtered_lines)
    return cleaned_log


def extract_errors_from_log_file(log_text):
    """
    Extract error messages and context from a GitHub log text.

    This function looks for lines in the log file containing the words "ERROR"
    or "Exception".  It extracts up to 5 lines of context before the error
    message and includes them in the final error message. The function returns
    a list of all error messages found in the log file.

    Parameters
    ----------
    log_text : str
        GitHub log text to parse.

    Returns
    -------
    list[str]
        A list of error messages with context.

    Examples
    --------
    >>> errors = extract_errors_from_log_file("github.log")
    >>> for error in errors:
    ...     print(error)

    """
    errors = []

    # Look for lines containing error messages and extract the context
    for line in log_text.splitlines():
        if "ERROR" in line or "Exception" in line:
            error_context = []
            error_context.append(line)

            # Extract context before the error message
            for i in range(1, 6):
                if line.startswith((" " * i, "\t" * i)):
                    error_context.append(line[i:].strip())
                else:
                    break

            # Extract the error message
            match = re.search(r"\b[A-Z][A-Za-z]*Error?\b", line)
            if match:
                error_type = match.group(0)
                error_message = line.split(error_type, 1)[1].strip(": ")
                error_context.append(f"{error_type}: {error_message}")
                errors.append("\n".join(error_context))

    return errors

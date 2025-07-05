import math
from PIL import Image, ImageDraw, ImageFont

def is_prime(n):
    """
    Checks if a given number is prime.
    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
    """
    if n < 2:
        return False
    # Check for divisibility from 2 up to the square root of n
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_nearest_prime(n):
    """
    Finds the nearest prime number to a given integer n.
    If two primes are equidistant, the smaller one is chosen.
    """
    if n <= 2:
        return 2 # The nearest prime to 0, 1, or 2 is 2

    if is_prime(n):
        return n # If n itself is prime, it's the nearest

    lower_prime = -1
    upper_prime = -1

    # Search downwards for a prime
    i = 0
    while True:
        current_lower = n - i
        if current_lower < 2: # Stop if we go below 2 (no primes below 2)
            break
        if is_prime(current_lower):
            lower_prime = current_lower
            break
        i += 1

    # Search upwards for a prime
    j = 0
    while True:
        current_upper = n + j
        if is_prime(current_upper):
            upper_prime = current_upper
            break
        j += 1

    # Compare distances and return the nearest prime
    if lower_prime == -1: # Only an upper prime was found (e.g., for n=3, lower is 2, upper is 3)
        return upper_prime
    if upper_prime == -1: # Should not happen if n > 2 as primes are infinite
        return lower_prime

    diff_lower = n - lower_prime
    diff_upper = upper_prime - n

    if diff_lower <= diff_upper:
        return lower_prime
    else:
        return upper_prime

def create_table_image(numbers, nearest_primes, filename="prime_table.png"):
    """
    Creates an image of the table with numbers and their nearest primes.
    """
    # Image settings
    width = 400
    row_height = 40
    padding_x = 20
    padding_y = 10
    header_height = 50
    num_rows = len(numbers)
    height = header_height + num_rows * row_height + padding_y * 2

    # Create a blank white image
    img = Image.new('RGB', (width, height), color = (255, 255, 255))
    d = ImageDraw.Draw(img)

    try:
        # Try to load a common font, otherwise use default
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        print("Could not load 'arial.ttf'. Using default font.")

    # Colors
    text_color = (0, 0, 0) # Black
    line_color = (150, 150, 150) # Grey

    # Draw header
    d.text((padding_x, padding_y), "Number", fill=text_color, font=font)
    d.text((width / 2 + padding_x, padding_y), "Nearest Prime", fill=text_color, font=font)
    d.line([(0, header_height - 5), (width, header_height - 5)], fill=line_color, width=2)

    # Draw rows
    for i in range(num_rows):
        y_pos = header_height + i * row_height + padding_y
        d.text((padding_x, y_pos), str(numbers[i]), fill=text_color, font=font)
        d.text((width / 2 + padding_x, y_pos), str(nearest_primes[i]), fill=text_color, font=font)
        if i < num_rows - 1:
            d.line([(0, y_pos + row_height - padding_y), (width, y_pos + row_height - padding_y)], fill=line_color, width=1)

    # Save the image
    img.save(filename)
    print(f"Table saved as {filename}")


def main():
    """
    Main function to get user input, find nearest primes, and display results.
    """
    numbers = []
    nearest_primes = []

    print("Please enter 10 numbers:")
    for i in range(10):
        while True:
            try:
                num = int(input(f"Enter number {i + 1}: "))
                numbers.append(num)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

    print("\nCalculating nearest prime numbers...")
    for num in numbers:
        nearest_primes.append(find_nearest_prime(num))

    # Create and save the table as an image
    create_table_image(numbers, nearest_primes)

if __name__ == "__main__":
    main()




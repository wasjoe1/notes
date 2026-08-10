# why euclidean algo works? (finding GCD)
- qns: why does repeatedly subtracting smaller number from larger number, eventually produce GCD
- ans:
    - claim: If a > b, then gcd(a, b) = gcd(a-b, b).
    - This is because any number that divides both a and b must also divide (a-b)
    - so conversely, any number dividing both (a-b) and b must also divide a (since a = (a-b) + b).
    - hence, subtracting doesn't change the set of common divisors —> it just shrinks the numbers while preserving the gcd
    - keep doing this until two numbers are equal (or one hits 0) and that final value is the gcd
    * greatest divisor is never broken apart
    * visualization: https://www.youtube.com/watch?v=Jwf6ncRmhPg&t=520s
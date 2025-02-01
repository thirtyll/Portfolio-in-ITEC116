from fastapi import FastAPI

app = FastAPI()

@app.get("/factorial/{starting_number}")
def compute_factorial(starting_number: int):
    if starting_number == 0:
        return {"result": False}

    
    factorial_result = 1
    count = starting_number
    while count > 1:
        factorial_result *= count
        count -= 1

    return {"result": factorial_result}

